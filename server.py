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
