import pytest
import random
from player import Player
from deck import Deck
from card import Card
import itertools
import math

# region fixture and helper function
@pytest.fixture
def player():
    player = Player()
    return player

@pytest.fixture
def full_deck():
    return Deck()

def random_five():
    deck = Deck()
    deck.shuffle()
    hand = []
    for _ in range(5):
        hand.append(deck.deal())

    return hand

# helper function to create hardcoded hand
# require both list to be same length
def create_hand(num_list, suit_list):
    hand = []

    for i in range(len(num_list)):
        card = Card(suit_list[i], num_list[i])
        hand.append(card)
    
    return hand

def random_straight_num_list(allow_royal_flush=True):
    if allow_royal_flush:
        consecutive_value_combos = [(i, i+1, i+2, i+3, i+4) for i in range(2, 11)]
    else:
        consecutive_value_combos = [(i, i+1, i+2, i+3, i+4) for i in range(2, 10) ]
    straight_combo = random.choice(consecutive_value_combos)
    return straight_combo

def random_suits(count=1):
    if count == 5:
        return ["♠️", "♥️", "♣️", "♦️", "♠️"]

    return random.sample(["♠️", "♥️", "♣️", "♦️"], k=count)

def random_nums(count=1):
    return random.sample(range(2, 15), k=count)

# for 2x/3x/4x combinations
def all_iter_combination(count, num_list, print_result=False):
    suits = ["♠️", "♥️", "♣️", "♦️"]

    all_possibilities = []

    for num in num_list:
        same_card_value = []
        for suit in suits:
            same_card_value.append(Card(suit, num))
        combinations = itertools.combinations(same_card_value, count)
        all_possibilities.extend([list(combination) for combination in combinations])

    if print_result == True:
        for combo in all_possibilities:
            print([str(card) for card in combo])

    return all_possibilities
    
def hand_in_valid_combination(retained_hand, all_combinations, print_result=False):
    valid_combinations = []
    hand_str = [str(card) for card in retained_hand]
    
    for combo in all_combinations:
        str_combo = [str(card) for card in combo]
        if all(card in str_combo for card in hand_str):
            valid_combinations.append(combo)

    if print_result:
        print(f"Printing all valid combinations for {hand_str}:")
        for combo in valid_combinations:
            str_combo = [str(card) for card in combo]
            print(str_combo)

    return valid_combinations

# for straight flush - we exclude royal - flush = True, royal=False
# for straight only - we include royal - flush = False, royal=True
def all_iter_consecutive_combination(flush, royal, print_result=False):
    all_straight_any_suit = []
    consecutive_value_combos = [(i, i+1, i+2, i+3, i+4) for i in range(2, 10)]
    if royal:
        consecutive_value_combos = [(i, i+1, i+2, i+3, i+4) for i in range(2, 11)]

    suits = ['♠️', '♥️', '♣️', '♦️']

    for combo in consecutive_value_combos:
        card_possibilities = []
        for num in combo:
            dummy = []
            for suit in suits:
                dummy.append(Card(suit, num))
            card_possibilities.append(dummy)
        for cards in itertools.product(*card_possibilities):
            all_straight_any_suit.append(list(cards))

    all_straight_flush = []
    all_straight = []

    for combo in all_straight_any_suit:
        suit_list = [card.suit for card in combo]
        if len(set(suit_list)) == 1:
            all_straight_flush.append(combo)
        else:
            all_straight.append(combo)
    
    output = all_straight_flush if flush else all_straight

    if print_result:
        for combo in output:
            print([str(card) for card in combo])

    return output

# for iteration of random number that is not the same value
# (2H, 3H) in output
# (2H, 2S) not in output
# excluded all pairs/triple/quad
def random_num_combination(count, num_list):
    suits = ["♠️", "♥️", "♣️", "♦️"]
    deck = [Card(suit, value) for suit, value in itertools.product(suits, num_list)]
    
    all_combinations = itertools.combinations(deck, count)

    output = []

    for combo in all_combinations:
        combo_list = list(combo)
        values = [card.value for card in combo_list]
        if len(set(values)) == count:
            output.append(combo_list)

    return output

# endregion fixture and helper function

# SPECIFIC TEST CASE
TEST_GIVEN_HAND = create_hand([10,11,12,13,14], ["♥️", "♦️", "♣️", "♠️","♦️"])
TEST_RETAINED_HAND = [TEST_GIVEN_HAND[1], TEST_GIVEN_HAND[2], TEST_GIVEN_HAND[-1]]

print("TEST_GIVEN_HAND: ", [str(card) for card in TEST_GIVEN_HAND])
print("TEST_RETAINED_HAND: ", [str(card) for card in TEST_RETAINED_HAND])


# region interact with deck and hand
def test_draw(player: Player, full_deck: Deck):
    num_card_before = len(player.hand)
    drawn_card = full_deck.deal()
    player.draw(drawn_card)
    assert len(player.hand) == num_card_before + 1

    assert drawn_card in player.hand

    assert drawn_card not in full_deck.cards

def test_mulligan(player: Player, full_deck: Deck):
    for _ in range(5):
        drawn_card = full_deck.deal()
        player.draw(drawn_card)
    
    before = player.hand[:]

    player.mulligan(player.hand, full_deck)
    
    assert before != player.hand

def test_is_same_suit(player: Player):
    # scenario 1: same suit
    hand = create_hand(random_nums(5), random_suits(1)*5)
    assert player.is_same_suit(hand) == True

    # scenario 2: different suit
    hand = create_hand(random_nums(5), ["♠️", "♥️", "♣️", "♦️","♦️"])
    assert player.is_same_suit(hand) == False

    # scenario 3: no card in hand
    assert player.is_same_suit([]) == True

def test_generate_all_retained_hand_combination(player: Player):
    given_hand = create_hand(random_nums(5), random_suits(5))
    all_choose_one = math.comb(5,1)
    all_choose_two = math.comb(5,2)
    all_choose_three = math.comb(5,3)
    all_choose_four = math.comb(5,4)
    all_choose_none = math.comb(5,0)
    total_combination = all_choose_none + all_choose_one + all_choose_two + all_choose_three + all_choose_four
    assert len(player.generate_all_retained_hand_combination(given_hand)) == total_combination

def test_generate_method_list(player: Player):
    # scenario 1: high card
    given_hand = create_hand([2,4,6,8,9], random_suits(5))
    method_list = player.generate_method_list(given_hand)
    current_hand_name = method_list[0]["name"]
    assert current_hand_name == "high card"
    assert len(method_list) == 10

    # scenario 2: one pair
    given_hand = create_hand([6,6,10,11,12], random_suits(5))
    method_list = player.generate_method_list(given_hand)
    current_hand_name = method_list[0]["name"]
    assert current_hand_name == "one pair"
    assert len(method_list) == 9

    # scenario 3: two pair
    given_hand = create_hand([2,2,4,4,7], random_suits(5))
    method_list = player.generate_method_list(given_hand)
    current_hand_name = method_list[0]["name"]
    assert current_hand_name == "two pair"
    assert len(method_list) == 8

    # scenario 4: three of a kind
    given_hand = create_hand([7,7,7,8,9], random_suits(5))
    method_list = player.generate_method_list(given_hand)
    current_hand_name = method_list[0]["name"]
    assert current_hand_name == "three of a kind"
    assert len(method_list) == 7

    # scenario 5: straight
    given_hand = create_hand([5,6,7,8,9], random_suits(5))
    method_list = player.generate_method_list(given_hand)
    current_hand_name = method_list[0]["name"]
    assert current_hand_name == "straight"
    assert len(method_list) == 6

    # scenario 6: flush
    given_hand = create_hand([2,6,8,10,14], random_suits(1)*5)
    method_list = player.generate_method_list(given_hand)
    current_hand_name = method_list[0]["name"]
    assert current_hand_name == "flush"
    assert len(method_list) == 5

    # scenario 7: full house
    given_hand = create_hand([10,10,10,5,5], random_suits(5))
    method_list = player.generate_method_list(given_hand)
    current_hand_name = method_list[0]["name"]
    assert current_hand_name == "full house"
    assert len(method_list) == 4

    # scenario 8: 4 of a kind
    given_hand = create_hand([14,14,14,14,10], random_suits(5))
    method_list = player.generate_method_list(given_hand)
    current_hand_name = method_list[0]["name"]
    assert current_hand_name == "four of a kind"
    assert len(method_list) == 3

    # scenario 9: straight flush
    given_hand = create_hand([9,10,11,12,13], random_suits(1)*5)
    method_list = player.generate_method_list(given_hand)
    current_hand_name = method_list[0]["name"]
    assert current_hand_name == "straight flush"
    assert len(method_list) == 2

    # scenario 10: royal flush
    given_hand = create_hand([10,11,12,13,14], random_suits(1)*5)
    method_list = player.generate_method_list(given_hand)
    current_hand_name = method_list[0]["name"]
    assert current_hand_name == "royal flush"
    assert len(method_list) == 1

# endregion interact with deck
    
# region check combo method

def test_is_royal_flush(player: Player):
    # scenario 1: True
    values = [10, 11, 12, 13, 14]
    hand = create_hand(values, random_suits(1)*5)
    assert player.is_royal_flush(hand) == True

    # scenario 2: False - straight flush not royal
    hand = create_hand(random_straight_num_list(allow_royal_flush=False), random_suits(1)*5)
    assert player.is_royal_flush(hand) == False

    # Sanity checks - hardcoded number
    hand = create_hand([10,11,12,13,14], ["♣️"]*5)
    assert player.is_royal_flush(hand) == True

    hand = create_hand([2,3,4,5,6], ["♣️"]*5)
    assert player.is_royal_flush(hand) == False

