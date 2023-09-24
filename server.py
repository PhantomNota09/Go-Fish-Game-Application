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
    def __handle_connections(self, server_sock):
        while True:
            msgAndAddress = server_sock.recvfrom(1024)
            command = msgAndAddress[0].decode().strip().split()
            try:
                if(len(command) == 0):
                    continue
                elif(command[0] == "register"):
                    print(f'Received Register command from player with IP and Port:{msgAndAddress[1]}')
                    self.__print_command(command)
                    response = self.__register_player(command)
                elif(command[0] == "end"):
                    print(f'Received End command from player with IP and Port:{msgAndAddress[1]}')
                    self.__print_command(command)
                    response = self.__end_game(command)
                elif(command[0] == "de-register"):
                    print(f'Received de-register command from player with IP and Port:{msgAndAddress[1]}')
                    self.__print_command(command)
                    response = self.__de_register_player(command)
                elif(command[0] == "query" and command[1] == "players"):
                    print(f'Received query Players command from player with IP and Port:{msgAndAddress[1]}')
                    response = self.__query_players()
                elif(command[0] == "query" and command[1] == "games"):
                    print(f'Received Query Games command from player with IP and Port:{msgAndAddress[1]}')
                    response = self.__query_games()
                elif(command[0] == "start" and command[1] == "game"):
                    print(f'Received Start Game command from player with IP and Port:{msgAndAddress[1]}')
                    self.__print_command(command)
                    response = self.__start_game(command)
                else:
                    print(f'Received Invalid command from player with IP and Port:{msgAndAddress[1]}')
                    response = "FAILURE:%Unable to process command"
                server_sock.sendto(response.encode(),msgAndAddress[1])
            except Exception as err:
                print(f'Error while processing the command from {msgAndAddress[1]}:')
                self.__print_command(command)
                print(err)
            print("\n")
            print("\n")
    def __print_command(self,command):
        print(command)
    
    def __register_player(self,request):
        if request[1] in self.players.keys():
            return "FAILURE"
        self.players[request[1]] = Player(request[1],request[2],request[3],request[4],request[5]);
        return "SUCCESS"
    
    def __query_players(self):
        res = ""
        count = len(self.players);
        res = str(count) + ":%" + json.dumps([ob.__dict__ for ob in self.players.values()])
        return res
    def __start_game(self,request):
        res = "SUCCESS:%"
        if((int(request[3]) < 1 or int(request[3]) > 4) or (request[2] not in self.players.keys()) or (len(self.players) - len(self.gamers) - 1 < int(request[3]))):
            return "FAILURE"
        gameId = random.choices(string.ascii_uppercase + string.digits, k=4)
        gameId = "".join(gameId)
        potentialPlayers = list(set(self.players.keys())-set(self.gamers))
        potentialPlayers.remove(request[2])
        selectPlayers = random.choices(potentialPlayers,k=int(request[3]));
        self.games[gameId] = Game(gameId,request[2],[x for x in selectPlayers])
        selectPlayers.insert(0,request[2])
        self.gamers.extend(selectPlayers)
        res += gameId + ":%"
        res += json.dumps([self.players.get(ob).__dict__ for ob in selectPlayers])
        return res;
    
    def __query_games(self):
        res = ""
        count = len(self.games);
        res = str(count) + ":%" + json.dumps([self.games.get(ob).__dict__ for ob in self.games])
        return res
    
if __name__ == '__main__':
    server = Server()
    server.start()
