import socket
import time 
import re
from threading import Thread
from game import Game

severIp = ''
serverPort = 0
mPort = 0
rPort = 0
pPort = 0
clientName = ''
clientIp = ""
clientManagerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
peerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
dispFlag = True
stop_flag = False

#Method for taking the user input for clientIp, clientName, serverIp, serverPort, mPort, rPort, pPort
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
    peerSocket.bind(("",int(pPort)));
    clientManagerSocket.settimeout(5)
    peerSocket.setblocking(False)
    if(re.search(exp, serverIp) and mPort.isdigit() and rPort.isdigit() and pPort.isdigit()):
        return True
    return False

#method for constructing the register command and sending it to the server, recieving the response
def __register_player():
    request = f'register {clientName} {clientIp} {mPort} {rPort} {pPort}'
    clientManagerSocket.sendto(request.encode(),(serverIp,serverPort))
    message, serverAdd = clientManagerSocket.recvfrom(1024)
    print(message.decode())

#method for constructing the query players command and sending it to the server, recieving the response
def __query_players():
    request = f'query players'
    clientManagerSocket.sendto(request.encode(),(serverIp,serverPort))
    message, serverAdd = clientManagerSocket.recvfrom(1024)
    print(message.decode())

def handle_request(self,command):
    pass

#method for constructing the start game command and sending it to the server, recieving the response
def __start_game():
    k = input("Enter no.of desired Players: ")
    request = f'start game {clientName} {k}'
    clientManagerSocket.sendto(request.encode(),(serverIp,serverPort))
    message, serverAdd = clientManagerSocket.recvfrom(1024)
    players = message.decode()
    print(players)
    if(players != 'FAILURE'):
        print(players.split(':%')[2])
        __play_game(players.split(':%')[2])

#method for constructing the query games command and sending it to the server, recieving the response
def __query_games():
    request = f'query games'
    clientManagerSocket.sendto(request.encode(),(serverIp,serverPort))
    message, serverAdd = clientManagerSocket.recvfrom(1024)
    print(message.decode())
 
#method for constructing the end game command and sending it to the server, recieving the response   
def __end_game():
    gameId = input("Enter the GameId: ")
    request = f'end {gameId} {clientName}'
    clientManagerSocket.sendto(request.encode(),(serverIp,serverPort))
    message, serverAdd = clientManagerSocket.recvfrom(1024)
    print(message.decode())

#method for constructing the de-register player command and sending it to the server, recieving the response
def __de_register_player():
    request = f'de-register {clientName}'
    clientManagerSocket.sendto(request.encode(),(serverIp,serverPort))
    message, serverAdd = clientManagerSocket.recvfrom(1024)
    print(message.decode())
    

#Method to display menu options
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

def __play_game(players):
    game = Game(players,peerSocket);
    game.start();

def __game_phase():
    global dispFlag
    global stop_flag
    while not stop_flag:
        try:
            msgAndAddress = peerSocket.recvfrom(1024)
            command = msgAndAddress[0].decode().strip().split(':%')
        except BlockingIOError:
            continue
        
        if(len(command) == 0):
            continue
        elif(command[0] == "setup"):
            print("command Received: ",command[0],command[3])
            print(f"Game started with {command[2]} players and {command[1]} as manager")
            handle_request(command)
            print("\n")
            #dispFlag = False
        elif(command[0] == "deal_cards"):
            print("command Received: ",command[0],command[1])
            print(f"The inital cards dealt are : {command[1]}")
            handle_request(command)
            print("\n")
        elif(command[0] == "winner"):
            print("command Received: ",command[0],command[1])
            print(f"Game ended and {command[1]} is the winner")
            handle_request(command)
            print("\n")
            dispFlag = True
        elif(command[0] == "verify_books"):
            print(f"I cleared the book with {command[1]}. Sending message in the ring")
            print("command: ",command[0],command[1],command[2])
            handle_request(command)
            print("\n")
        elif(command[0] == "ask"):
            print("command Received: ",command[0],command[1],command[2])
            print(f"Recived ask message from {command[1]} for the card {command[2]}")
            handle_request(command)
            print("\n")
        elif(command[0] == "go_fish"):
            print("command Received: ",command[0],command[1])
            print(f"Received go_fish message from {command[1]}. Drawing the top card from deck")
            handle_request(command)
            print("\n")
        elif(command[0] == "your_move"):
            print("command Received: ",command[0])
            handle_request(command)
            print("\n")
        elif(command[0] == "catch"):
            print("command Received: ",command[0],command[1],command[2])
            print(f"Got the card {command[2]} from {command[1]}")
            print(f"The current hand is {command[3]}")
            handle_request(command)
            print("\n")
        elif(command[0] == "display"):
            print(command[1]);
            print("\n")
        #peerSocket.sendto("Received Message".encode(),msgAndAddress[1]);

# The main method which calls the appropriate method accrding the option selected by the user
if __name__ == '__main__':
    while(not  __get_input_params()):
        pass
    serverPort, mPort, rPort, pPort = int(serverPort), int(mPort), int(rPort), int(pPort)
    thread = Thread(target = __game_phase)
    thread.start()
    while True:
        if dispFlag:
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
                stop_flag = True
                thread.join()
                peerSocket.close();
                break;
            else:
                print("Invalid choice. Please select a valid option (1-7).")
