import platform
from deck import Deck
from player import Player
import os
from tqdm import tqdm

TEST_VALUES = [10,11,12,13,14]
TEST_SUITS = ["♠️", "♠️", "♠️", "♠️","♠️"]
TEST_LOOP = 1000

def clear_terminal():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def random_test_case():
    # setup game
    deck = Deck()
    player = Player()
    deck.shuffle()

    for _ in range(5):
        player.draw(deck.deal())
    
    player.show_hand()
    print("\n")

    # calc best probabilities and best retained hand
    (best_retained_hand, best_probabilities) = player.find_best_retained_hand(player.hand, print_result=True)

    if best_probabilities > 1:
        return
    return best_probabilities

def specific_test_case():
    # setup game
    deck = Deck()
    player = Player()
    deck.shuffle()

    for i in range(5):
        player.draw(deck.deal_card(TEST_VALUES[i], TEST_SUITS[i]))

    player.show_hand()
    print("\n")

    # calc best probabilities and best retained hand
    player.find_best_retained_hand(player.hand, print_result=True)

def all_iteration():
    # setup game
    deck = Deck()
    player = Player()

    all_iteration_list = deck.generate_all_iteration()

    for iter in tqdm(all_iteration_list, desc="Calculating probabilities", unit="combination"):
        try:
            (best_retained_hand, best_probabilities) = player.find_best_retained_hand(iter)

            if best_probabilities > 1:
                return
            else:
                clear_terminal()
        except TypeError:
            print(f"given hand: {[str(card) for card in iter]}")
            return
        
option = input(f"Random test {TEST_LOOP}x (Y)\nSpecific test case (N)\nAll 2,598,960 hand combination (A)\n")

if option == "Y":
    for _ in range(TEST_LOOP):
        random_test_case()
        clear_terminal()
if option == "N":
    specific_test_case()
if option == "A":
    all_iteration()