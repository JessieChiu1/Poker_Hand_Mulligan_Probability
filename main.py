from deck import Deck
from player import Player

def demo():
    # setup game
    deck = Deck()
    player = Player()
    deck.shuffle()

    for _ in range(5):
        player.draw(deck.deal())
    
    player.show_hand()
    print("\n")

    # calc best probabilities and best retained hand
    print("Generate and calculating all retained hand possibilities and their better hand probabilities\n")
    (best_retained_hand, best_probabilities) = player.find_best_retained_hand(player.hand, print_result=True)

    return best_probabilities

demo()