def test_is_straight_flush(player: Player):
    # Scenario 1: True - Random straight flush
    # make sure Ace is not included to ensure non-royal-flush
    hand = create_hand(random_straight_num_list(allow_royal_flush=False), random_suits(1)*5)
    assert player.is_straight_flush(hand) == True

    # Scenario 2: False - Royal straight flush
    hand = create_hand([10,11,12,13,14], random_suits(1)*5)
    assert player.is_straight_flush(hand) == False

    # Sanity checks - hardcoded number
    hand = create_hand([9,10,11,12,13], ["♣️"]*5)
    assert player.is_straight_flush(hand) == True

    hand = create_hand([10,11,12,13,14], ["♣️"]*5)
    assert player.is_straight_flush(hand) == False

    hand = create_hand([2,3,4,6,10], ["♠️"]*4 + ["♦️"])
    assert player.is_straight_flush(hand) == False

    # Test
    assert player.is_straight_flush(TEST_GIVEN_HAND) == False

def test_is_four_of_a_kind(player: Player):
    # scenario 1: True
    num = random_nums(2)
    hand = create_hand([num[0]]*4 + [num[1]], random_suits(5))
    assert player.is_four_of_a_kind(hand) == True

    # Sanity checks - hardcoded numbers
    hand = create_hand([2, 2, 2, 2, 3], random_suits(5))
    assert player.is_four_of_a_kind(hand) == True

    hand = create_hand([2, 3, 5, 8, 14], random_suits(5))
    assert player.is_four_of_a_kind(hand) == False

def test_is_full_house(player: Player):
    # scenario 1: True
    num = random_nums(2)
    hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    assert player.is_full_house(hand) == True

    # Sanity checks - hardcoded numbers
    hand = create_hand([2,2,2,3,3], random_suits(5))
    assert player.is_full_house(hand) == True

    hand = create_hand([4,7,9,10,13], random_suits(5))
    assert player.is_full_house(hand) == False

def test_is_flush(player: Player):
    # scenario 1: True
    hand = create_hand([2,4,5,8,10], random_suits(1)*5)
    print([str(card) for card in hand])
    assert player.is_flush(hand) == True

    # scenario 2: False - royal flush
    hand = create_hand([10,11,12,13,14], random_suits(1)*5)
    assert player.is_flush(hand) == False

    # scenario 3: False - straight flush
    hand = create_hand(random_straight_num_list(allow_royal_flush=False), random_suits(1)*5)
    assert player.is_flush(hand) == False

    # Sanity checks - hardcoded numbers
    hand = create_hand([2,4,5,8,10], ["♦️"]*5)
    assert player.is_flush(hand) == True

    hand = create_hand([2,3,4,5,6], ["♦️"]*5)
    assert player.is_flush(hand) == False

    hand = create_hand([2,4,5,8,10], ["♠️", "♥️", "♣️", "♦️", "♠️"])
    assert player.is_flush(hand) == False

def test_is_straight(player: Player):
    # scenario 1: True
    hand = create_hand(random_straight_num_list(allow_royal_flush=False), random_suits(5))
    assert player.is_straight(hand) == True

    # scenario 2: False - royal flush
    hand = create_hand([10,11,12,13,14], random_suits(1)*5)
    assert player.is_straight(hand) == False

    # scenario 3: False - straight flush
    hand = create_hand(random_straight_num_list(allow_royal_flush=False), random_suits(1)*5)
    assert player.is_straight(hand) == False

    # Sanity checks - hardcoded numbers
    hand = create_hand([2,3,4,5,6], random_suits(5))
    assert player.is_straight(hand) == True

    hand = create_hand([2,3,4,5,6], random_suits(1)*5)
    assert player.is_straight(hand) == False

    hand = create_hand([2,4,6,8,10], random_suits(1)*5)
    assert player.is_straight(hand) == False

def test_is_three_of_a_kind(player: Player):
    # scenario 1: True
    num = random_nums(3)
    hand = create_hand([num[0]]*3 + [num[1]] + [num[2]], random_suits(5))
    assert player.is_three_of_a_kind(hand) == True

    # scenario 2: False - full house
    num = random_nums(2)
    hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    assert player.is_three_of_a_kind(hand) == False

    # Sanity checks - hardcoded numbers
    hand = create_hand([2,2,2,4,5], random_suits(5))
    assert player.is_three_of_a_kind(hand) == True

    hand= create_hand([2,2,2,4,4], random_suits(5))
    assert player.is_three_of_a_kind(hand) == False

def test_is_two_pair(player: Player):
    # scenario 1: True
    num = random_nums(3)
    hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    assert player.is_two_pair(hand) == True

    # scenario 2: False - full house
    num = random_nums(2)
    hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    assert player.is_two_pair(hand) == False

    # Sanity checks - hardcoded numbers
    hand = create_hand([2,2,3,3,4], random_suits(5))
    assert player.is_two_pair(hand) == True

    hand= create_hand([2,2,2,4,4], random_suits(5))
    assert player.is_two_pair(hand) == False

def test_is_one_pair(player: Player):
    # scenario 1: True
    num = random_nums(4)
    hand = create_hand([num[0]]*2 + [num[1]] + [num[2]] + [num[3]], random_suits(5))
    assert player.is_one_pair(hand) == True

    # scenario 2: False - 2 pairs
    num = random_nums(3)
    hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    assert player.is_one_pair(hand) == False

    # scenario 3: False = full house
    num = random_nums(2)
    hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    assert player.is_one_pair(hand) == False

    # scenario 4: False - three of a kind
    num = random_nums(3)
    hand = create_hand([num[0]]*3 + [num[1]] + [num[2]], random_suits(5))
    assert player.is_one_pair(hand) == False

    # Sanity checks - hardcoded numbers
    hand = create_hand([2,2,3,4,5], random_suits(5))
    assert player.is_one_pair(hand) == True

    hand = create_hand([2,2,3,3,4], random_suits(5))
    assert player.is_one_pair(hand) == False

    hand= create_hand([2,2,2,4,4], random_suits(5))
    assert player.is_one_pair(hand) == False

    hand= create_hand([2,2,2,4,5], random_suits(5))
    assert player.is_one_pair(hand) == False

def test_is_high_card(player: Player):
    # scenario 1: True
    hand = create_hand([2,3,4,5,8], random_suits(5))
    assert player.is_high_card(hand) == True

    # scenario 2: False - flush
    hand = create_hand([2,3,4,5,8], random_suits(1)*5)
    assert player.is_high_card(hand) == False

    # scenario 2: Fals - consecutive number combo
    hand = create_hand([4,5,6,7,8], random_suits(5))
    assert player.is_high_card(hand) == False

# endregion check combo method
    
# region calc total number of combinations
# https://en.wikipedia.org/wiki/Poker_probability
# https://www.youtube.com/playlist?list=PL6ZxDcgthxgLWbRPb_x3u_r_260FOsfjO

def test_calc_total_combination(player: Player):
    # You need to think about the same hand not being double counted for example: drawing (4Heart, 5Heart) is the same as (5Heart, 4Heart) 
    # Mathematically, I care about combination not permutation
    
    # scenario 1: 0 
    assert player.calc_total_combination(0) == 1

    # scenario 2: 1
    assert player.calc_total_combination(1) == 48

    # scenario 3: 2 
    assert player.calc_total_combination(2) == (49 * 48) // math.factorial(2)

    # scenario 4: 3
    assert player.calc_total_combination(3) == (50 * 49 * 48) // math.factorial(3)

    # scenario 5: 4
    assert player.calc_total_combination(4) == (51 * 50 * 49 * 48) // math.factorial(4)

    # scenario 6: 5
    assert player.calc_total_combination(5) == (52 * 51 * 50 * 49 * 48) // math.factorial(5)

    # Sanity checks
    assert player.calc_total_combination(5) == 2598960

def test_calc_royal_flush_total_combination(player: Player):
    # find all royal flush combo
    all_royal_flush = []
    suits = ["♠️", "♥️", "♣️", "♦️"]
    val = [10,11,12,13,14]
    for suit in suits:
        one_royal_flush = []
        for num in val:
            one_royal_flush.append(Card(suit, num))
        all_royal_flush.append(one_royal_flush)

    # scenario 1: mulligan 5
    assert player.calc_royal_flush_total_combination([]) == len(all_royal_flush)

    # scenario 2: retain hand has 1 possibilities
    retained_hand = create_hand([10,11], random_suits(1)*2)
    all_valid_combination = hand_in_valid_combination(retained_hand, all_royal_flush)
    assert player.calc_royal_flush_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 3: retain hand has no possibilities
    retained_hand = create_hand([9,13], random_suits(1)*2)
    all_valid_combination = hand_in_valid_combination(retained_hand, all_royal_flush)
    assert player.calc_royal_flush_total_combination(retained_hand) == len(all_valid_combination)

    # Test
    all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_royal_flush)
    assert player.calc_royal_flush_total_combination(TEST_RETAINED_HAND) == len(all_valid_combination)

