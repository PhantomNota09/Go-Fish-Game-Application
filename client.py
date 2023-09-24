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
