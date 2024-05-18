import pytest
from deck import Deck

@pytest.fixture
def full_deck():
    deck = Deck()
    return deck

def test_create_deck(full_deck):
    # Count occurrences of each value and suit
    value_counts = {value: 0 for value in range(2, 15)}
    suit_counts = {"♠️": 0, "♥️": 0, "♣️": 0, "♦️": 0}

    # Iterate through the deck and count occurrences
    for card in full_deck.cards:
        value_counts[card.value] += 1
        suit_counts[card.suit] += 1

    for value in value_counts:
        assert value_counts[value] == 4

    for suit in suit_counts:
        assert suit_counts[suit] == 13

    assert len(full_deck.cards) == 52

def test_deck_shuffling(full_deck):
    original_order = full_deck.cards[:]
    full_deck.shuffle()

    assert original_order != full_deck.cards

def test_deal(full_deck):
    next_deal = full_deck.cards[-1]
    deal_card = full_deck.deal()

    assert next_deal == deal_card

def test_mulligan(full_deck):
    full_deck.shuffle()

    hand = []
    for _ in range(5):
        hand.append(full_deck.deal())
    
    redraw = full_deck.mulligan(hand)

    assert hand is not redraw
    
def test_create_duplicate_deck(full_deck):
    duplicate_deck = full_deck.create_duplicate_deck()

    # check they are not the same IN MEMORY
    assert duplicate_deck is not full_deck

    # also check that the cards are in the same order
    for card1, card2 in zip(full_deck.cards, duplicate_deck.cards):
        assert card1 == card2

def test_deal_card(full_deck):
    ace_heart = full_deck.deal_card(14, "♥️")

    assert ace_heart.suit == "♥️"
    assert ace_heart.value == 14
    assert ace_heart.face == 'Ace'

def test_generate_all_iteration(full_deck):
    all_iteration_list = full_deck.generate_all_iteration()

    assert len(all_iteration_list) == 2598960
    assert len(set(tuple(hand) for hand in all_iteration_list)) == 2598960