def test_calc_straight_flush_total_combination(player: Player):
    # find all straight flush combo
    all_straight_flush = all_iter_consecutive_combination(flush=True, royal=False)

    # scenario 1: mulligan 5
    assert player.calc_straight_flush_total_combination([]) == len(all_straight_flush)

    # scenario 2: possible straight flush - edge
    retained_hand = create_hand([11,12,13], random_suits(1)*3) 
    all_valid_combination = hand_in_valid_combination(retained_hand, all_straight_flush)
    assert player.calc_straight_flush_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 2: possible straight flush - mid
    retained_hand = create_hand([9], random_suits(1))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_straight_flush)
    assert player.calc_straight_flush_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 3: royal flush
    retained_hand = create_hand([10,11,12,13,14], random_suits(1)*5)
    all_valid_combination = hand_in_valid_combination(retained_hand, all_straight_flush)
    assert player.calc_straight_flush_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 4: no straight flush by number list
    retained_hand = create_hand([2,5,10], random_suits(1)*5)
    all_valid_combination = hand_in_valid_combination(retained_hand, all_straight_flush)
    assert player.calc_straight_flush_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 5: no straight flush by suit
    retained_hand = create_hand([12,13], random_suits(2))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_straight_flush)
    assert player.calc_straight_flush_total_combination(retained_hand) == len(all_valid_combination)

    # Sanity check: - excluding steel wheel (A-2-3-4-5)
    assert player.calc_straight_flush_total_combination([]) == 36 - 4

    # Test
    all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_straight_flush)
    assert player.calc_straight_flush_total_combination(TEST_RETAINED_HAND) == len(all_valid_combination)   

def test_calc_four_of_a_kind_total_combination(player: Player):
    # find all 4 of a kind combo
    all_four_of_a_kind = []
    quad_combo = all_iter_combination(num_list=range(2,15), count=4)

    for quad in quad_combo:
        num = quad[0].value
        num_list = list(range(2, 15))
        num_list.remove(num)
        singles = all_iter_combination(num_list=num_list, count=1)
        for single in singles:
            combination = quad + list(single)
            all_four_of_a_kind.append(combination)

    # scenario 1: mulligan 5
    assert player.calc_four_of_a_kind_total_combination([]) == len(all_four_of_a_kind)

    # scenario 2: XXXX retained hand
    retained_hand = create_hand(random_nums(1)*4, random_suits(4))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_four_of_a_kind)
    assert player.calc_four_of_a_kind_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 3: XXXY retained hand
    num = random_nums(2)
    retained_hand = create_hand([num[0]]*3 + [num[1]], random_suits(4))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_four_of_a_kind)
    assert player.calc_four_of_a_kind_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 4: XXY retained hand
    num = random_nums(2)
    retained_hand = create_hand([num[0]]*2 + [num[1]], random_suits(3))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_four_of_a_kind)
    assert player.calc_four_of_a_kind_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 5: XXX retained hand
    retained_hand = create_hand(random_nums(1)*3, random_suits(3))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_four_of_a_kind)
    assert player.calc_four_of_a_kind_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 6: XX retained hand
    retained_hand = create_hand(random_nums(1)*2, random_suits(2))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_four_of_a_kind)
    assert player.calc_four_of_a_kind_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 7: XY retained hand
    retained_hand = create_hand([num[0]] + [num[1]], random_suits(2))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_four_of_a_kind)
    assert player.calc_four_of_a_kind_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 8: X 1x quad in retained hand
    retained_hand = create_hand(random_nums(1), random_suits(1))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_four_of_a_kind)
    assert player.calc_four_of_a_kind_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 9: no full house possibilities with XYZ in retained hand
    num = random_nums(3)
    retained_hand = create_hand([num[0]] + [num[1]] + [num[2]], random_suits(3))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_four_of_a_kind)
    assert player.calc_four_of_a_kind_total_combination(retained_hand) == len(all_valid_combination)

    # Sanity check
    assert player.calc_four_of_a_kind_total_combination([]) == 624

    # Test
    all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_four_of_a_kind)
    assert player.calc_four_of_a_kind_total_combination(TEST_RETAINED_HAND) == len(all_valid_combination)

def test_calc_full_house_total_combination(player: Player):
    # find all full house combo
    all_full_house = []
    three_card_combo = all_iter_combination(num_list=range(2,15),count=3)

    for triple in three_card_combo:
        num = triple[0].value
        num_list = list(range(2, 15))
        num_list.remove(num)
        pairs = all_iter_combination(num_list=num_list, count=2)
        for pair in pairs:
            combination = triple + list(pair)
            all_full_house.append(combination)

    # scenario 1: mulligan 5
    assert player.calc_full_house_total_combination([]) == len(all_full_house)

    # scenario 2: 4 retained hand XXXY
    num = random_nums(2)
    retained_hand = create_hand([num[0]]*3 + [num[1]], random_suits(4))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    assert player.calc_full_house_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 3: 4 retained hand XXYY
    num = random_nums(2)
    retained_hand = create_hand([num[0]]*2 + [num[1]]*2, random_suits(4))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    assert player.calc_full_house_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 3: 4 retained hand XXX
    retained_hand = create_hand(random_nums(3), random_suits(3))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    assert player.calc_full_house_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 4: 3 retained hand XXY
    num = random_nums(2)
    retained_hand = create_hand([num[0]]*2 + [num[1]]*1, random_suits(3))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    assert player.calc_full_house_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 5: 2 retained hand XY
    retained_hand = create_hand(random_nums(2), random_suits(2))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    assert player.calc_full_house_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 6: 2 retained hand XX
    num = random_nums(2)
    retained_hand = create_hand(random_nums(1)*2, random_suits(2))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    assert player.calc_full_house_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 7 : 1 retained hand
    num = random_nums(2)
    retained_hand = create_hand(random_nums(1), random_suits(1))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    assert player.calc_full_house_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 8: no full house possibilities with XYZ in retained hand
    retained_hand = create_hand(random_nums(1)*3, random_suits(3))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    assert player.calc_full_house_total_combination(retained_hand) == len(all_valid_combination)

    # Sanity check
    assert player.calc_full_house_total_combination([]) == 3744

    # Test
    all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_full_house)
    assert player.calc_full_house_total_combination(TEST_RETAINED_HAND) == len(all_valid_combination)

def test_calc_flush_total_combination(player: Player):
    # find all flush combo
    all_flush = []
    # all combination of 5 number from 13 number
    all_combinations = list(itertools.combinations(range(2, 15), 5))
    # all straight combo - excluding steel wheel A-2-3-4-5
    consecutive_value_combos = [(i, i+1, i+2, i+3, i+4) for i in range(2, 11)]

    # all combination excluding straight and royal 
    all_valid_value_combination = [combo for combo in all_combinations if combo not in consecutive_value_combos]

    for combo in all_valid_value_combination:
        suits = ["♠️", "♥️", "♣️", "♦️"]
        for suit in suits:
            flush_combo = [Card(suit, value) for value in combo]
            all_flush.append(flush_combo)

    # scenario 1: mulligan 5 - exclude straight flush/royal flush
    assert player.calc_flush_total_combination([]) == len(all_flush)

    # scenario 2: keep cards in same suit
    retained_hand = create_hand(random_nums(3), random_suits(1)*3)
    all_valid_combination = hand_in_valid_combination(retained_hand, all_flush)
    assert player.calc_flush_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 3: no flush possibilities different suit
    retained_hand = create_hand(random_nums(2), random_suits(2))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_flush)
    assert player.calc_flush_total_combination(retained_hand) == len(all_valid_combination)

    # Sanity check
    # add back 4 because I am not counting steel wheel and steel wheel is counted in wiki and the YT video
    assert player.calc_flush_total_combination([]) == 5108 + 4

    # Test
    all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_flush)
    assert player.calc_flush_total_combination(TEST_RETAINED_HAND) == len(all_valid_combination)

def test_calc_straight_total_combination(player: Player):
    # find all straight combo
    all_straight_no_flush = all_iter_consecutive_combination(flush=False, royal=True)
    
    # scenario 1: mulligan 5 - exclude straight flush/royal flush
    assert player.calc_straight_total_combination([]) == len(all_straight_no_flush)
            
    # scenario 2: straight possibilities different suit - edge
    retained_hand = create_hand([12,13,14], random_suits(3))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_straight_no_flush)
    assert player.calc_straight_total_combination(retained_hand) == len(all_valid_combination) 

    # scenario 3: straight possibilities different suit - mid
    retained_hand = create_hand([6,7,8], random_suits(3))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_straight_no_flush)
    assert player.calc_straight_total_combination(retained_hand) == len(all_valid_combination) 

    # scenario 4: retained hand is same suit - exclude straight flush
    retained_hand = create_hand([6,7,8], random_suits(1)*3)
    all_valid_combination = hand_in_valid_combination(retained_hand, all_straight_no_flush)
    assert player.calc_straight_total_combination(retained_hand) == len(all_valid_combination) 

    # scenario 5: retained hand is same suit
    retained_hand = create_hand([10,11,12], random_suits(1)*3)
    all_valid_combination = hand_in_valid_combination(retained_hand, all_straight_no_flush)
    assert player.calc_straight_total_combination(retained_hand) == len(all_valid_combination) 

    # scenario 6: retained hand can't make straight
    retained_hand = create_hand([2,13], random_suits(2))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_straight_no_flush)
    assert player.calc_straight_total_combination(retained_hand) == len(all_valid_combination) 

    # Sanity check
    # remember that we are excluding steel wheel
    # (9/choose 1)(4/choose 1)^5 - (9/choose 1)(4/choose 1) == 9180
    assert player.calc_straight_total_combination([]) == 9180

    # Test
    all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_straight_no_flush)
    assert player.calc_straight_total_combination(TEST_RETAINED_HAND) == len(all_valid_combination) 

