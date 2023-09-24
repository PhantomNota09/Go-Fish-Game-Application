import socket
import time 
import re

severIp = ''
serverPort = 0
mPort = 0
rPort = 0
pPort = 0
clientName = ''
clientIp = ""
clientManagerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
