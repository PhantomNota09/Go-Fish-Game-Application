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

def __get_input_params():
    regex = "(([0-9]|[1-9][0-9]|1[0-9][0-9]|"\
            "2[0-4][0-9]|25[0-5])\\.){3}"\
            "([0-9]|[1-9][0-9]|1[0-9][0-9]|"\
            "2[0-4][0-9]|25[0-5])"
    exp = re.compile(regex)
    global clientIp, clientName, serverIp, serverPort, mPort, rPort, pPort
    clientName, clientIp, serverIp, serverPort, mPort, rPort, pPort = input("Enter client Name, clientIp, severIP, server Port, m-port, r-port, p-port [space sepearated]:").rsplit(" ",7)
    print(clientName)
    print(serverIp)
    print(serverPort)
    print(mPort)
    print(rPort)
    print(pPort)
    clientManagerSocket.bind(("",int(mPort)))
    clientManagerSocket.settimeout(5)
    if(re.search(exp, serverIp) and mPort.isdigit() and rPort.isdigit() and pPort.isdigit()):
        return True
    return False

def __register_player():
    request = f'register {clientName} {clientIp} {mPort} {rPort} {pPort}'
    clientManagerSocket.sendto(request.encode(),(serverIp,serverPort))
    message, serverAdd = clientManagerSocket.recvfrom(1024)
    print(message.decode())

def __query_players():
    request = f'query players'
    clientManagerSocket.sendto(request.encode(),(serverIp,serverPort))
    message, serverAdd = clientManagerSocket.recvfrom(1024)
    print(message.decode())

def __start_game():
    k = input("Enter no.of desired Players: ")
    request = f'start game {clientName} {k}'
    clientManagerSocket.sendto(request.encode(),(serverIp,serverPort))
    message, serverAdd = clientManagerSocket.recvfrom(1024)
    print(message.decode())

def __query_games():
    request = f'query games'
    clientManagerSocket.sendto(request.encode(),(serverIp,serverPort))
    message, serverAdd = clientManagerSocket.recvfrom(1024)
    print(message.decode())

def __end_game():
    gameId = input("Enter the GameId: ")
    request = f'end {gameId} {clientName}'
    clientManagerSocket.sendto(request.encode(),(serverIp,serverPort))
    message, serverAdd = clientManagerSocket.recvfrom(1024)
    print(message.decode())

def __de_register_player():
    request = f'de-register {clientName}'
    clientManagerSocket.sendto(request.encode(),(serverIp,serverPort))
    message, serverAdd = clientManagerSocket.recvfrom(1024)
    print(message.decode())
    

def __display_options():
    print("***************************")
    print("***************************")
    print("***************************")
    print("Menu:")
    print("1. Register Player")
    print("2. Query Players")
    print("3. Start Game")
    print("4. Query Games")
    print("5. End Game")
    print("6. De-register Player")
    print("7. Exit the program")
    print("***************************")

if __name__ == '__main__':
    while(not  __get_input_params()):
        pass
    serverPort, mPort, rPort, pPort = int(serverPort), int(mPort), int(rPort), int(pPort)
    while True:
        __display_options()
        choice = input("Enter your choice: ")
        if choice == "1":
            __register_player()
        elif choice == "2":
            __query_players()
        elif choice == "3":
            __start_game()
        elif choice == "4":
            __query_games()
        elif choice == "5":
            __end_game()
        elif choice == "6":
            __de_register_player()
        elif choice == "7":
            print("Exiting the program.")
            clientManagerSocket.close()
        else:
            print("Invalid choice. Please select a valid option (1-7).")