def test_calc_three_of_a_kind_total_combination(player: Player):
    # find all 3 of a kind combo
    num_list = list(range(2, 15))
    triple_list = all_iter_combination(3, num_list)
    all_three_of_a_kind = []
    
    for triple in triple_list:
        num_list = list(range(2,15))
        num_list.remove(triple[0].value)
        random_two = random_num_combination(count=2, num_list=num_list)
        for two_cards in random_two:
            all_three_of_a_kind.append(triple + list(two_cards))

    # scenario 1: mulligan 5 - exclude full house/four of a kind
    assert player.calc_three_of_a_kind_total_combination([]) == len(all_three_of_a_kind)

    # scenario 2: 4 retained hand XXXY - exclude full house/four of a kind
    num = random_nums(2)
    retained_hand = create_hand([num[0]]*3 + [num[1]], random_suits(4))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    assert player.calc_three_of_a_kind_total_combination(retained_hand) == len(all_valid_combination)
    
    # scenario 3: 3 retained hand XXY - exclude full house/four of a kind
    retained_hand = create_hand([num[0]]*2 + [num[1]], random_suits(3))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    assert player.calc_three_of_a_kind_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 4: 3 retained hand XXX - exclude full house/four of a kind
    retained_hand = create_hand(random_nums(1)*3, random_suits(3))
    all_valid_combination  = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    assert player.calc_three_of_a_kind_total_combination(retained_hand) == len(all_valid_combination)    
    
    # scenario 5: 3 retained hand XX - exclude full house/four of a kind
    retained_hand = create_hand(random_nums(1)*2, random_suits(2))
    all_valid_combination  = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    assert player.calc_three_of_a_kind_total_combination(retained_hand) == len(all_valid_combination)
    
    # scenario 6: 2 retained hand XY - exclude full house/four of a kind
    retained_hand = create_hand(random_nums(2), random_suits(2))
    all_valid_combination  = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    assert player.calc_three_of_a_kind_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 7: 1 retained hand X - exclude full house/four of a kind
    retained_hand = create_hand(random_nums(1), random_suits(1))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    assert player.calc_three_of_a_kind_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 8: 3 retained hand XYZ
    retained_hand = create_hand(random_nums(3), random_suits(3))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    assert player.calc_three_of_a_kind_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 9: no possibilities XXYY
    num = random_nums(2)
    retained_hand = create_hand([num[0]]*2 + [num[1]]*2, random_suits(4))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    assert player.calc_three_of_a_kind_total_combination(retained_hand) == len(all_valid_combination)

    # Sanity check
    assert player.calc_three_of_a_kind_total_combination([]) == 54912

    # Test
    all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_three_of_a_kind)
    assert player.calc_three_of_a_kind_total_combination(TEST_RETAINED_HAND) == len(all_valid_combination)

def test_calc_two_pairs_total_combination(player: Player):
    # find all two pairs combo
    all_two_pairs = []

    all_pairs = all_iter_combination(count=2, num_list=list(range(2,15)))

    all_only_two_pairs = itertools.combinations(all_pairs, 2)
    all_only_two_pairs_list = []
    for combo in all_only_two_pairs:
        flattened_combo = [card for sublist in combo for card in sublist]
        unique_values = set([card.value for card in flattened_combo])
        only_two_value = len(unique_values) == 2
        # only contains true pairs
        if only_two_value:
            all_only_two_pairs_list.append(flattened_combo)

    for combo in all_only_two_pairs_list:
        num_list = list(range(2,15))
        values = set([card.value for card in combo])
        for val in values:
            num_list.remove(val)
        random_num = random_num_combination(count=1, num_list=num_list)
        for num in random_num:
            all_two_pairs.append(combo + list(num))

    # scenario 1: mulligan 5 - exclude 4 of a kind/full house/3 of a kind
    assert player.calc_two_pairs_total_combination([]) == len(all_two_pairs)

    # scenario 2: 4 retained hand XXYZ
    num = random_nums(3)
    retained_hand = create_hand([num[0]]*2 + [num[1]] + [num[2]], random_suits(4))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    assert player.calc_two_pairs_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 3: 4 retained hand XXYY
    num = random_nums(2)
    retained_hand = create_hand([num[0]]*2 + [num[1]]*2, random_suits(4))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    assert player.calc_two_pairs_total_combination(retained_hand) == len(all_valid_combination)
    
    # scenario 4: 3 retained hand XXY - exclude 4 of a kind/full house/3 of a kind
    num = random_nums(2)
    retained_hand = create_hand([num[0]]*2 + [num[1]], random_suits(3))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    assert player.calc_two_pairs_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 5: 3 retained hand XYZ - exclude 3 of a kind
    retained_hand = create_hand(random_nums(3), random_suits(3))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    assert player.calc_two_pairs_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 6: 2 retained hand XX- exclude 4 of kind/full house/3 of a kind
    retained_hand = create_hand(random_nums(1)*2, random_suits(2))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    assert player.calc_two_pairs_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 7: 2 retained hand XY- exclude 4 of a kind/full house/3 of a kind
    retained_hand = create_hand(random_nums(2), random_suits(2))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    assert player.calc_two_pairs_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 8: 1 retained hand X - exclude 4 of a kind/full house/3 of a kind
    retained_hand = create_hand(random_nums(1), random_suits(1))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    assert player.calc_two_pairs_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 9: no possibilities XXX
    retained_hand = create_hand(random_nums(1)*3, random_suits(3))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    assert player.calc_two_pairs_total_combination(retained_hand) == len(all_valid_combination)

    # Sanity check
    assert player.calc_two_pairs_total_combination([]) == 123552

    # Test
    all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_two_pairs)
    assert player.calc_two_pairs_total_combination(TEST_RETAINED_HAND) == len(all_valid_combination)

def test_calc_one_pair_total_combination(player: Player):
    # find all 1 pair combo
    all_one_pair = []
    num_list = list(range(2,15))
    pairs = all_iter_combination(count=2, num_list=num_list)

    for pair in pairs:
        num_list = list(range(2,15))
        num_list.remove(pair[0].value)
        random_num = random_num_combination(count=3, num_list=num_list)
        for num in random_num:
            all_one_pair.append(pair + list(num))

    # scenario 1: mulligan 5- exclude 4 of a kind/full house/3 of a kind/2 pairs
    assert player.calc_one_pair_total_combination([]) == len(all_one_pair)

    # scenario 2: XYZA
    retained_hand = create_hand(random_nums(4), random_suits(4))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    assert player.calc_one_pair_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 3: XXYZ
    num = random_nums(3)
    retained_hand = create_hand([num[0]]*2 + [num[1]] + [num[2]], random_suits(4))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    assert player.calc_one_pair_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 4: XXY
    num = random_nums(2)
    retained_hand = create_hand([num[0]]*2 + [num[1]], random_suits(3))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    assert player.calc_one_pair_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 5: XYZ
    retained_hand = create_hand(random_nums(3), random_suits(3))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    assert player.calc_one_pair_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 6: 2 retained hand XX- exclude 4 of a kind/full house/3 of a kind/2 pairs
    retained_hand = create_hand(random_nums(1)*2, random_suits(2))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    assert player.calc_one_pair_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 7: 2 retained hand XY- exclude 4 of a kind/full house/3 of a kind/2 pairs
    retained_hand = create_hand(random_nums(2), random_suits(2))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    assert player.calc_one_pair_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 8: 1 retained hand X - exclude 4 of a kind/full house/3 of a kind/2 pairs
    retained_hand = create_hand(random_nums(1), random_suits(1))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    assert player.calc_one_pair_total_combination(retained_hand) == len(all_valid_combination)

    # scenario 9: no possibilities - 4 of a kind
    hand = create_hand(random_nums(1)*4, random_suits(4))
    all_valid_combination = hand_in_valid_combination(hand, all_one_pair)
    assert player.calc_one_pair_total_combination(hand) == len(all_valid_combination)

    # scenario 10: no possibilities - 3 of a kind
    hand = create_hand(random_nums(1)*3, random_suits(3))
    all_valid_combination = hand_in_valid_combination(hand, all_one_pair)
    assert player.calc_one_pair_total_combination(hand) == len(all_valid_combination)

    # scenario 11: no possibilities - 2 pairs
    num = random_nums(2)
    hand = create_hand([num[0]]*2 + [num[1]]*2, random_suits(2) + random_suits(2))
    all_valid_combination = hand_in_valid_combination(hand, all_one_pair)
    assert player.calc_one_pair_total_combination(hand) == len(all_valid_combination)

    # Sanity check
    assert player.calc_one_pair_total_combination([]) == 1098240

    # Test
    all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_one_pair)
    assert player.calc_one_pair_total_combination(TEST_RETAINED_HAND) == len(all_valid_combination)

# endregion check total number of combinations

