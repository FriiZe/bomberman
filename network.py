# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from model import *
import socket
import threading
import select
import pickle

################################################################################
#                          NETWORK SERVER CONTROLLER                           #
################################################################################

class NetworkServerController:

    def __init__(self, model, port, map_loaded):
        self.model = model
        self.port = port
        self.server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('', port))
        self.server_socket.listen(1)
        threading.Thread(None, self.connexion, None, ()).start()
        self.map_loaded = map_loaded
        self.lock = threading.Lock()
        # ...

    # time event
    def connexion(self):
        #on attend une socket et on crée un thread lorsqu'on en a une
        while True:
            accepted_socket, address = self.server_socket.accept()
            threading.Thread(None, self.socket_treatment, None, (accepted_socket,)).start()

    # Fonction de traitement de chaque socket
    def socket_treatment(self, client_socket):
        while True:
            received_data = client_socket.recv(1500).split("|".encode())

            if received_data[0] == 0:
                client_socket.close()
                break

            decoded_data = received_data[0].decode()
			
			##################################################
			#### Messages recus par le serveur et analyse ####
			##################################################

            if decoded_data == "map":
				# on envoie la map
                client_socket.sendall(self.map_loaded.encode())

            if decoded_data == "fruits":
				# on envoie la liste des fruits
                client_socket.sendall(pickle.dumps(self.model.fruits))

            if decoded_data.startswith("nickname "):
				# on envoie la liste des persos après avoir ajouté le nouveau
                with self.lock:
                    self.model.add_character(decoded_data.replace("nickname ", ""))
                client_socket.sendall(pickle.dumps(self.model.characters))
            
            if decoded_data.startswith("move "):
				# sépare les éléments du message ["move", "nickname", "direction"]
                list_data = decoded_data.split(" ")
				# on move le perso
                with self.lock:
                    self.model.move_character(list_data[1], int(list_data[2]))
            
            if decoded_data.startswith("drop_bomb "):
				# ajoute une bombe au model
                with self.lock:
                    self.model.drop_bomb(decoded_data.replace("drop_bomb ", ""))
            
            if decoded_data.startswith("get_model "):
				# on separe la commande principale de la commande secondaire
                model_part = decoded_data.replace("get_model ", "")
                if model_part == "characters":
					#on envoie la liste des persos
                    client_socket.sendall(pickle.dumps(self.model.characters))
                
                if model_part == "fruits":
					# on envoie la liste des fruits
                    client_socket.sendall(pickle.dumps(self.model.fruits))
                
                if model_part == "bombs":
					# on envoie la liste des bombes
                    client_socket.sendall(pickle.dumps(self.model.bombs))

			#####################
			#### Fin analyse ####
			#####################

    #def tick(self, dt):
        # ...
        #return True

################################################################################
#                          NETWORK CLIENT CONTROLLER                           #
################################################################################

class NetworkClientController:

    def __init__(self, model, host, port, nickname):
        self.model = model
        #self.host = host
        #self.port = port
        self.nickname = nickname

        # client socket
        self.client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.connect((host, port))

        # request for map to download
        self.client_socket.sendall("map|".encode())
        self.map_to_load = self.client_socket.recv(1500).decode()
        self.model.load_map(self.map_to_load)

        #request for fruits
        self.client_socket.sendall("fruits|".encode())
        self.model.fruits = pickle.loads(self.client_socket.recv(1500))

        # request for creating a character
        nickname = "nickname " + self.nickname + "|"
        self.client_socket.sendall(nickname.encode())
        self.model.characters = pickle.loads(self.client_socket.recv(1500))
        # ...

	#########################
	#### keyboard events ####
	#########################
    
    def keyboard_quit(self):
        print("=> event \"quit\"")
        return False

    def keyboard_move_character(self, direction):
        print("=> event \"keyboard move direction\" {}".format(DIRECTIONS_STR[direction]))
        if direction in DIRECTIONS:
            command = "move " + self.nickname + " " + str(direction) + "|"
            self.client_socket.sendall(command.encode())
        # ...
        return True

    def keyboard_drop_bomb(self):
        print("=> event \"keyboard drop bomb\"")
        command = "drop_bomb " + self.nickname + "|"
        self.client_socket.sendall(command.encode())
        # ...
        return True

    #############################
    #### End keyboard events ####
    #############################
    
	# fonction pour demander en continu les infos au serveur
    def get_model(self):
        self.client_socket.sendall("get_model characters|".encode())
        self.model.characters = pickle.loads(self.client_socket.recv(1500))

        self.client_socket.sendall("get_model fruits|".encode())
        self.model.fruits = pickle.loads(self.client_socket.recv(1500))

        self.client_socket.sendall("get_model bombs|".encode())
        self.model.bombs = pickle.loads(self.client_socket.recv(1500))

    # time event

    def tick(self, dt):
        self.get_model()
        # ...
        return True
