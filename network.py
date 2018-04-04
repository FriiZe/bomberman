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
        self.server_socket = socket.socket(family=socket.AF_INET6, type=socket.SOCK_STREAM, proto=0)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('', port))
        self.server_socket.listen(1)
        self.map_loaded = map_loaded
        self.player = None
        # ...

    # time event

    def socket_treatment(self, client_socket):
        while True:
            received_data = client_socket.recv(1500)

            if received_data == 0:
                client_socket.close()
                break

            decoded_data = received_data.decode()

            if decoded_data == "map":
                client_socket.send(self.map_loaded.encode())

            if decoded_data == "fruits":
                fruits_list = pickle.dumps(self.model.fruits)
                client_socket.send(fruits_list)

            #if decoded_data.startswith("nickname "):
            #    self.player = decoded_data

            #if decoded_data == "players":
            #    model.add_character()

    def tick(self, dt):
        accepted_socket, address = self.server_socket.accept()
        threading.Thread(None, self.socket_treatment, None, (accepted_socket,)).start()
        # ...
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
        self.client_socket = socket.socket(family=socket.AF_INET6, type=socket.SOCK_STREAM, proto=0)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.connect((host, port))

        self.client_socket.send("map".encode()) # request for map to download
        self.map_to_load = self.client_socket.recv(1500).decode()
        self.model.load_map(self.map_to_load)

        self.client_socket.send("fruits".encode()) #request for fruits
        self.fruits = pickle.loads(self.client_socket.recv(1500))
        for i in range(len(self.fruits)):
            model.add_fruit(self.fruits[i].kind, self.fruits[i].pos)

        #nickname = "nickname " + self.nickname # request for creating a character
        #self.client_socket.send(nickname.encode())
        #self.player = self.client_socket.recv(1500).decode()

        #self.client_socket.send("players".encode()) #request for players
        #self.players = pickle.loads(self.client_socket.recv(1500))
        #for i in range(len(self.players)):
        # ...

    # keyboard events

    def keyboard_quit(self):
        print("=> event \"quit\"")
        return False

    def keyboard_move_character(self, direction):
        print("=> event \"keyboard move direction\" {}".format(DIRECTIONS_STR[direction]))
        # ...
        return True

    def keyboard_drop_bomb(self):
        print("=> event \"keyboard drop bomb\"")
        # ...
        return True

    # time event

    def tick(self, dt):
        # ...
        return True
