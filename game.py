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
            
            if not success:
                self.send_msg(f"display:%The cards donot Match!! Go fish!",self.get_player(ask));
                self.send_msg(f"go_fish:%{ask}",self.get_player(player));
                #print('Go fish!')
                self.send_msg(f"display:%Drawing the card from the deck and sending it to {ask}",self.get_player(player)); 
                if self.deck.cards:
                    hands[player].append(self.deck.cards.pop())
                    self.send_msg(f"display:%Received the card {hands[player][-1]} from {player}",self.get_player(ask));
                    if hands[player][-1] == card:
                        success = True
                        self.send_msg(f"display:%Lucky!! The last drawn card match the ask",self.get_player(player));                       
                        #print('Fished the {}! Lucky!'.format(card))
                    else:
                        self.send_msg(f"display:%The last drawn card doesn't match the ask. Passing the turn to next player.",self.get_player(player));
                        
                else:
                    self.send_msg(f"display:%Cant draw a card!! No deck. Passing the turn to next player.",self.get_player(player)); 
                    #print('Can\'t fish - no deck.')
            else:
                self.send_msg(f"display:%There is a hit!! Giving the card {card} to {player}",self.get_player(ask));
                self.send_msg(f"catch:%{ask}:%{card}:%{hands[player]}",self.get_player(player));
                #print('{} got the {} from {}.'.format(player, card, ask))
            if not success:
                prev_idx = idx
                idx += 1
                if idx >= len(names):
                    idx = 0
            
            self.verify_books(player, hands.get(player),hands)
            
            if sum(self.scores.values()) == 13:
                size = max(map(len, names))
                sorted_scores = sorted(self.scores, key=self.scores.get, reverse=True)
                for key, value in hands.items():
                    self.send_msg(f"winner:%{sorted_scores[0]}",self.get_player(key));
                
                print('Scores:')
                for k in sorted_scores:
                    print(k.ljust(size), self.scores[k])
                break
    
