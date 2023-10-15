from Deck import Deck
from server import Player
import json
import random
import time

class Game:
    
    def __init__(self,players,peerSocket):
        self.players = json.loads(players, object_hook=self.player_decoder)
        self.deck = Deck()
        self.scores = {}
        self.peerSocket = peerSocket
    
    def player_decoder(self,obj):
        if 'name' in obj and 'ipv4' in obj and 'mport' in obj and 'rport' in obj and 'pport' in obj:
            return Player(obj['name'], obj['ipv4'],obj['mport'],obj['rport'],obj['pport'])
        return obj
    
    def get_player(self,name):
        for player in self.players:
            if(player.name == name):
                return player;
        return
        
    def deal_cards(self):
        self.scores = {player.name:0 for player in self.players}
        hands = self.deck.deal_cards(self.players);
        return hands
    
    def verify_books(self, name, hand,hands): # checks a name/hand for wins
        for card in set(hand):
            if hand.count(card) == 4:
                self.send_msg(f"verify_books:%{card}:%{hand}",self.get_player(name));
                for i in range(4):
                    hands[name].remove(card)
                self.scores[name] += 1
                #print('{} cleared the {}!'.format(name, card))
    
    def send_msg(self,message,player):
        self.peerSocket.sendto(message.encode(),(player.ipv4,int(player.pport)))
        time.sleep(0.5)
        #message, serverAdd = self.peerSocket.recvfrom(1024)
        return
    
    def make_choice(self,names,player,hands):
        ask = random.choice([name for name in names if name != player])
        card = random.choice(hands[player])

  