# region calc better combo if hand is already a given combo
def test_calc_total_better_royal_flush_combination(player: Player):
    # scenario 1: royal flush
    given_hand = create_hand([10,11,12,13,14], random_suits(1)*5)
    retained_hand = []
    assert player.calc_total_better_royal_flush_combination(given_hand, retained_hand) == 0

    # scenario 2: not royal flush
    given_hand = create_hand([9,10,11,12,13], random_suits(1)*5)
    retained_hand = []
    assert player.calc_total_better_royal_flush_combination(given_hand, retained_hand) == 0

    # Test
    if player.is_royal_flush(TEST_GIVEN_HAND):
        assert player.calc_total_better_royal_flush_combination(TEST_GIVEN_HAND, TEST_RETAINED_HAND) == 0
    
def test_calc_total_better_straight_flush_combination(player: Player):
    # helper function to find combo that is BETTER than given hand
    def find_better_combo(given_hand, all_valid_combo, print_result=False):
        output = []

        for combo in all_valid_combo:
            max_given_val = max([card.value for card in given_hand])
            max_combo_val = max([card.value for card in combo])
            same_suit = player.is_same_suit(given_hand)
            if max_combo_val > max_given_val and same_suit:
                output.append(combo)
        
        if print_result:
            for combo in output:
                print([str(card) for card in combo])

        return output

    # find all straight flush combo
    all_straight_flush = all_iter_consecutive_combination(flush=True, royal=False)

    for combo in all_straight_flush:
        print([str(card) for card in combo])

    # scenario 1: worst straight flush - 2-3-4-5-6 - no retained_hand
    given_hand = create_hand([2,3,4,5,6], random_suits(1)*5)
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_straight_flush)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_straight_flush_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 2: worst straight flush - 2-3-4-5-6 - card in retained_hand
    given_hand = create_hand([2,3,4,5,6], random_suits(1)*5)
    retained_hand = given_hand[2:4]
    print(f"given_hand: {[str(card) for card in given_hand]}")
    print(f"retained_hand: {[str(card) for card in retained_hand]}")
    all_valid_combination = hand_in_valid_combination(retained_hand, all_straight_flush)
    all_better_combination = find_better_combo(given_hand, all_valid_combination, print_result=True)
    assert player.calc_total_better_straight_flush_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 3: best straight flush - 9-10-J-Q-K - no better straight flush
    given_hand = create_hand([9,10,11,12,13], random_suits(1)*5)
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_straight_flush)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_straight_flush_combination(given_hand, retained_hand) == len(all_better_combination)

    # Test
    if player.is_straight_flush(TEST_GIVEN_HAND):
        all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_straight_flush)
        all_better_combination = find_better_combo(TEST_GIVEN_HAND, all_valid_combination)
        assert player.calc_total_better_straight_flush_combination(TEST_GIVEN_HAND, TEST_RETAINED_HAND) == len(all_better_combination)

def test_calc_total_better_four_of_a_kind_combination(player: Player):
    # helper function to find combo that is BETTER than given hand
    def find_better_combo(given_hand, all_valid_combo, print_result=False):
        output = []

        # find quad or kicker
        given_quad = None
        given_kicker = None
        given_values = [card.value for card in given_hand]
        for val in set(given_values):
            if given_values.count(val) == 4:
                given_quad = val
            if given_values.count(val) == 1:
                given_kicker = val

        for combo in all_valid_combo:
            combo_quad = None
            combo_kicker = None
            value = [card.value for card in combo]
            for val in set(value):
                if value.count(val) == 4:
                    combo_quad = val
                else:
                    combo_kicker = val

            if combo_quad > given_quad:
                output.append(combo)
            elif combo_quad == given_quad and combo_kicker > given_kicker:
                output.append(combo)
        
        if print_result:
            for combo in output:
                print([str(card) for card in combo])

        return output

    # find all 4 of a kind combo
    all_four_of_a_kind = []
    quad_combo = all_iter_combination(num_list=range(2,15), count=4)

    for quad in quad_combo:
        num = quad[0].value
        num_list = list(range(2, 15))
        num_list.remove(num)
        singles = all_iter_combination(num_list=num_list, count=1)
        for single in singles:
            combination = quad + list(single)
            all_four_of_a_kind.append(combination)

    # scenario 1: worst 4 of a kind 2-2-2-2-3 - no card in retained hand
    given_hand = create_hand([2,2,2,2,3], random_suits(5))
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_four_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_four_of_a_kind)
    assert player.calc_total_better_four_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 2: best 4 of a kind A-A-A-A-K - no card in retained hand
    given_hand = create_hand([14,14,14,14,13], random_suits(5))
    all_valid_combination = hand_in_valid_combination(retained_hand, all_four_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_four_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 3: retained quad in hand XXXX
    num = random_nums(2)
    given_hand = create_hand([num[0]]*4 + [num[1]], random_suits(5))
    retained_hand = given_hand[0:4]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_four_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_four_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 4: retained XXY
    num = random_nums(2)
    given_hand = create_hand([num[0]]*4 + [num[1]], random_suits(5))
    retained_hand = given_hand[-3:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_four_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_four_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 5: retained XY - Y > X
    num = random_nums(2)
    num.sort()
    given_hand = create_hand([num[0]]*4 + [num[1]], random_suits(5))
    retained_hand = given_hand[-2:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_four_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_four_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 6: retained XY - X > Y
    num = random_nums(2)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*4 + [num[1]], random_suits(5))
    retained_hand = given_hand[-2:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_four_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_four_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 7: retained kicker Y - Y > X
    num = random_nums(2)
    num.sort()
    given_hand = create_hand([num[0]]*4 + [num[1]], random_suits(5))
    retained_hand = [given_hand[-1]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_four_of_a_kind)
    all_better_combination = find_better_combo(given_hand,all_valid_combination)
    assert player.calc_total_better_four_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 8: retained kicker Y - X > Y
    num = random_nums(2)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*4 + [num[1]], random_suits(5))
    retained_hand = [given_hand[-1]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_four_of_a_kind)
    all_better_combination = find_better_combo(given_hand,all_valid_combination)
    assert player.calc_total_better_four_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 9: retained 1x quad X - Y > X
    num = random_nums(2)
    num.sort()
    given_hand = create_hand([num[0]]*4 + [num[1]], random_suits(5))
    retained_hand = [given_hand[0]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_four_of_a_kind)
    all_better_combination = find_better_combo(given_hand,all_valid_combination)
    assert player.calc_total_better_four_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 10: retained 1x quad X - X > Y
    num = random_nums(2)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*4 + [num[1]], random_suits(5))
    retained_hand = [given_hand[0]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_four_of_a_kind)
    all_better_combination = find_better_combo(given_hand,all_valid_combination)
    assert player.calc_total_better_four_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # Test
    if player.is_four_of_a_kind(TEST_GIVEN_HAND):
        all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_four_of_a_kind)
        all_better_combination = find_better_combo(TEST_GIVEN_HAND ,all_valid_combination)
        assert player.calc_total_better_four_of_a_kind_combination(TEST_GIVEN_HAND, TEST_RETAINED_HAND) == len(all_better_combination)

