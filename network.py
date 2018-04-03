# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from model import *
import socket
import select
import threading

################################################################################
#                         EVENT MANAGER SERVER                                 #
################################################################################

### Class EventManagerServer ###

class EventManagerServer:

    def __init__(self, model):
        self.model = model

    # network events
    # ...

################################################################################
#                          NETWORK SERVER CONTROLLER                           #
################################################################################

class NetworkServerController:

    def __init__(self, model, evm, port, liste_attente):
        self.model = model
        self.evm = evm
        self.port = port
        self.liste_attente = liste_attente

    def tick(self, dt):
        read, writ, exc = select.select(self.liste_attente, [], [])
        server_sock = self.liste_attente[0]
        for sock in read:
            if sock == server_sock:
                s2, addr = sock.accept()
                self.liste_attente.append(s2)
            else:
                threading.Thread(None, event_manager, None, ()).start()
                liste_attente.remove(sock)
        print(self.liste_attente)
        return True

    def server_sock(self):
        s = socket.socket(family=socket.AF_INET6, type=socket.SOCK_STREAM, proto=0)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', self.port))
        s.listen(1)
        self.liste_attente.append(s)
        return s

################################################################################
#                         EVENT MANAGER CLIENT                                 #
################################################################################

### Class EventManagerClient ###

class EventManagerClient:

    def __init__(self, model):
        self.model = model

    # keyboard events
    def quit(self):
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

    # network events
    # ...

################################################################################
#                          NETWORK CLIENT CONTROLLER                           #
################################################################################

class NetworkClientController:

    def __init__(self, model, evm, host, port, nickname):
        self.model = model
        self.evm = evm
        self.host = host
        self.port = port
        self.nickname = nickname
        # ...

    def tick(self, dt):
        # ...
        return True

    def client_sock(self):
        s = socket.socket(family=socket.AF_INET6, type=socket.SOCK_STREAM, proto=0)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((self.host, self.port))
        return s