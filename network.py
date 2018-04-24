# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from model import *
import socket
import threading
import select
import pickle
import errno

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
        self.change = False
        self.clients = {}
        self.disconnected_clients = {}
        # ...

    # time event
    def connexion(self):
        #on attend une socket et on crée un thread lorsqu'on en a une
        while True:
            accepted_socket, (address, port) = self.server_socket.accept()
            threading.Thread(None, self.socket_treatment, None, (accepted_socket, address)).start()

    # Fonction de traitement de chaque socket
    def socket_treatment(self, client_socket, address):
        while True:
            received_data = client_socket.recv(1500).split("|".encode())

            if received_data[0] == 0:
                client_socket.close()
                break

            decoded_data = received_data[0].decode()

			##################################################
			#### Messages recus par le serveur et analyse ####
			##################################################
            with self.lock:
                if decoded_data == "map":
                    # on envoie la map
                    client_socket.sendall(self.map_loaded.encode())

                if decoded_data.startswith("nickname "):
                    # on envoie la liste des persos après avoir ajouté le nouveau
                    nickname = decoded_data.replace("nickname ", "")
                    
                    if len(self.disconnected_clients) > 0:
                        for disconnected in self.disconnected_clients:
                            if disconnected == nickname and self.disconnected_clients[nickname][2] == address:
                                self.model.characters.append(self.disconnected_clients[nickname][1])
                                self.disconnected_clients.pop(nickname, None)
                                break
                            else:
                                self.model.add_character(nickname)
                                break
                    else:
                        self.model.add_character(nickname)
                    
                    self.clients[nickname] = [client_socket, None, address]
                    client_socket.sendall(pickle.dumps(self.model.characters))
                
            with self.lock:
                if decoded_data.startswith("move "):
                    # sépare les éléments du message ["move", "nickname", "direction"]
                    list_data = decoded_data.split(" ")
                    # on move le perso
                    self.model.move_character(list_data[1], int(list_data[2]))
                
                if decoded_data.startswith("drop_bomb "):
                    # ajoute une bombe au model
                    self.model.drop_bomb(decoded_data.replace("drop_bomb ", ""))

                if decoded_data.startswith("disconnect"):
                    self.clients[nickname][1] = self.model.look(nickname)
                    self.model.kill_character(nickname)
                    self.disconnected_clients[nickname] = self.clients[nickname]
                    self.clients.pop(nickname, None)
                    client_socket.close()
                    break

                self.change = True
			#####################
			#### Fin analyse ####
			#####################
    def send_model(self):
        for client in self.clients.values():
            datas = [self.model.characters, self.model.fruits, self.model.bombs]
            client[0].sendall(pickle.dumps(datas))

    def tick(self, dt):
        # ...
        if self.change == True:
            self.send_model()
            self.change = False
        return True

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

        # request for creating a character
        nickname = "nickname " + self.nickname + "|"
        self.client_socket.sendall(nickname.encode())
        self.model.characters = pickle.loads(self.client_socket.recv(1500))
        # ...

        self.client_socket.setblocking(False)

	#########################
	#### keyboard events ####
	#########################
    
    def keyboard_quit(self):
        self.client_socket.sendall("disconnect".encode())
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

    # time event

    def tick(self, dt):
        try:
            decoded_data = pickle.loads(self.client_socket.recv(15000))
            self.model.characters = decoded_data[0]
            self.model.fruits = decoded_data[1]
            self.model.bombs = decoded_data[2]
        except socket.error as e:
            if e.args[0] == errno.EWOULDBLOCK:
                pass
            else:
                print("Socket error: ", e)
        return True