def test_calc_total_better_full_house_combination(player: Player):
    # helper function to find combo that is BETTER than given hand
    def find_better_combo(given_hand, all_valid_combo, print_result=False):
        output = []

        # setup
        given_triple = None
        given_pair = None
        given_values = [card.value for card in given_hand]
        for val in set(given_values):
            if given_values.count(val) == 3:
                given_triple = val
            if given_values.count(val) == 2:
                given_pair = val

        for combo in all_valid_combo:
            combo_triple = None
            combo_pair = None
            value = [card.value for card in combo]
            for val in set(value):
                if value.count(val) == 3:
                    combo_triple = val
                else:
                    combo_pair = val

            if combo_triple > given_triple:
                output.append(combo)
            elif combo_triple == given_triple and combo_pair > given_pair:
                output.append(combo)
        
        if print_result:
            for combo in output:
                print([str(card) for card in combo])

        return output

    # find all full house combo
    all_full_house = []
    three_card_combo = all_iter_combination(num_list=range(2,15),count=3)

    for triple in three_card_combo:
        num = triple[0].value
        num_list = list(range(2, 15))
        num_list.remove(num)
        pairs = all_iter_combination(num_list=num_list, count=2)
        for pair in pairs:
            combination = triple + list(pair)
            all_full_house.append(combination)

    # scenario 1: worst full house 2-2-2-3-3 - no retained hand
    given_hand = create_hand([2,2,2,3,3], random_suits(5))
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_full_house_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 2: best full house A-A-A-K-K - no retained hand
    given_hand = create_hand([14,14,14,13,13], random_suits(5))
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_full_house_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 3: keep 2x of each card - XXYY - X > Y
    num = random_nums(2)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    retained_hand = given_hand[1:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_full_house_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 4: keep 2x of each card - XXYY - Y > X
    num = random_nums(2)
    num.sort()
    given_hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    retained_hand = given_hand[1:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_full_house_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 5: keep triple + 1x pair- XXXY
    num = random_nums(2)
    given_hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    retained_hand = given_hand[:-1]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_full_house_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 6: keep triple XXX
    num = random_nums(2)
    given_hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    retained_hand = given_hand[:3]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_full_house_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 7 - XYY or XXY - X > Y
    num = random_nums(2)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    retained_hand = given_hand[1:4]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_full_house_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 8: - XYY or XXY Y > X
    num = random_nums(2)
    num.sort()
    given_hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    retained_hand = given_hand[1:4]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_full_house_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 9: keep 2 quad XX - X > Y
    num = random_nums(2)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    retained_hand = given_hand[:2]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_full_house_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 10: keep 2 quad XX - Y > X
    num = random_nums(2)
    num.sort()
    given_hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    retained_hand = given_hand[:2]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_full_house_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 11: keep pair YY - X > Y
    num = random_nums(2)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    retained_hand = given_hand[-2:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_full_house_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 12: keep pair YY - Y > X
    num = random_nums(2)
    num.sort()
    given_hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    retained_hand = given_hand[-2:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_full_house_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 13: keep XY - X > Y
    num = random_nums(2)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    retained_hand = given_hand[2:4]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_full_house_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 14: keep XY - Y > X
    num = random_nums(2)
    num.sort()
    given_hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    retained_hand = given_hand[2:4]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_full_house_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 15: keep 1x triple card X - X > Y
    num = random_nums(2)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    retained_hand = [given_hand[0]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_full_house_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 16: keep 1x triple card X - Y > X
    num = random_nums(2)
    num.sort()
    given_hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    retained_hand = [given_hand[0]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_full_house_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 17: keep 1x pair card Y - X > Y
    num = random_nums(2)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    retained_hand = [given_hand[-1]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_full_house_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 18: keep 1x pair card Y - Y > X
    num = random_nums(2)
    num.sort()
    given_hand = create_hand([num[0]]*3 + [num[1]]*2, random_suits(5))
    retained_hand = [given_hand[-1]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_full_house)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_full_house_combination(given_hand, retained_hand) == len(all_better_combination)

    # Test
    if player.is_full_house(TEST_GIVEN_HAND):
        all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_full_house)
        all_better_combination = find_better_combo(TEST_GIVEN_HAND, all_valid_combination)
        assert player.calc_total_better_full_house_combination(TEST_GIVEN_HAND, TEST_RETAINED_HAND) == len(all_better_combination)

def test_calc_total_better_flush_combination(player: Player):
    # helper function to find combo that is BETTER than given hand
    def find_better_combo(given_hand, all_valid_combo, print_result=False):
        output = []
        given_hand_value = [card.value for card in given_hand]
        given_hand_value.sort(reverse=True)

        for combo in all_valid_combo:
            combo_value = [card.value for card in combo]
            combo_value.sort(reverse=True)

            for i in range(5):
                if combo_value[i] > given_hand_value[i]:
                    output.append(combo)
                    break
                if combo_value[i] < given_hand_value[i]:
                    break

        if print_result:
            for combo in output:
                str_combo = [str(card) for card in combo]
                print(str_combo)

        return output

    # find all flush combo
    all_flush = []
    # all combination of 5 number from 13 number
    all_combinations = list(itertools.combinations(range(2, 15), 5))
    # all straight combo - excluding steel wheel A-2-3-4-5
    consecutive_value_combos = [(i, i+1, i+2, i+3, i+4) for i in range(2, 11)]

    # all combination excluding straight and royal 
    all_valid_value_combination = [combo for combo in all_combinations if combo not in consecutive_value_combos]

    for combo in all_valid_value_combination:
        suits = ["♠️", "♥️", "♣️", "♦️"]
        for suit in suits:
            flush_combo = [Card(suit, value) for value in combo]
            all_flush.append(flush_combo)

    # scenario 1: best flush - no retained hand
    given_hand = create_hand([14,13,12,11,9], random_suits(1)*5)
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_flush)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_flush_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 2: worst flush - no retained hand
    given_hand = create_hand([2,3,4,5,7], random_suits(1)*5)
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_flush)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_flush_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 3: no retained hand
    given_hand = create_hand([2,4,7,9,14], random_suits(1)*5)
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_flush)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_flush_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 4: retained card
    given_hand = create_hand([2,4,7,9,14], random_suits(1)*5)
    retained_hand = [given_hand[0]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_flush)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_flush_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 5: retained card can make straight flush
    given_hand = create_hand([5,6,7,8,10], random_suits(1)*5)
    retained_hand = given_hand[:2]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_flush)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_flush_combination(given_hand, retained_hand) == len(all_better_combination)

    # Test
    if player.is_flush(TEST_GIVEN_HAND):
        all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_flush)
        all_better_combination = find_better_combo(TEST_GIVEN_HAND, all_valid_combination)
        assert player.calc_total_better_flush_combination(TEST_GIVEN_HAND, TEST_RETAINED_HAND) == len(all_better_combination)

def test_calc_total_better_straight_combination(player: Player):
    def find_better_combo(given_hand, all_valid_combo, print_result=False):
        output = []
        for combo in all_valid_combo:
            max_given_val = max([card.value for card in given_hand])
            max_combo_val = max([card.value for card in combo])
            if max_combo_val > max_given_val:
                output.append(combo)
        
        if print_result:
            for combo in output:
                str_combo = [str(card) for card in combo]
                print(str_combo)
        
        return output
    # all straight combo
    all_straight_no_flush = all_iter_consecutive_combination(flush=False, royal=True)

    # scenario 1: best straight - no card in retained hand - 10-J-Q-K-A
    given_hand = create_hand([10,11,12,13,14], random_suits(4) + random_suits(1))
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_straight_no_flush)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_straight_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 2: worst straight - no card in retained hand - 2-3-4-5-6
    given_hand = create_hand([2,3,4,5,6], random_suits(4) + random_suits(1))
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_straight_no_flush)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_straight_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 3: mid straight - no card in retained hand
    given_hand = create_hand([5,6,7,8,9], random_suits(4) + random_suits(1))
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_straight_no_flush)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_straight_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 4: straight - retained_card
    given_hand = create_hand([7,8,9,10,11], random_suits(4) + random_suits(1))
    retained_hand = [given_hand[0]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_straight_no_flush)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_straight_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 4: straight - retained_card that are same suit
    given_hand = create_hand([7,8,9,10,11], ["♠️", "♠️", "♠️", "♠️", "♠️"])
    retained_hand = [given_hand[0]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_straight_no_flush)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_straight_combination(given_hand, retained_hand) == len(all_better_combination)

    # Test
    if player.is_straight(TEST_GIVEN_HAND):
        all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_straight_no_flush)
        all_better_combination = find_better_combo(TEST_GIVEN_HAND, all_valid_combination)
        assert player.calc_total_better_straight_combination(TEST_GIVEN_HAND, TEST_RETAINED_HAND) == len(all_better_combination)

def test_calc_total_better_three_of_a_kind_combination(player: Player):
    # helper function to find combo that is BETTER than given hand
    def find_better_combo(given_hand, all_valid_combo, print_result=False):
        output = []

        # setup
        given_triple = None
        given_kicker_list = []
        given_values = [card.value for card in given_hand]

        for val in set(given_values):
            if given_values.count(val) == 3:
                given_triple = val
            if given_values.count(val) == 1:
                given_kicker_list.append(val)

        given_kicker_list.sort(reverse=True)

        for combo in all_valid_combo:
            # find each combo's triple and kicker val
            combo_triple = None
            combo_kicker = []
            combo_values = [card.value for card in combo]
            for val in set(combo_values):
                if combo_values.count(val) == 3:
                    combo_triple = val
                if combo_values.count(val) == 1:
                    combo_kicker.append(val)

            combo_kicker.sort(reverse=True)

            # compare to find BETTER combo
            if combo_triple > given_triple:
                output.append(combo)
            if combo_triple == given_triple:
                for i in range(2):
                    if combo_kicker[i] > given_kicker_list[i]:
                        output.append(combo)
                        break
                    if combo_kicker[i] < given_kicker_list[i]:
                        break

        if print_result:
            for combo in output:
                str_combo = [str(card) for card in combo]
                print(str_combo)
        
        return output

    # find all 3 of a kind combo
    num_list = list(range(2, 15))
    triple_list = all_iter_combination(3, num_list)
    all_three_of_a_kind = []
    
    for triple in triple_list:
        num_list = list(range(2,15))
        num_list.remove(triple[0].value)
        random_two = random_num_combination(count=2, num_list=num_list)
        for two_cards in random_two:
            all_three_of_a_kind.append(triple + list(two_cards))

    # scenario 1: best - three of a kind - no card in retained hand - A-A-A-K-Q
    given_hand = create_hand([14,14,14,13,12], random_suits(5))
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 2: worst three of a kind - no card in retained hand - 2-2-2-3-4
    given_hand = create_hand([14,14,14,12,11], random_suits(5))
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 3: XXXY retained hand
    num = random_nums(3)
    given_hand = create_hand([num[0]]*3 + [num[1]] + [num[2]], random_suits(5))
    retained_hand = given_hand[:-1]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 4: XXYZ
    num = random_nums(3)
    given_hand = create_hand([num[0]]*3 + [num[1]] + [num[2]], random_suits(5))
    retained_hand = given_hand[1:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 5: XXX retained hand
    num = random_nums(3)
    given_hand = create_hand([num[0]]*3 + [num[1]] + [num[2]], random_suits(5))
    retained_hand = given_hand[:-2]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 6: XXY or XXZ retained hand
    num = random_nums(3)
    given_hand = create_hand([num[0]]*3 + [num[1]] + [num[2]], random_suits(5))
    retained_hand = given_hand[1:4]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 7: XYZ retained hand X > Y > Z
    num = random_nums(3)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*3 + [num[1]] + [num[2]], random_suits(5))
    retained_hand = given_hand[2:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 8: XYZ retained hand - Z > Y > X
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[0]]*3 + [num[1]] + [num[2]], random_suits(5))
    retained_hand = given_hand[2:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 9: XYZ retained hand - Y > X > Z
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[1]]*3 + [num[0]] + [num[2]], random_suits(5))
    retained_hand = given_hand[2:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 10: XX retained hand
    num = random_nums(3)
    given_hand = create_hand([num[0]]*3 + [num[1]] + [num[2]], random_suits(5))
    retained_hand = given_hand[:2]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 11: XY or XZ retained hand - X > Y or X > Z
    num = random_nums(3)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*3 + [num[1]] + [num[2]], random_suits(5))
    retained_hand = given_hand[2:4]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 12: XY or XZ retained hand - Y > X or Z > X
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[0]]*3 + [num[1]] + [num[2]], random_suits(5))
    retained_hand = given_hand[2:4]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 13: YZ retained hand - X > Y > Z
    num = random_nums(3)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*3 + [num[1]] + [num[2]], random_suits(5))
    retained_hand = given_hand[3:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 14: YZ retained hand - Z > Y > X
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[0]]*3 + [num[1]] + [num[2]], random_suits(5))
    retained_hand = given_hand[3:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)  
    
    # scenario 15: X retained hand - X > Y > Z
    num = random_nums(3)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*3 + [num[1]] + [num[2]], random_suits(5))
    retained_hand = [given_hand[0]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 16: X retained hand - Z > Y > X
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[0]]*3 + [num[1]] + [num[2]], random_suits(5))
    retained_hand = [given_hand[0]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 17: X retained hand - Y > X > Z
    num = random_nums(3)
    num.sort(reverse=True)
    given_hand = create_hand([num[1]]*3 + [num[0]] + [num[2]], random_suits(5))
    retained_hand = [given_hand[0]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 18: Y or Z retained hand - X > Y/Z
    num = random_nums(3)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*3 + [num[1]] + [num[2]], random_suits(5))
    retained_hand = [given_hand[-1]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 19: Y or Z retained hand - Z/Y > X
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[0]]*3 + [num[1]] + [num[2]], random_suits(5))
    retained_hand = [given_hand[-1]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_three_of_a_kind)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_three_of_a_kind_combination(given_hand, retained_hand) == len(all_better_combination)

    # Test
    if player.is_three_of_a_kind(TEST_GIVEN_HAND):
        all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_three_of_a_kind)
        all_better_combination = find_better_combo(TEST_GIVEN_HAND, all_valid_combination)
        assert player.calc_total_better_three_of_a_kind_combination(TEST_GIVEN_HAND, TEST_RETAINED_HAND) == len(all_better_combination)

