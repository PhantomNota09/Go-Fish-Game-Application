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


    
    def start(self):
        hands = self.deal_cards();
        
        
        for key, value in hands.items():
            self.send_msg(f"setup:%{self.players[0].name}:%{len(self.players)}:%{json.dumps([ob.__dict__ for ob in self.players])}",self.get_player(key));
        for key, value in hands.items():
            self.send_msg(f"deal_cards:%{value}",self.get_player(key));
        
        
        for player in self.players:
            self.verify_books(player.name,hands.get(player.name),hands);
        idx = 1
        prev_idx = 0
        names = list(hands.keys())
        while 1:
            player = names[idx] #selecting the player
            if prev_idx != idx:
                self.send_msg(f"your_move",self.get_player(player));
            if not hands[player]: # handles player not having a hand
                if self.deck.cards:
                    hands[player].append(self.deck.cards.pop())
                else:
                    prev_idx = idx
                    idx += 1
                    if idx >= len(names):
                        idx = 0
                    continue
            ask = random.choice([name for name in names if name != player])
            card = random.choice(hands[player])
            self.send_msg(f"display:%Asking {ask} for the card {card}",self.get_player(player));
            self.send_msg(f"ask:%{player}:%{card}",self.get_player(ask));
            #print('{} asks for {} from {}.'.format(player, card, ask))
            
            success = False
            while card in hands[ask]:
                hands[ask].remove(card)
                hands[player].append(card)
                success = True
