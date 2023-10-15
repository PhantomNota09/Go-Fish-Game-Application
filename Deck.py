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
if __name__ == '__main__':
    deck = Deck();
    players = "[{\"name\": \"client2\", \"ipv4\": \"192.168.0.4\", \"mport\": \"15561\", \"rport\": \"15562\", \"pport\": \"15563\"}, {\"name\": \"client1\", \"ipv4\": \"192.168.0.4\", \"mport\": \"15551\", \"rport\": \"15552\", \"pport\": \"15553\"}]"
    players = json.loads(players, object_hook=deck.player_decoder)
    print(players)
    deck.deal_cards(players);