def test_calc_total_better_two_pairs_combination(player: Player):
    # helper function to find combo that is BETTER than given hand
    def find_better_combo(given_hand, all_valid_combo, print_result=False):
        output = []

        # Setup
        given_pairs_list = []
        given_kicker = None
        given_values = [card.value for card in given_hand]

        for val in set(given_values):
            if given_values.count(val) == 2:
                given_pairs_list.append(val)
            if given_values.count(val) == 1:
                given_kicker = val

        given_pairs_list.sort(reverse=True)

        for combo in all_valid_combo:
            # find pair and kicker value for each combo
            combo_pairs_list = []
            combo_kicker = None
            combo_values = [card.value for card in combo]
            for val in set(combo_values):
                if combo_values.count(val) == 2:
                    combo_pairs_list.append(val)
                if combo_values.count(val) == 1:
                    combo_kicker = val

            combo_pairs_list.sort(reverse=True)

            if max(combo_pairs_list) > max(given_pairs_list):
                output.append(combo)
            elif max(combo_pairs_list) == max(given_pairs_list):
                if min(combo_pairs_list) > min(given_pairs_list):
                    output.append(combo)
                elif min(combo_pairs_list) == min(given_pairs_list) and combo_kicker > given_kicker:
                    output.append(combo)

        if print_result:
            for combo in output:
                str_combo = [str(card) for card in combo]
                print(str_combo)

        return output

    # all two pairs combinations
    all_two_pairs = []

    all_pairs = all_iter_combination(count=2, num_list=list(range(2,15)))

    all_only_two_pairs = itertools.combinations(all_pairs, 2)
    all_only_two_pairs_list = []
    for combo in all_only_two_pairs:
        flattened_combo = [card for sublist in combo for card in sublist]
        unique_values = set([card.value for card in flattened_combo])
        only_two_value = len(unique_values) == 2
        # only contains true pairs
        if only_two_value:
            all_only_two_pairs_list.append(flattened_combo)

    for combo in all_only_two_pairs_list:
        num_list = list(range(2,15))
        values = set([card.value for card in combo])
        for val in values:
            num_list.remove(val)
        random_num = random_num_combination(count=1, num_list=num_list)
        for num in random_num:
            all_two_pairs.append(combo + list(num))

    assert len(all_two_pairs) == 123552

    # scenario 1: best 2 pairs - no retained hand
    given_hand = create_hand([14,14,13,13,12], random_suits(5))
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 2: worst 2 pairs - no retained hand
    given_hand = create_hand([2,2,3,3,4], random_suits(5))
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)
    
    # scenario 3: XXYY retained hand
    num = random_nums(3)
    given_hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    retained_hand = given_hand[:-1]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 4: XXYZ or XYYZ retained hand
    num = random_nums(3)
    given_hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    retained_hand = given_hand[1:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 5: XXY retained hand
    num = random_nums(3)
    given_hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    retained_hand = given_hand[:3]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 6: XXZ retained hand Z > X
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    retained_hand = given_hand[:2] + [given_hand[-1]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 7: XXZ retained hand X > Z
    num = random_nums(3)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    retained_hand = given_hand[:2] + [given_hand[-1]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 8: XYZ retained hand - Z > X/Y
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    retained_hand = given_hand[1:3] + [given_hand[-1]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 9: XYZ retained hand - X/Y > Z
    num = random_nums(3)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    retained_hand = given_hand[1:3] + [given_hand[-1]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 10: XYZ retained hand - X > Z > Y
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[1]]*2 + [num[0]]*2 + [num[2]], random_suits(5))
    retained_hand = given_hand[1:3] + [given_hand[-1]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 11: XX retained hand Z > X/X
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    retained_hand = given_hand[:2]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 12: XX retained hand X/Y > Z
    num = random_nums(3)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    retained_hand = given_hand[:2]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 13: XX retained hand X > Z > Y
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[1]]*2 + [num[0]]*2 + [num[2]], random_suits(5))
    retained_hand = given_hand[:2]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 14: XY retained hand Z > X/Y
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    retained_hand = given_hand[1:3]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 15: XY retained hand X/Y > Z
    num = random_nums(3)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    retained_hand = given_hand[1:3]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 16: XY retained hand X > Z > Y
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[1]]*2 + [num[0]]*2 + [num[2]], random_suits(5))
    retained_hand = given_hand[1:3]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 17: XZ/YZ retained hand - Z > X/Y
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    retained_hand = given_hand[-2:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 18: XZ/YZ retained hand - X/Y > Z
    num = random_nums(3)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    retained_hand = given_hand[-2:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 19: XZ/YZ retained hand - X > Z > Y
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[1]]*2 + [num[0]]*2 + [num[2]], random_suits(5))
    retained_hand = given_hand[-2:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 20: X/Y retained hand - Z > X/Y
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    retained_hand = [given_hand[0]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 21: X/Y retained hand - X/Y > Z
    num = random_nums(3)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    retained_hand = [given_hand[0]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 22: X/Y retained hand - X > Z > Y
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[1]]*2 + [num[0]]*2 + [num[2]], random_suits(5))
    retained_hand = [given_hand[0]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 23: Z retained hand - Z > X/Y
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    retained_hand = [given_hand[-1]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 24: Z retained hand - X/Y > Z
    num = random_nums(3)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*2 + [num[1]]*2 + [num[2]], random_suits(5))
    retained_hand = [given_hand[-1]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 25: Z retained hand - X > Z > Y
    num = random_nums(3)
    num.sort()
    given_hand = create_hand([num[1]]*2 + [num[0]]*2 + [num[2]], random_suits(5))
    retained_hand = [given_hand[-1]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_two_pairs)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_two_pairs_combination(given_hand, retained_hand) == len(all_better_combination)

    # Test
    if player.is_two_pair(TEST_GIVEN_HAND):
        all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_two_pairs)
        all_better_combination = find_better_combo(TEST_GIVEN_HAND, all_valid_combination)
        assert player.calc_total_better_two_pairs_combination(TEST_GIVEN_HAND, TEST_RETAINED_HAND) == len(all_better_combination)

def test_calc_total_better_pair_combination(player: Player):
    def find_better_combo(given_hand, all_valid_combo, print_result=False):
        output = []
        
        # Setup
        given_pair = None
        given_kicker_list = []
        given_values = [card.value for card in given_hand]
        
        for val in set(given_values):
            if given_values.count(val) == 2:
                given_pair = val
            if given_values.count(val) == 1:
                given_kicker_list.append(val)

        given_kicker_list.sort(reverse=True)

        for combo in all_valid_combo:
            # find each combo's pair and kicker val
            combo_pair = None
            combo_kicker = []
            combo_values = [card.value for card in combo]
            for val in set(combo_values):
                if combo_values.count(val) == 2:
                    combo_pair = val
                if combo_values.count(val) == 1:
                    combo_kicker.append(val)

            combo_kicker.sort(reverse=True)

            # compare to find BETTER combo
            if combo_pair > given_pair:
                output.append(combo)
            if combo_pair == given_pair:
                for i in range(3):
                    if combo_kicker[i] > given_kicker_list[i]:
                        output.append(combo)
                        break
                    if combo_kicker[i] < given_kicker_list[i]:
                        break

        if print_result:
            for combo in output:
                str_combo = [str(card) for card in combo]
                print(str_combo)
        
        return output
    
    # all one pair
    all_one_pair = []
    num_list = list(range(2,15))
    pairs = all_iter_combination(count=2, num_list=num_list)

    for pair in pairs:
        num_list = list(range(2,15))
        num_list.remove(pair[0].value)
        random_num = random_num_combination(count=3, num_list=num_list)
        for num in random_num:
            all_one_pair.append(pair + list(num))

    # scenario 1: best pair combo: A-A-K-Q-J - no retained hand
    given_hand = create_hand([14,14,13,12,11], random_suits(5))
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_one_pair_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 2: worst pair combo: 2-2-3-4-5 - no retained hand
    given_hand = create_hand([2,2,3,4,5], random_suits(5))
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    all_better_combination = find_better_combo(given_hand,all_valid_combination)
    assert player.calc_total_better_one_pair_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 3: XXYZ retained_hand
    num = random_nums(4)
    given_hand = create_hand([num[0]]*2 + [num[1]] + [num[2]] + [num[3]], random_suits(5))
    retained_hand = given_hand[:-1]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    all_better_combination = find_better_combo(given_hand,all_valid_combination)
    assert player.calc_total_better_one_pair_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 4: XYZA retained_hand - YZA > X
    num = random_nums(4)
    num.sort()
    given_hand = create_hand([num[0]]*2 + [num[1]] + [num[2]] + [num[3]], random_suits(5))
    retained_hand = given_hand[1:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_one_pair_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 5: XYZA retained_hand - X > YZA
    num = random_nums(4)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*2 + [num[1]] + [num[2]] + [num[3]], random_suits(5))
    retained_hand = given_hand[1:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_one_pair_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 6: XYZA retained_hand - Y > X > ZA
    num = random_nums(4)
    num.sort()
    given_hand = create_hand([num[1]]*2 + [num[0]] + [num[2]] + [num[3]], random_suits(5))
    retained_hand = given_hand[1:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_one_pair_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 7: XXY retained_hand
    num = random_nums(4)
    given_hand = create_hand([num[0]]*2 + [num[1]] + [num[2]] + [num[3]], random_suits(5))
    retained_hand = given_hand[:3]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_one_pair_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 8: XYZ retained_hand - YZ > X
    num = random_nums(4)
    num.sort()
    given_hand = create_hand([num[0]]*2 + [num[1]] + [num[2]] + [num[3]], random_suits(5))
    retained_hand = given_hand[1:4]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_one_pair_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 9: XYZ retained_hand - X > YZ
    num = random_nums(4)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*2 + [num[1]] + [num[2]] + [num[3]], random_suits(5))
    retained_hand = given_hand[1:4]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_one_pair_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 10: XYZ retained_hand - Y > X > Z
    num = random_nums(4)
    num.sort()
    given_hand = create_hand([num[1]]*2 + [num[0]] + [num[2]] + [num[3]], random_suits(5))
    retained_hand = given_hand[1:4]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_one_pair_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 11: XX retained_hand
    num = random_nums(4)
    given_hand = create_hand([num[0]]*2 + [num[1]] + [num[2]] + [num[3]], random_suits(5))
    retained_hand = given_hand[:2]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_one_pair_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 12: XY retained_hand - Y > X
    num = random_nums(4)
    num.sort()
    given_hand = create_hand([num[0]]*2 + [num[1]] + [num[2]] + [num[3]], random_suits(5))
    retained_hand = given_hand[1:3]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_one_pair_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 13: XY retained_hand - X > Y
    num = random_nums(4)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*2 + [num[1]] + [num[2]] + [num[3]], random_suits(5))
    retained_hand = given_hand[1:3]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_one_pair_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 14: X retained_hand - YZA > X
    num = random_nums(4)
    num.sort()
    given_hand = create_hand([num[0]]*2 + [num[1]] + [num[2]] + [num[3]], random_suits(5))
    retained_hand = [given_hand[0]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_one_pair_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 15: X retained_hand - X > YZA
    num = random_nums(4)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*2 + [num[1]] + [num[2]] + [num[3]], random_suits(5))
    retained_hand = [given_hand[0]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_one_pair_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 16: X retained_hand - Y > X > ZA
    num = random_nums(4)
    num.sort()
    given_hand = create_hand([num[1]]*2 + [num[0]] + [num[2]] + [num[3]], random_suits(5))
    retained_hand = [given_hand[0]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_one_pair_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 17: Y retained_hand Y > X
    num = random_nums(4)
    num.sort()
    given_hand = create_hand([num[0]]*2 + [num[1]] + [num[2]] + [num[3]], random_suits(5))
    retained_hand = [given_hand[-1]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_one_pair_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 18: Y retained_hand - X > Y
    num = random_nums(4)
    num.sort(reverse=True)
    given_hand = create_hand([num[0]]*2 + [num[1]] + [num[2]] + [num[3]], random_suits(5))
    retained_hand = [given_hand[-1]]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_one_pair)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_one_pair_combination(given_hand, retained_hand) == len(all_better_combination)

    # TEST
    if player.is_one_pair(TEST_GIVEN_HAND):
        all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_one_pair)
        all_better_combination = find_better_combo(TEST_GIVEN_HAND, all_valid_combination)
        assert player.calc_total_better_one_pair_combination(TEST_GIVEN_HAND, TEST_RETAINED_HAND) == len(all_better_combination)

def test_calc_total_better_high_card_combination(player: Player):
    # helper function to find combo that is BETTER than given hand
    def find_better_combo(given_hand, all_valid_combo, print_result=False):
        output = []
        given_hand_value = [card.value for card in given_hand]
        given_hand_value.sort(reverse=True)

        for combo in all_valid_combo:
            combo_value = [card.value for card in combo]
            combo_value.sort(reverse=True)

            for i in range(5):
                if combo_value[i] > given_hand_value[i]:
                    output.append(combo)
                    break
                if combo_value[i] < given_hand_value[i]:
                    break

        if print_result:
            for combo in output:
                str_combo = [str(card) for card in combo]
                print(str_combo)

        return output

    # generate all high card combination:
    all_high_card_combination = []
    all_five_card_combination = random_num_combination(5, list(range(2,15)))

    consecutive_value_combos = [[i, i+1, i+2, i+3, i+4] for i in range(2, 11)]

    for combo in all_five_card_combination:
        combo_value = [card.value for card in combo]
        combo_suit = [card.suit for card in combo]
        combo_value.sort()

        # all_unique = len(set(combo_value)) == 5
        straight = combo_value in consecutive_value_combos
        flush = len(set(combo_suit)) == 1

        if not straight and not flush:
            all_high_card_combination.append(combo)

    # sanity check - removing straight/flush/pair/triple/quad
    # ((13/choose 5) - (9/choose 1)) * ((4/choose 1)^5 - (4/choose 1)) == 1,305,960
    assert len(all_high_card_combination) == (math.comb(13,5) - math.comb(9,1)) * (math.comb(4,1)**5 - math.comb(4,1))
    assert len(all_high_card_combination) == 1303560

    # scenario 1: best high card A-K-Q-J-9 - no retained hand
    given_hand = create_hand([14,13,12,11,9], random_suits(5))
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_high_card_combination)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_high_card_combination(given_hand, retained_hand) == len(all_better_combination)


    # scenario 2: worst high card 2-3-4-5-7 - no retained hand
    given_hand = create_hand([2,3,4,5,7], random_suits(5))
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_high_card_combination)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_high_card_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 3: no retained hand
    given_hand = create_hand(random_nums(5), random_suits(5))
    retained_hand = []
    all_valid_combination = hand_in_valid_combination(retained_hand, all_high_card_combination)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_high_card_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 4: retained hand
    given_hand = create_hand(random_nums(5), random_suits(5))
    retained_hand = given_hand[3:]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_high_card_combination)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_high_card_combination(given_hand, retained_hand) == len(all_better_combination)

    # scenario 5: retained card can make straight 
    given_hand = create_hand([2,3,4,5,7], random_suits(5))
    retained_hand = given_hand[:3]
    all_valid_combination = hand_in_valid_combination(retained_hand, all_high_card_combination)
    all_better_combination = find_better_combo(given_hand, all_valid_combination)
    assert player.calc_total_better_high_card_combination(given_hand, retained_hand) == len(all_better_combination)

    # Test
    if player.is_high_card(TEST_GIVEN_HAND):
        all_valid_combination = hand_in_valid_combination(retained_hand, all_high_card_combination)
        all_better_combination = find_better_combo(TEST_GIVEN_HAND, all_valid_combination)
        assert player.calc_total_better_high_card_combination(TEST_GIVEN_HAND, TEST_RETAINED_HAND) == len(all_better_combination)
    
# endregion calc better combo if hand is already a given combo