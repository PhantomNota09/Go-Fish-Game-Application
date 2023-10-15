import random
from server import Player
import json

class Deck:
    
    def __init__(self):
        self.cards = list('0123456789JQKA'*4);
    
    def deal_cards(self,players):
        random.shuffle(self.cards);
        if len(players) > 4:
            hand_size = 5
        else:
            hand_size = 7
        hands = {player.name : [self.cards.pop() for i in range(hand_size)] for player in players}
        #print(hands)
        return hands;
    
    def player_decoder(self,obj):
        if 'name' in obj and 'ipv4' in obj and 'mport' in obj and 'rport' in obj and 'pport' in obj:
            return Player(obj['name'], obj['ipv4'],obj['mport'],obj['rport'],obj['pport'])
        return obj
