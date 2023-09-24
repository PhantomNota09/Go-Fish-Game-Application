import socket
import json
import random
import string

class Player:
    
    def __init__(self,name,ipv4,mport,rport,pport):
        self.name = name;
        self.ipv4 = ipv4;
        self.mport = mport;
        self.rport = rport;
        self.pport = pport;

class Game:
    
    def __init__(self,id,manager,players):
        self.id = id
        self.manager = manager
        self.players = players
class Server(object):
    
    def __init__(self):
        self.port = 15503
        self.players = {}
        self.games = {}
        self.gamers = []
    
    def start(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
        serversocket.bind(("", self.port))
        print('Server started running...')
        #print(f'serverIp : {socket.gethostbyname(socket.gethostname())}')
        print(f'server port = {self.port}')
        self.__handle_connections(serversocket)
if __name__ == '__main__':
    server = Server()
    server.start()
