import random
import itertools
from card import Card

class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()

    def create_deck(self):
        """
        At init - create a full poker deck
        """
        suits = ["♠️", "♥️", "♣️", "♦️"]
        values = range(2, 15) 
        for suit, value in itertools.product(suits, values):
            self.cards.append(Card(suit, value))

    def shuffle(self):
        """
        Shuffle deck 
        """
        random.shuffle(self.cards)

    def showDeck(self):
        """
        print card in deck
        """
        for card in self.cards:
            print(str(card))

    def deal(self):
        """
        Deal the last card of the deck
        """
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None
        
    def mulligan(self, mulligan_list):
        """
        Given a list of card to mulligan - return those card(s) to the deck and redraw the same num of discarded card
        """
        redraw = []
        for card in mulligan_list:
            self.cards.append(card)
        self.shuffle()
        for _ in range(len(mulligan_list)):
            redraw.append(self.deal())
        return redraw

    def create_duplicate_deck(self):
        """
        Create a copy of the deck
        """
        new_deck = Deck()
        new_deck.cards = self.cards[:]
        return new_deck

    def deal_card(self, value, suit):
        """
        Given a value and a suit, deal a specific card from the deck
        """
        for card in self.cards:
            if card.value == value and card.suit == suit:
                self.cards.remove(card)
                return card
        return None
    
    def generate_all_iteration(self):
        """
        Generate all 2,598,960 poker hand combination from a poker deck
        """
        all_iteration = itertools.combinations(self.cards, 5)
        all_iteration_list = [list(hand) for hand in all_iteration]

        return all_iteration_list
    
