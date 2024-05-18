import pytest
import random
from player import Player
from deck import Deck
from card import Card
import itertools
import math

pytest.skip("Run only when testing a specific test case", allow_module_level=True)
# region fixture and helper function
@pytest.fixture
def player():
    player = Player()
    return player

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
TEST_GIVEN_HAND = create_hand([10,11,12,13,14], ["♠️", "♠️", "♠️", "♠️","♠️"])
TEST_RETAINED_HAND = [TEST_GIVEN_HAND[1], TEST_GIVEN_HAND[2], TEST_GIVEN_HAND[-1]]

print("TEST_GIVEN_HAND: ", [str(card) for card in TEST_GIVEN_HAND])
print("TEST_RETAINED_HAND: ", [str(card) for card in TEST_RETAINED_HAND])

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

    # Test
    all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_royal_flush)
    assert player.calc_royal_flush_total_combination(TEST_RETAINED_HAND) == len(all_valid_combination)

def test_calc_straight_flush_total_combination(player: Player):
    # find all straight flush combo
    all_straight_flush = all_iter_consecutive_combination(flush=True, royal=False)

    # Test
    all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_straight_flush)
    assert player.calc_straight_flush_total_combination(TEST_RETAINED_HAND) == len(all_valid_combination)  

def test_calc_straight_flush_total_combination(player: Player):
    # find all straight flush combo
    all_straight_flush = all_iter_consecutive_combination(flush=True, royal=False)

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

    # Test
    all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_flush)
    assert player.calc_flush_total_combination(TEST_RETAINED_HAND) == len(all_valid_combination)

def test_calc_straight_total_combination(player: Player):
    # find all straight combo
    all_straight_no_flush = all_iter_consecutive_combination(flush=False, royal=True)

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

    # Test
    all_valid_combination = hand_in_valid_combination(TEST_RETAINED_HAND, all_one_pair)
    assert player.calc_one_pair_total_combination(TEST_RETAINED_HAND) == len(all_valid_combination)

# endregion check total number of combinations

# region calc better combo if hand is already a given combo
def test_calc_total_better_royal_flush_combination(player: Player):
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

    # Test
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

    # Test
    if player.is_high_card(TEST_GIVEN_HAND):
        all_valid_combination = hand_in_valid_combination(retained_hand, all_high_card_combination)
        all_better_combination = find_better_combo(TEST_GIVEN_HAND, all_valid_combination)
        assert player.calc_total_better_high_card_combination(TEST_GIVEN_HAND, TEST_RETAINED_HAND) == len(all_better_combination)
    