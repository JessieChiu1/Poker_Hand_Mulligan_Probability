import math
import itertools
from deck import Deck

class Player:
    def __init__(self):
        self.hand = []

    def draw(self, card):
        self.hand.append(card)
    
    def mulligan(self, mulligan_list, deck):
        for card in mulligan_list:
            self.hand.remove(card)
        new_cards = deck.mulligan(mulligan_list)
        for card in new_cards:
            self.draw(card)

    def show_hand(self):
        hand = [str(card) for card in self.hand]
        print(f"Player's hand: {hand}")

    def is_same_suit(self, card_list):
        """
        check if input are same suit - return true when card_list is empty
        """
        suits = [card.suit for card in card_list]
        return len(set(suits)) <= 1
    
    def generate_all_retained_hand_combination(self, given_hand):
        """
        - keep an output list
        - generate all keep 0,1,2,3,4 card combo
        """
        output = []

        output.append([])
        for i in range(1,5):
            iterations = list(itertools.combinations(given_hand,i))
            [output.append(list(iteration)) for iteration in iterations]

        return output

    def generate_method_list(self, given_hand):
        """
        Generate the list of dictionary that pertained to a given hand.

        It is used for calc_percent_of_better_combination method
        """
        formula_list = [{
            "name": "high card",
            "check": self.is_high_card,
            "better": self.calc_total_better_high_card_combination,
        }, {
            "name": "one pair",
            "check": self.is_one_pair,
            "total": self.calc_one_pair_total_combination,
            "better": self.calc_total_better_one_pair_combination
        }, {
            "name": "two pair",
            "check": self.is_two_pair,
            "total": self.calc_two_pairs_total_combination,
            "better": self.calc_total_better_two_pairs_combination,
        }, {
            "name": "three of a kind",
            "check": self.is_three_of_a_kind,
            "total": self.calc_three_of_a_kind_total_combination,
            "better": self.calc_total_better_three_of_a_kind_combination,
        }, {
            "name": "straight",
            "check": self.is_straight,
            "total": self.calc_straight_total_combination,
            "better": self.calc_total_better_straight_combination,
        }, {
            "name": "flush",
            "check": self.is_flush,
            "total": self.calc_flush_total_combination,
            "better": self.calc_total_better_flush_combination,
        }, {
            "name": "full house",
            "check": self.is_full_house,
            "total": self.calc_full_house_total_combination,
            "better": self.calc_total_better_full_house_combination,
        }, {
            "name": "four of a kind",
            "check": self.is_four_of_a_kind,
            "total": self.calc_four_of_a_kind_total_combination,
            "better": self.calc_total_better_four_of_a_kind_combination,
        }, {
            "name": "straight flush",
            "check": self.is_straight_flush,
            "total": self.calc_straight_flush_total_combination,
            "better": self.calc_total_better_straight_flush_combination,
        }, {
            "name": "royal flush",
            "check": self.is_royal_flush,
            "total": self.calc_royal_flush_total_combination,
            "better": self.calc_total_better_royal_flush_combination
        }]

        for i in range(len(formula_list)):
            if formula_list[i]["check"](given_hand) == True:
                return formula_list[i:]

    def calc_percent_of_better_combination(self, given_hand, retained_hand, method_list):
        """
        Calculate the percentage of better combination for a specific set of retained hand
        """
        num_card_to_draw = 5 - len(retained_hand)
        current_combo = method_list[0]
        better_combo = method_list[1:]

        num_all_combinations = self.calc_total_combination(num_card_to_draw)
        better_combination = 0
        better_combination += current_combo["better"](given_hand, retained_hand)
        for combo in better_combo:
            try:
                better_combination += combo["total"](retained_hand)
            except TypeError:
                print(f"given_hand: {[str(card) for card in given_hand]}")
                print(f"retained_hand: {[str(card) for card in retained_hand]}")
                print(f"stopped at: calc total combination of {combo['name']}\n")
                return
            
            
        return better_combination / num_all_combinations
    
    def find_best_retained_hand(self, given_hand, print_result=False):
        """
        This method will loop through all retained hand combinations to find the retained hand combination that yield the best percentage of better combinations
        """
        # setup
        best_retained_hand = None
        best_better_hand_probability = 0

        retained_hand_combination = self.generate_all_retained_hand_combination(given_hand)
        method_list = self.generate_method_list(given_hand)

        for retained_hand in retained_hand_combination:
            retained_hand_p = self.calc_percent_of_better_combination(given_hand, retained_hand, method_list)

            if print_result:
                print(f"given_hand: {[str(card) for card in given_hand]}\nretained_hand: {[str(card) for card in retained_hand]}\nbetter_hand_probability: {retained_hand_p * 100:.2f}%\n")

            if retained_hand_p > best_better_hand_probability:
                best_retained_hand = retained_hand
                best_better_hand_probability = retained_hand_p
        
        # print result
        print("\n\n\n")
        print("Best retained hand:")
        if best_retained_hand == None:
            print(f"given hand: {[str(card) for card in given_hand]}\nbest retained hand: {None}\nbest retained hand probabilities: {best_better_hand_probability * 100:.2f}%")
        else:
            print(f"given hand: {[str(card) for card in given_hand]}\nbest retained hand: {[str(card) for card in best_retained_hand]}\nbest retained hand probabilities: {best_better_hand_probability * 100:.2f}%")

        return (best_retained_hand, best_better_hand_probability)
    
    # region check combo method
    
    def is_royal_flush(self, card_list):
        """
        same suit and 10-Jack-Queen-King-Ace order
        """
        if len(card_list) != 5:
            return False
        
        values = sorted([card.value for card in card_list])

        if self.is_same_suit(card_list) and values == [10, 11, 12, 13, 14]:
            return True
        return False

    def is_straight_flush(self, card_list):
        """
        all same suit
        and in
        2-3-4-5-6-7-8-9-10-Jack-Queen-King consecutive order
        """
        values = [card.value for card in card_list]
        consecutive_value_combos = [[i, i+1, i+2, i+3, i+4] for i in range(2, 10)]

        for combo in consecutive_value_combos:
            consecutive = all(val in combo for val in values)
            same_suit = self.is_same_suit(card_list)
            if consecutive and same_suit:
                return True
        
        return False

    def is_four_of_a_kind(self, card_list):
        """
        same card's value x4
        X-X-X-X-Y
        """
        if len(card_list) != 5:
            return False

        values = [card.value for card in card_list]
        for value in set(values):
            if values.count(value) == 4:
                return True
        return False

    def is_full_house(self, card_list):
        """
        triple and pair
        X-X-X-Y-Y
        """
        if len(card_list) != 5:
            return False

        value_counts = []
        values = [card.value for card in card_list]
        unique_values = set(values)

        for value in unique_values:
            count = values.count(value)
            value_counts.append({'value': value, 'count': count})

        if len(value_counts) == 2:
            for count_dict in value_counts:
                if count_dict['count'] == 3:
                    return True

        return False
    
    def is_flush(self, card_list):
        """
        same suit no pattern
        """
        consecutive_value_combos = [[i, i+1, i+2, i+3, i+4] for i in range(2, 11)]

        if len(card_list) != 5:
            return False

        if not self.is_same_suit(card_list):
            return False

        values = [card.value for card in card_list]
        values.sort()
        if values in consecutive_value_combos:
            return False

        return True

    def is_straight(self, card_list):
        """
        different suit but consecutive order
        """
        if self.is_same_suit(card_list):
            return False

        consecutive_value_combos = [(i, i+1, i+2, i+3, i+4) for i in range(2, 11)]

        values = [card.value for card in card_list]
        values.sort()
        
        for combo in consecutive_value_combos:
            if all(val in values for val in combo):
                return True
        
        return False

    def is_three_of_a_kind(self, card_list):
        """
        triple + 2 unique single
        XXXYZ
        """
        counts = {}
        values = [card.value for card in card_list]

        for value in set(values):
            counts[value] = values.count(value)

        sorted_counts = sorted(counts.values())

        return sorted_counts == [1, 1, 3]

    def is_two_pair(self, card_list):
        """
        2 pairs + 1 kicker
        XXYYZ
        """
        counts = {}
        values = [card.value for card in card_list]
        
        for value in set(values):
            counts[value] = values.count(value)

        sorted_counts = sorted(counts.values())

        return sorted_counts == [1, 2, 2]

    def is_one_pair(self, card_list):
        """
        1 pair + 3 unqiue kicker
        XXYZA
        """
        counts = {}
        values = [card.value for card in card_list]
        
        for value in set(values):
            counts[value] = values.count(value)

        sorted_counts = sorted(counts.values())

        return sorted_counts == [1, 1, 1, 2]

    def is_high_card(self, card_list):
        """
        no combo
        """
        values = [card.value for card in card_list]
        values.sort()

        consecutive_value_combos = [[i, i+1, i+2, i+3, i+4] for i in range(2, 11)]
        straight = values in consecutive_value_combos

        straight = False
        for combo in consecutive_value_combos:
            if all(val in values for val in combo):
                straight = True

        same_suit = self.is_same_suit(card_list)

        if len(set(values)) == 5 and not straight and not same_suit:
            return True

        return False

    # endregion check combo method

    # region calculate total combination of combo per hand
    def calc_total_combination(self, mulligan_num):
        """
        Calculate the total number of possible combinations of cards after a mulligan.
        """
        total_cards_in_deck = 52
        hand_size = 5
        card_in_deck = total_cards_in_deck - hand_size + mulligan_num

        return math.comb(card_in_deck, mulligan_num)
    
    def calc_royal_flush_total_combination(self, retained_hand):
        """
        Conditions:
        - royal flush needs to all be in the same suit
        - 10-Jack-Queen-King-Ace order

        Scenarios:
        1. players didn't retained cards in hand
            - 4 possible combo for each suit
        2. players did retained card(s)
            - check if they are same suit
            - check if they are the all within the value
            - there can be max 1 royal flush combo in this scenario
        """
        if len(retained_hand) == 0:
            return 4

        if not self.is_same_suit(retained_hand):
            return 0
        
        for card in retained_hand:
            if card.value not in [10,11,12,13,14]:
                return 0
        
        return 1
    
    def calc_straight_flush_total_combination(self, retained_hand):
        """
        Conditions:
        - needs to be the same suit
        - in consecutive order
        - DO NOT count royal flush

        I thought the best way to solve this would be to find all of the combination of straight based on value alone and eliminate them based on the retained_hand. I set the range from 2 to 13 (14: Ace will not be included) because I didn't want to include the royal flush combinations

        Scenarios
        1. players didn't retained cards in hand
            - count total straight per suit
            - 4 * consecutive combo because there are 4 suits
        2. players did retained card(s)
            - check if they are the same suit
            - check how many consecutive_value_combo contains all of the retained_hand's value
        """
        # this is all straight and royal flush num combinations
        consecutive_straight_combo = [(i, i+1, i+2, i+3, i+4) for i in range(2, 10)]

        if len(retained_hand) == 0:
            return 4 * len(consecutive_straight_combo)

        if not self.is_same_suit(retained_hand):
            return 0
        
        valid_combinations = 0
        value = [card.value for card in retained_hand]

        for combo in consecutive_straight_combo:
            if all(val in combo for val in value):
                valid_combinations += 1
        return valid_combinations

    def calc_four_of_a_kind_total_combination(self, retained_hand):
        """
        Condition:
        - 4x same value card
        - 1x random card

        Scenarios:
        1. players didn't retained cards in hand
            - 13 possible 4x same value card 
            - the remaining cards in the deck would be 48 
            - each of those 13 possibilities can match with those 48 random cards
            - 13 x 48
        2. players did retained card(s)
            - possible total unique card on hand < 2 to be valid(Set)
            - XXXX or XXX or XX
                - X is predetermined quad 
                - find all possible kicker
            - XX(X)Y
                - value is predetermined
                - X is predetermined quad
                - only 1 possibilities
            - XY
                - value for combo is predetermined
                - either XXXXY or YYYYX 
            - X or Y
                - can either be quad or kicker
                - find all possible kicker
                - find all possible quad
        """
        if len(retained_hand) == 0:
            return 13 * 48
        
        values = [card.value for card in retained_hand]
        if len(set(values)) > 2:
            return 0
        
        count_list = []
        for val in set(values):
            count_list.append(values.count(val))

        count_list.sort()

        if count_list == [4] or count_list == [3] or count_list == [2]:
            all_kicker = 12 * 4
            return all_kicker
        
        if count_list == [1,2] or count_list == [1,3]:
            return 1
        
        if count_list == [1,1]:
            return 2

        if len(retained_hand) == 1:
            # card is quad
            all_kicker = 12 * 4
            # card is single
            all_quad = 12
            return all_kicker + all_quad

        return 0
         
    def calc_full_house_total_combination(self, retained_hand):
        """
        Condition:
        - triple + pair

        Scenarios:
        1. players didn't retained cards in hand
            - total triple possibilities is 13
            - total pair possibilities is 12 (because the triple's value is invalid)
            - find total possible way to draw 3x same value card from 4
            - find total possible way to draw 2x same value card from 4
            - each of those 3x possibilities can match with each 2x possibilities
        2. players did retained card(s)
            - possible total unique card on hand < 2 to be valid (Set)
            - create list that keep track of number count
            - all valid num_counter are [1] [2] [3] [1,1] [1,2] [1,3] [2,2]
                - X / XX / XXX / XY / XXY / YYX / XXXY / XXYY
            - if there is a num that is already triple, it limit the triple possibilities
            - if there is already 2 numbers in the retained hand, it limited both triple and pair possibilities

        """
        if len(retained_hand) == 0:
            total_full_house_num_combo = 13 * 12
            total_triple_combo_given_num = math.comb(4,3)
            total_pair_combo_given_num = math.comb(4,2)
            return total_full_house_num_combo * total_triple_combo_given_num * total_pair_combo_given_num
        
        values = [card.value for card in retained_hand]
        if len(set(values)) > 2:
            return 0

        count_list = []
        for value in set(values): 
            count_list.append(values.count(value))

        
        count_list.sort()
        
        # the count should be any of these possibilities [1] [2] [3] [1,1] [1,2] [1,3] [2,2]

        # if retained hand has only 1 values, that leaves a lot of possibility on the pair and triple
        if 3 in count_list:
            # count = [3] - no limit on pair combination
            if len(count_list) == 1:
                return math.comb(4,2) * 12
            # count = [1,3] - there is only 3 possibilities because the number for full house combo is already determine
            return math.comb(3,1)

        # limitless pair or triple possibilities because only 1 number is determined
        if len(count_list) == 1:
            # card is triple possibilities 
            triple_combo = math.comb(4-count_list[0], 3-count_list[0])
            other_pair_combo = math.comb(4,2) * 12
            all_combination_where_card_is_triple = triple_combo * other_pair_combo
            # card is pair possibilities
            other_triple_combo = math.comb(4,3) * 12
            pair_combo = math.comb(4-count_list[0],2 - count_list[0]) 
            all_combination_where_card_is_pair = other_triple_combo * pair_combo

            return all_combination_where_card_is_triple + all_combination_where_card_is_pair

        # limited pair or triple possibilities because both num is determined
        # XXY
        if len(count_list) == 2:
            # count[0] is triple and count[1] is pair
            triple_combo = math.comb(4-count_list[0], 3-count_list[0])
            pair_combo = math.comb(4-count_list[1],2-count_list[1])

            combo_position_a = triple_combo * pair_combo
            # count[1] is triple and count[0] is pair
            triple_combo = math.comb(4-count_list[1], 3-count_list[1])
            pair_combo = math.comb(4-count_list[0],2-count_list[0])

            combo_position_b = triple_combo * pair_combo

            return combo_position_a + combo_position_b

    def calc_flush_total_combination(self, retained_hand):
        """
        Condition:
        - all same suit
        - DO NOT 2x count royal flush/straight flush combo

        Scenarios:
        1. cards are different suit
        2. players didn't retained cards in hand
            - 4 suits
            - find total possible way to draw 5 card from 13
            - 4 x total comb
        3. players did retained card(s)
            - find all possible 5 card combination for a single suit
            - take away all possible straight/royal flush combination - this is different depending on number, if it is a 2, there is only 1 straight combination

        """
        if not self.is_same_suit(retained_hand):
            return 0

        consecutive_value_combos = [(i, i+1, i+2, i+3, i+4) for i in range(2, 11)]

        if len(retained_hand) == 0:
            return 4 * (math.comb(13,5) - len(consecutive_value_combos))
        
        remaining_card_with_same_suit = 13 - len(retained_hand)

        flush_with_royal_and_straight = math.comb(remaining_card_with_same_suit, 5 - len(retained_hand))

        value = [card.value for card in retained_hand]

        consecutive_combo_count = 0
        for combo in consecutive_value_combos:
            if all(val in combo for val in value):
                consecutive_combo_count += 1

        return flush_with_royal_and_straight - consecutive_combo_count 

    def calc_straight_total_combination(self, retained_hand):
        """
        Condition:
        - all consecutive order
        - DO NOT count royal flush/straight flush combo
        - include [10,J,Q,K,A] 
        - NO steel wheel [A,2,3,4,5]

        Scenarios:
        1. players didn't retained cards in hand
            - find total possible consecutive num_combo without
                - eg. [2,3,4,5,6] or [10,J,Q,K,A]
            - for any given combo
                - there are 4 suit for each value
                - so the total suit combo with any given number order is 
                - each of those possibilities multiply by each other 
                - remove straight/royal flush combo
        2. players did retained card(s)
            - if there is any repeat value - return 0
            - find all valid consecutive combination
            - for each of those valid consecutive combination, it depends on how many cards is missing, if we need 2 card to complete the hand, then each of those 2 card can be in any suit, thus 4 * 4
            - if all of the card in retained hand is the same suit, we need to also remove the scenario where the it can be a straight flush 
        """
        consecutive_value_combos = [(i, i+1, i+2, i+3, i+4) for i in range(2, 11)]
        values = [card.value for card in retained_hand]

        if len(values) != len(set(values)):
            return 0
        
        if len(retained_hand) == 0:
            total_combo_num_order = len(consecutive_value_combos)
            # Each card can have any of the 4 suits
            total_combo_given_order_w_suit = 4 ** 5  
            # 4 straight flushes per suit per consecutive combo
            total_combo_same_suit_given_order = 4
            return total_combo_num_order * (total_combo_given_order_w_suit - total_combo_same_suit_given_order)
        

        valid_straight = []

        for combo in consecutive_value_combos:
            if all(num in combo for num in values):
                valid_straight.append(combo)

        # because each card can be 4 different suit, the number of possibilities depends on how many card(s) is missing from our hand
        # ie. 1 card missing 4 different outcome, 2 card missing 4*4 outcome
        num_card_missing = 5 - len(retained_hand)
        output = len(valid_straight) * (4 ** num_card_missing)

        # if all of the card in hand is the same suit, then for each valid combination, there is 1 combination that will be a straight flush instead
        if self.is_same_suit(retained_hand):
            return output - len(valid_straight)
        return output

    def calc_three_of_a_kind_total_combination(self, retained_hand):
        """
        Condition:
        - triple
        - 2x random cards NOT Pair
        - DO NOT count 4 of a kind/full house combo

        Scenarios:
        1. players didn't retained cards in hand
            - all triple combinations * all two single NON-pair combination
        2. players did retained card(s)
            - Invalid - if 4 unique card in retained hand
            - Invalid - XXYY - only 2 pairs or full house
            - check if there are more than 3 unique value - invalid
            - XXYZ
                - drawing X
            - XXX
                - drawing random 2 NON-pair number
            - XXY
                - drawing X * drawing non Z
            - XYZ
                - drawing XX + drawing YY + drawing ZZ
            - XY
                - drawing XX * drawing Z
                - drawing YY * drawing Z
            - XX
                - drawing X + random 2 NON-pair number
                - drawing X * drawing random 2 Non-pair number
            - X
                - drawing XX * drawing Y * drawing Z
                - drawing Z * drawing YYY

        """
        if len(set([card.value for card in retained_hand])) > 3:
            return 0

        if len(retained_hand) == 0:
            triple_combinations = math.comb(4, 3) * 13
            # choose 2 number from the remaining 12 number and each of them has 1/4 chance to choose in that suit
            single_combinations = math.comb(12, 2) * (math.comb(4, 1) ** 2) 
            return triple_combinations * single_combinations
        
        values = [card.value for card in retained_hand]
        
        count_list = []
        for value in set(values):
            count = values.count(value)
            count_list.append(count)
        
        count_list.sort()

        # XXYZ
        if count_list == [1,1,2]:
            return math.comb(2,1)
        # XXYY
        if count_list == [2,2]:
            return 0
        # XXXY
        if count_list == [1,3]:
            return (13 - 2) * 4
        # XXX
        if count_list == [3]:
            # all combinations of any 2 number because it can't be x
            # all suit possibilities
            return math.comb(12, 2) * (4 ** 2)
        # XYY
        if count_list == [1,2]:
            draw_y = 2
            draw_z = (13 - 2) * 4
            return draw_y * draw_z
        # XYZ
        if count_list == [1,1,1]:
            # draw_pair represent drawing either XX YY or ZZ
            draw_pair = math.comb(3,2)
            return 3 * draw_pair
        # XX
        if count_list == [2]:
            # draw X
            draw_x = 2
            # draw yz
            draw_yz = math.comb(12, 2) * (4 ** 2)
            return draw_x * draw_yz
        # XY
        if count_list == [1,1]:
            # XXXYZ and YYYXZ
            draw_xx = math.comb(3, 2)
            draw_y = (13 - 2) * 4
            freq_1 = 2 * (draw_xx * draw_y)
            # ZZZXY
            triple = math.comb(11,1) * math.comb(4,3)
            # total
            return freq_1 + triple
        # X
        if count_list == [1]:
            # scenario XXXYZ
            draw_xx = math.comb(3,2)
            draw_yz = math.comb(12, 2) * (4 ** 2)
            freq_1 = draw_xx * draw_yz
            # scenario YYYXZ
            draw_triple = math.comb(12,1) * math.comb(4,3)
            draw_z = (13 - 2) * 4
            freq_2 = draw_triple * draw_z
            return freq_1 + freq_2
         
    def calc_two_pairs_total_combination(self, retained_hand):
        """
        Condition:
        - 2x pairs
        - 1x random card with DIFFERENT value from pairs

        Scenarios:
        1. players didn't retained cards in hand
            - given any value, find total pair combinations based on suit
            - any two number combination 
            - any two number has 4 suit possibilities each
            - all remaining card combination with different value from two pairs
        2. players did retained card(s)
            - Invalid - unique cards > 3
            - Invalid - triple or quad
            - XXYZ
                - drawing Y + drawing Z
            - XXYY
                - drawing non-pair num card
            - XXY
                - drawing Y + drawing any pair
            - XYZ
                - drawing X and Y
                - drawing Y and Z
                - drawing Z and X
            - XX
                - drawing any pairs
                - drawing a random num
            - XY
                - drawing X, Y, Z
                - drawing X and any pair
                - drawing Y and any pair
            - X
                - drawing X and pair and Z
                - drawing 2 pairs
        """
        if len(retained_hand) == 0:
            two_num = math.comb(13,2)
            two_pair_comb = two_num * (math.comb(4,2) ** 2)
            one_num = math.comb(11, 1) * math.comb(4,1)
            return two_pair_comb * one_num
                
        values = [card.value for card in retained_hand]
        if len(set(values)) > 3:
            return 0 
        
        count_list = []
        for val in set(values):
            count_list.append(values.count(val))

        count_list.sort()

        # frequent math.comb
        draw_one_from_three = math.comb(3,1)
        draw_two_pairs = math.comb(12,2) * (math.comb(4,2) ** 2)
        draw_non_pair_num = math.comb(52 - 8 ,1)
        
        # XXXX or XXX
        if 3 in count_list or 4 in count_list:
            return 0
        # XXYY
        if count_list == [2,2]:
            return (13 - len(count_list)) * 4
        # XXYZ
        if count_list == [1,1,2]:
            # draw y + draw z
            return 2 *draw_one_from_three
        # XYZ
        if count_list == [1,1,1]:
            # draw x and draw y
            freq_1 = draw_one_from_three ** 2
            # draw y and z
            freq_2 = draw_one_from_three ** 2
            # draw x and z
            freq_3 = draw_one_from_three ** 2
            
            return freq_1 + freq_2 + freq_3
        # XXY
        if count_list == [1,2]:
            # draw y and z
            freq_1 = draw_one_from_three * draw_non_pair_num
            # draw any pair
            draw_pair = math.comb(11,1) * math.comb(4,2)
            return freq_1 + draw_pair
        # XX
        if count_list == [2]:
            # draw pair and z
            draw_pair = math.comb(12,1) * math.comb(4,2)
            return draw_pair * draw_non_pair_num
        # XY
        if count_list == [1,1]:
            # draw x y z
            freq_1 = (draw_one_from_three ** 2) * draw_non_pair_num
            # draw x and pair
            draw_pair = math.comb(11,1) * math.comb(4,2)
            freq_2 = draw_one_from_three * draw_pair
            # draw y and pair
            freq_3 = draw_one_from_three * draw_pair
            return freq_1 + freq_2 + freq_3
        # X
        if count_list == [1]:
            draw_pair = math.comb(12,1) * math.comb(4,2)
            # draw x pair and z
            freq_1 = draw_one_from_three * draw_pair * draw_non_pair_num
            # draw 2 pair
            freq_2 = draw_two_pairs
            return freq_1 + freq_2
                 
    def calc_one_pair_total_combination(self, retained_hand):
        """
        Condition:
        - 1 pairs
        - 3x random cards with DIFFERENT pairs and each other
        - DO NOT count full house/2x pair combo

        Scenarios:
        1. players didn't retained cards in hand
            - all pair combination
            - choose 3 from non-pair num with suit consideration
        2. players did retained card(s)
            - Invalid - XXXX XXX XXYY
            - XXYZ
                - pair is predetermined
            - XYZA
                - find all combination of drawing either X/Y/Z/A
            - XXY
                - pair is predetermined
            - XYZ
                - find all combination of drawing either X/Y/Z and 1 other non-pairing card
                - find all remaining pair combination
            - XX
                - all random 3 card combination with non-pair value
            - XY
                - draw X and 2 random
                - draw y and 2 random
                - draw pair and z
            - X
                - draw x and 3 random
                - draw pair and 2 random
        """
        if len(retained_hand) == 0:
            pair_combo = math.comb(13,1) * (math.comb(4,2))
            three_num = math.comb(12,3) * (math.comb(4,1) ** 3)
            return pair_combo * three_num
        
        values = [card.value for card in retained_hand]
        if len(set(values)) > 4:
            return 0 
        
        count_list = []
        for val in set(values):
            count_list.append(values.count(val))

        count_list.sort()

        # XXX XXXX XXYY
        if 3 in count_list or 4 in count_list or count_list == [2,2]:
            return 0
        # XXYZ
        if count_list == [1,1,2]:
            total_num = 13 - len(count_list)
            return total_num * 4
        # XYZA
        if count_list == [1,1,1,1]:
            # each card can be a pair
            return len(count_list) * math.comb(3,1)
        # XXY
        if count_list == [1,2]:
            return math.comb(13 - len(count_list), 2) * (math.comb(4,1) ** 2)
        # XYZ
        if count_list == [1,1,1]:
            # all pair combo
            pair_freq = (13 - len(count_list)) * math.comb(4,2)
            # prob of choosing X/Y/Z and 1 other card
            choose_finish_pair = math.comb(3,1)
            choose_last_card = (13 - len(count_list)) * math.comb(4,1)
            finish_pair_freq = choose_finish_pair * choose_last_card

            # 3x finish pair freq because either X/Y/Z can be pair
            return pair_freq + 3 * (finish_pair_freq)
        # XX
        if count_list == [2]:
            random_three_num = math.comb(12,3) * (math.comb(4,1) ** 3)
            return random_three_num
        # XY
        if count_list == [1,1]:
            # draw x and 2 random num
            draw_one_from_three = math.comb(3,1)
            random_two_num = math.comb(11,2) * (math.comb(4,1) ** 2)
            freq_1 = draw_one_from_three * random_two_num
            # draw y and 2 random num
            # same as freq_1
            # draw pair and z
            draw_pair = math.comb(11,1) * (math.comb(4,2))
            random_num = math.comb(10,1) * math.comb(4,1)
            freq_2 = draw_pair * random_num

            return (2 * freq_1) + freq_2
        # X
        if count_list == [1]:
            # draw x and 3 random num
            draw_x = math.comb(3,1)
            random_three_num = math.comb(12,3) * (math.comb(4,1) ** 3)
            freq_1 = draw_x * random_three_num
            # draw pair and 2 random num
            draw_pair = math.comb(12,1) * math.comb(4,2)
            random_two_num = math.comb(11,2) * (math.comb(4,1) ** 2)
            freq_2 = draw_pair * random_two_num

            return freq_1 + freq_2

    # endregion calculate total combination of combo per hand

    # region calculate better combo if hand is already a given combo
    # IE: given a pair in hand already - calculate pair combination that are better than current hand

    def calc_total_better_royal_flush_combination(self, given_hand, retained_hand):
        """
        if hand is already royal flush - there is nothing better
        """
        if not self.is_royal_flush(given_hand):
            return 0
        
        return 0

    def calc_total_better_straight_flush_combination(self, given_hand, retained_hand):
        """
        Condition:
        - The combo is better if the combo's highest card > given hand's highest card

        Scenarios:
        - find all consecutive value combo to make straight
        1. retained hand is empty
            - it can be any possible suit, just find all better consecutive combo and multiply it by 4 for each suit
        2. retained hand is not empty
            - depending on the value in hand - it can be limited combo 
            - find number of all consecutive combo and -1 because it will include given_hand combo
        """
        if not self.is_straight_flush(given_hand):
            return 0

        valid_combo = 0

        consecutive_value_combos = [[i, i+1, i+2, i+3, i+4] for i in range(2, 10)]
        given_values = [card.value for card in given_hand]
        retained_values = [card.value for card in retained_hand]

        max_given_val = max(given_values)

        for combo in consecutive_value_combos:
            max_combo_val = max(combo)
            valid = all(val in combo for val in retained_values)
            
            if max_combo_val > max_given_val and valid:
                valid_combo += 1

        if len(retained_hand) == 0:
            return valid_combo * 4

        return valid_combo

    def calc_total_better_four_of_a_kind_combination(self, given_hand, retained_hand):
        """
        Condition:
        - 4 of a kind is rank by its quad than by its kicker

        Scenarios:
        1. retained hand is empty
            - find same quad with better kicker
            - find better quad with any kicker
        2. retained hand is not empty
            - XX(XX)
                - quad is predetermined - find all better kicker
            - XY
                - both values is predetermined - only 1 combination in which kicker num > given_num
            - Y - keep kicker
                - Y is kicker - all better quad
                - Y Can be quad if given kicker > given quad
            - X - keep 1x quad val
                - find all better kicker
                - find all better quad
            - XX(X)Y - can only make the same 4 of a kind 
                - return 0
            
        """
        if not self.is_four_of_a_kind(given_hand):
            return 0
        
        given_value = [card.value for card in given_hand]
        given_quad = None
        given_kicker = None
        for val in set(given_value):
            if given_value.count(val) == 4:
                given_quad = val
            else:
                given_kicker = val

        if len(retained_hand) == 0:
            # find all same quad but better kicker
            num_list = list(range(2,15))
            num_list.remove(given_quad)
            num_list.remove(given_kicker)
            better_kicker_num = [num for num in num_list if num > given_kicker]
            same_quad_better_kicker_freq = len(better_kicker_num) * 4

            # all better quad and any kicker
            num_list = list(range(2,15))
            better_quad_num = [num for num in num_list if num > given_quad]
            # 12 is the remaining num beside quad num ( 13 -1 )
            better_quad_any_kicker_freq = len(better_quad_num) * (12 * 4)

            return same_quad_better_kicker_freq + better_quad_any_kicker_freq

        # retained hand is not empty
        count_list = []
        for val in set([card.value for card in retained_hand]):
            retained_hand_val = [card.value for card in retained_hand]
            count_list.append(retained_hand_val.count(val))

        count_list.sort()

        # keep quad
        # XX(XX)
        if count_list == [2] or count_list == [3] or count_list == [4]:
            num_list = list(range(2,15))
            num_list.remove(given_quad)
            # remaining card is quad
            # find all better kicker num
            better_kicker_num = [num for num in num_list if num > given_kicker]
            better_kicker_freq = len(better_kicker_num) * 4
            return better_kicker_freq  

        # XY
        if count_list == [1,1]:
            if given_kicker > given_quad:
                return 1

        # # keep 1 card - kicker:
        if count_list == [1] and [given_kicker] == [card.value for card in retained_hand]:
            num_list = list(range(2,15))
            num_list.remove(given_kicker)
            # find all better quad
            better_quad = [num for num in num_list if num > given_quad]
            better_quad_freq = len(better_quad)
            # if kicker becomes quad
            kicker_to_quad_freq = 0
            if given_kicker > given_quad:
                kicker_to_quad_freq = 12 * 4
            
            return better_quad_freq + kicker_to_quad_freq
        
        # # keep 1 card - quad
        if count_list == [1] and [given_quad] == [card.value for card in retained_hand]:
            num_list = list(range(2,15))
            num_list.remove(given_quad)
            # find all better kicker
            better_kicker = [num for num in num_list if num > given_kicker]
            better_kicker_freq = len(better_kicker) * 4
            # find all better quad
            better_quad = [num for num in num_list if num > given_quad]
            better_quad_freq = len(better_quad)

            return better_kicker_freq + better_quad_freq

        # for XX(X)Y
        return 0

    def calc_total_better_full_house_combination(self, given_hand, retained_hand):
        """
        Condition:
        - full house is ranked by its triple and then the pair

        Scenarios:
        1. retained hand is empty
            - find same triple with better pair
                - triple can be any combination of the 4 cards
                - possible pair can not include triple num
            - find better triple with any pair
                - find all better triple
                - pair can be ANY pair not including 
        2. retained hand is not empty
            - XXXY
                - triple is predetermined
                - all val is predetermined
                - can only be the same full house as given hand
            - XXYY
                - all val is predetermined
                - either X or Y is triple
                - if X is triple - it will be the same full house as given_hand 
                -  Y can be triple if Y > X
            - XXX
                - find better pair
            - XXY or XYY
                - all val is predetermined
                - either X or Y is triple
            - XX or YY / X or Y is essentially the same scenario
                - only 1 val is predetermined - can be triple or pair
                - Y can be triple if Y > X
                - math.comb() change depending on how many X or Y there is already
            - XY
                - 1 better combination if pair val > triple val

        """
        if not self.is_full_house(given_hand):
            return 0
        
        given_values = [card.value for card in given_hand]
        given_triple = None
        given_pair = None
        for val in set(given_values):
            if given_values.count(val) == 3:
                given_triple = val
            else:
                given_pair = val

        if len(retained_hand) == 0:
            num_list = list(range(2,15))
            # find all better triple - all better triple can match with ANY pair
            better_triple = [num for num in num_list if num > given_triple]
            better_triple_freq = len(better_triple) * math.comb(4,3)
            any_pair = 12 * math.comb(4,2)
            better_full_house_freq_a = better_triple_freq * any_pair
            # find all better pair - triple stay the same but pair is better
            same_triple = math.comb(4,3)
            num_list.remove(given_triple)
            better_pair = [num for num in num_list if num > given_pair]
            better_pair_freq = len(better_pair) * math.comb(4,2)
            better_full_house_freq_b = same_triple * better_pair_freq

            return better_full_house_freq_a + better_full_house_freq_b
            

        count_list = []

        retained_hand_val = [card.value for card in retained_hand]
        for val in set(retained_hand_val):
            count_list.append(retained_hand_val.count(val))

        count_list.sort()

        # XXXY
        if count_list == [1,3]:
            return 0
        # XXYY
        if count_list == [2,2]:
            if given_pair > given_triple:
                return math.comb(2,1)
            else:
                return 0
        # XXX
        if count_list == [3]:
            num_list = list(range(2,15))
            num_list.remove(given_triple)
            better_pair_num = [num for num in num_list if num > given_pair]
            return len(better_pair_num) * math.comb(4,2)
        # XXY or XYY
        if count_list == [1,2]:
            if given_pair > given_triple:
                num_triple = retained_hand_val.count(given_triple)
                num_pair = retained_hand_val.count(given_pair)
                # reverse the num_pair and num_triple because we are testing scenario where the pair becomes the triple
                choose_triple = math.comb(4 - num_pair, 3 - num_pair)
                choose_pair = math.comb(4 - num_triple, 2 - num_triple)
                return choose_triple * choose_pair
            else:
                return 0
        # XX or YY / X or Y
        if count_list == [2] or count_list == [1]:
            # XX / X
            if given_triple == retained_hand_val[0]:
                num_x = retained_hand_val.count(given_triple)
                num_list = list(range(2,15))
                # X is triple
                choose_x = math.comb(4 - num_x, 3 - num_x)
                num_list.remove(given_triple)
                better_pair = [num for num in num_list if num > given_pair]
                better_pair_freq = len(better_pair) * math.comb(4,2)
                better_freq_a = choose_x * better_pair_freq
                # X is pair
                better_triple = [num for num in num_list if num > given_triple]
                better_triple_freq = len(better_triple) * math.comb(4,3)
                better_freq_b = better_triple_freq * math.comb(4- num_x, 2- num_x)

                return better_freq_a + better_freq_b
            # YY / Y
            if given_pair == retained_hand_val[0]:
                # Y is still pair
                num_y = retained_hand_val.count(given_pair)
                num_list = list(range(2,15))
                # better triple
                num_list.remove(given_pair)
                better_triple = [num for num in num_list if num > given_triple]
                better_triple_freq = len(better_triple) * math.comb(4,3)
                better_freq_a = better_triple_freq * math.comb(4 - num_y, 2 - num_y)
                # Y can be triple if Y > X
                better_freq_b = 0
                if given_pair > given_triple:
                    choose_y_triple = math.comb(4 - num_y, 3 - num_y)
                    any_pair = 12 * math.comb(4,2)
                    better_freq_b = choose_y_triple * any_pair
                
                return better_freq_a + better_freq_b
        # XY
        if count_list == [1,1]:
            # Y is triple and X is pair - only possible if Y > X
            if given_pair > given_triple:
                choose_y_triple = math.comb(3,2)
                choose_x_pair = math.comb(3,1)
                return choose_y_triple * choose_x_pair
            # X is triple and Y is pair - same full house as given hand
            else:
                return 0
        
    def calc_total_better_flush_combination(self, given_hand, retained_hand):
        """
        Condition:
        - all same suit 
        - rank by the highest value to lowest value 

        scenario 1 - did retained card:
            1. create find the mulligan card list
            2. find all possible num card that can be draw
            - The retained_value will be in both the given hand and the new mulligan hand - so you can think of them canceling each other out
            4. generate all combination of card draws
            5. compare both mulligan list and the draw list
            6. remove any straight flush combo
            7. suit is predetermined since we did retained card
        scenario 2 - retained no card:
            1. create find the mulligan card list
            2. find all possible num card that can be draw
            - The retained_value will be in both the given hand and the new mulligan hand - so you can think of them canceling each other out
            4. generate all combination of card draws
            5. compare both mulligan list and the draw list
            6. remove any straight flush combo
            7. suit is NOT predetermined so take the combination * 4

        Example since this logic might be difficult to follow:
        - given_value = [11,10,8,5,4]
        - retained_value = [10,5,4]
        - mulligan_value = [11,8]
        - card that can be draw from deck = [14,13,12,11,9,8,7,6,3,2]
        - need to find two scenarios, 2 for length of mulligan_value
            - (num > 11) + any num
            - (num > 11) + (num > 8)

        # example with ACTUAl numbers
        - only compare mulligan_value with possible draw value
            - example of 4 combinations
                - [14,3]
                - [11,9]
                - [11,3]
                - [3,2]

        - for each of the possible combination - you just need to compare the mulligan value with the possible combination's value to check if it is better
        - [14,3] compare with [11,8]
            - 14 > 8 (so it is a better flush)
            - new draw - [14,10,5,4,3] vs given - [11,10,8,5,4]
        - [11,9] compare with [11,8]
            - 11 = 11 -> compare 9 > 8 (so it is a better flush)
            - new draw - [11,10,9,5,4] vs given - [11,10,8,5,4]
        - [11,3] compare with [11,8]
            - 11 = 11 -> compare 3 < 8 (so it is NOT a better flush)
            - new draw - [11,10,5,4,3] vs given - [11,10,8,5,4]
        - [3,2] compare with [11,8]
            - 3 < 11 (so it is NOT a better flush)
            - new draw - [10,5,4,3,2] vs given - [11,10,8,5,4]

            
        Based on the above example [i,j] - you can see the pattern of needing to find any combination of number where :
            - num > i and j can be any number because if num > i, it is already a better flush combo
            - num = i and num2 > j 
            - num < i - never a better combo

        """
        if not self.is_flush(given_hand):
            return 0

        # setup - find all possible valid card draw
        given_values = [card.value for card in given_hand]
        retained_values = [card.value for card in retained_hand]
        mulligan_values = [num for num in given_values if num not in retained_values]
        mulligan_values.sort(reverse=True)

        num_in_deck = list(range(2,15))
        for num in retained_values:
            num_in_deck.remove(num)

        # filter out the better card draw
        all_better_flush = 0

        num_card_to_draw = len(mulligan_values)

        all_card_draw_combination = itertools.combinations(num_in_deck, num_card_to_draw)
        all_card_draw_combination = [list(combo) for combo in all_card_draw_combination]

        for combo in all_card_draw_combination:
            combo.sort(reverse=True)
            for i in range(num_card_to_draw):
                if combo[i] > mulligan_values[i]:
                    all_better_flush += 1
                    break
                if combo[i] < mulligan_values[i]:
                    break

        # remove straight flush
        all_possible_straight_flush_and_royal = 0
        consecutive_value_combos = [[i, i+1, i+2, i+3, i+4] for i in range(2, 11)]

        # sort combo so they can compare
        [combo.sort(reverse=True) for combo in consecutive_value_combos]
        given_values.sort(reverse=True)

        for combo in consecutive_value_combos:
            # check if the straight flush is even possible with retained hand
            if all(val in combo for val in retained_values):
                # actual check if the straight flush would be considered a better flush than current flush
                for i in range(5):
                    if combo[i] > given_values[i]:
                        all_possible_straight_flush_and_royal += 1
                        break
                    if combo[i] < given_values[i]:
                        break

        if len(retained_hand) == 0:
            return (all_better_flush - all_possible_straight_flush_and_royal) * 4
        
        return all_better_flush - all_possible_straight_flush_and_royal

    def calc_total_better_straight_combination(self, given_hand, retained_hand):
        """
        Condition:
        - straight is ranked by the highest card of the combo
        - exclude straight flush
        - include royal value in combo [10,J,Q,K,A]

        Scenario:
        1. did not retained card
            - find all better valid combo - compare the highest card in the given hand's combo with each valid combo's highest card
            - make sure to exclude all straight flush
                - num of straight flush is calc by taking all_better_valid_combo * 4 for each suit
        2. retained card
            - find all better valid combo - compare the highest card in the given hand's combo with each valid combo's highest card
            - make sure the better valid combo will contains all of the value in retained hand
            - make sure to exclude all straight flush (if retained_hand is same suit)
                - num of straight flush is calc by taking len(all_better_valid_combo) since there is already a predetermined suit - it can only have 1 straight flush combo
        """
        if not self.is_straight(given_hand):
            return 0
        
        consecutive_value_combos = [[i, i+1, i+2, i+3, i+4] for i in range(2, 11)]
        
        given_hand_value = [card.value for card in given_hand]

        all_better_valid_combo = []

        for combo in consecutive_value_combos:
            retained_hand_val = [card.value for card in retained_hand]
            if max(combo) > max(given_hand_value) and all(num in combo for num in retained_hand_val):
                all_better_valid_combo.append(combo) 
        num_card_missing = 5 - len(retained_hand)
        output = len(all_better_valid_combo) * (4 ** num_card_missing)

        # remove all straight flush combo - can be 4 for each suit
        if len(retained_hand) == 0:
            return output - (len(all_better_valid_combo) * 4)
        
        # remove all straight flush combo
        if self.is_same_suit(retained_hand):
            return output - len(all_better_valid_combo)
        
        return output

    def calc_total_better_three_of_a_kind_combination(self, given_hand, retained_hand):
        """
        Condition:
        - 3 of a kind is ranked by
            - triple
            - if triple is the same - rank by its highest kicker
            - if the above is the same - rank by its lowest kicker
        Use the same method to compare the kicker as flush combo

        Scenario:
        1. did not retained card [X,X,X,Y,Z]
            - find all combination where 
                - drawn triple > given_triple
                - any high kicker + low kicker 
            - find all combination where
                - drawn triple == given triple
                - drawn high kicker > given high kicker
                - any low kicker
            - find all combination where
                - drawn triple == given_triple
                - drawn high kicker == given high kicker
                - draw low kicker > given low kicker
            - sum all combination
        2. retained card
            - XX(X)(Y/Z)
                - triple is predetermined
                - find better kicker
            - XYZ
                - all 3 number is predetermined
                - if triple same - no better kicker
                - if Y > X - Y can be triple
                - if Z > X - Z can be triple
                - sum all possibilities
            - XY / XZ
                - 2 num is predetermined
                - X is triple + Y is kicker
                - if Y > X or Z > X - it can be triple + X is kicker
                - find all better triple val  + XY/XZ as kicker
                - sum all possibilities
            - X/Y/Z
                - 1 num is predetermined
                - retained card is triple
                - retained card is high kicker
                - retained card is low kicker

        """
        if not self.is_three_of_a_kind(given_hand):
            return 0

        given_values = [card.value for card in given_hand]
        retained_values = [card.value for card in retained_hand]
        given_triple = None
        given_kicker = []

        for val in set(given_values):
            if given_values.count(val) == 3:
                given_triple = val
            if given_values.count(val) == 1:
                given_kicker.append(val)

        given_kicker.sort(reverse=True)

        num_list = list(range(2,15))
        num_list = [num for num in num_list if num not in retained_values]

        better_triple_num = [num for num in num_list if num > given_triple]

        if len(retained_hand) == 0:
            num_in_deck = num_list[:]
            # all better triple + any kicker 
            better_triple = len(better_triple_num) * math.comb(4,3)
            any_kicker = math.comb(len(num_in_deck) - 1, 2) * (math.comb(4,1)**2)
            better_triple_freq = better_triple * any_kicker

            # same triple + better kicker
            num_in_deck.remove(given_triple)

            choose_triple = math.comb(4,3)
            kicker_combo = itertools.combinations(num_in_deck,2)
            better_kicker_list = []

            for combo in kicker_combo:
                combo_list = list(combo)
                combo_list.sort(reverse=True)

                if combo_list[0] > given_kicker[0]:
                    better_kicker_list.append(combo_list)
                if combo_list[0] == given_kicker[0] and combo_list[1] > given_kicker[1]:
                    better_kicker_list.append(combo_list)

            better_kicker_freq = choose_triple * len(better_kicker_list) * (math.comb(4,1)**2)

            return better_triple_freq + better_kicker_freq
        
        # retained card logic
        mulligan_kicker = [num for num in given_values if num not in retained_values and num != given_triple]
        mulligan_kicker.sort(reverse=True)
        count_list = []

        for val in set(retained_values):
            count_list.append(retained_values.count(val))
        
        count_list.sort()

        # XXX XXXY XXXZ XX XXY XXZ
        if 2 in count_list or 3 in count_list:
            # find better kicker by comparing mulligan_kicker with new draw kicker
            better_kicker = 0
            num_in_deck = list(range(2,15))
            [num_in_deck.remove(num) for num in set(retained_values)]
            all_draw_combo = itertools.combinations(num_in_deck, len(mulligan_kicker))
            for draw in all_draw_combo:
                draw_list = list(draw)
                draw_list.sort(reverse=True)
                for i in range(len(draw_list)):
                    if draw_list[i] > mulligan_kicker[i]:
                        better_kicker += 1
                        break
                    if draw_list[i] < mulligan_kicker[i]:
                        break

            better_kicker_freq = better_kicker * math.comb(4,1)**len(mulligan_kicker)

            if 2 in count_list:
                choose_x = math.comb(2,1)
                return choose_x * better_kicker_freq
            else:
                return better_kicker_freq
        
        # XYZ
        if count_list == [1,1,1]:
            freq = 0
            for val in given_kicker:
                if val > given_triple:
                    freq += math.comb(3,2)
            
            return freq
        
        # XY XZ YZ
        if count_list == [1,1]:
            retained_values.sort(reverse=True)
            # card 1 - triple, card 2 kicker
            freq_a = 0   

            if retained_values[0] > given_triple:
                choose_triple = math.comb(3,2)
                any_kicker = math.comb(len(num_list),1) * math.comb(4,1)

                freq_a = choose_triple * any_kicker

            if retained_values[0] == given_triple:
                # choose 2 from 3 because 1 card is already chosen
                choose_triple = math.comb(3,2)
                better_kicker = []
                for num in num_list:
                    kicker = [retained_values[1], num]
                    kicker.sort(reverse=True)

                    if kicker[0] > given_kicker[0]:
                        better_kicker.append(kicker)
                    if kicker[0] == given_kicker[0] and kicker[1] > given_kicker[1]:
                        better_kicker.append(kicker)
                
                # math.comb(4,1) instead of math.comb(4,1)**2 because 1 card is already chosen
                freq_a = choose_triple * (len(better_kicker) * (math.comb(4,1)))

            # card 2 - triple, card 1 kicker
            freq_b = 0
            if retained_values[1] > given_triple:
                choose_triple = math.comb(3,2)
                any_kicker = math.comb(len(num_list),1) * math.comb(4,1)

                freq_b = choose_triple * any_kicker

            if retained_values[1] == given_triple:
                choose_triple = math.comb(3,2)
                better_kicker = []
                for num in num_list:
                    kicker = [retained_values[0], num]
                    kicker.sort(reverse=True)

                    if kicker[0] > given_kicker[0]:
                        better_kicker.append(kicker)
                    if kicker[0] == given_kicker[0] and kicker[1] > given_kicker[1]:
                        better_kicker.append(kicker)
                # math.comb(4,1) instead of math.comb(4,1)**2 because 1 card is already chosen
                freq_b = choose_triple * (len(better_kicker) * (math.comb(4,1)))

            # both card kicker - find better triple
            freq_c = len(better_triple_num) * math.comb(4,3)

            return freq_a + freq_b + freq_c

        # X Y Z
        if count_list == [1]:
            # X
            if retained_values[0] == given_triple:
                # card is triple + better kicker
                choose_x = math.comb(3,2)
                better_kicker = 0
                kicker_combo = itertools.combinations(num_list, 2)
                for kicker in kicker_combo:
                    kicker_list = list(kicker)
                    kicker_list.sort(reverse=True)
                    if kicker_list[0] > given_kicker[0]:
                        better_kicker += 1
                    if kicker_list[0] == given_kicker[0] and kicker_list[1] > given_kicker[1]:
                        better_kicker += 1
                
                freq_a = choose_x * (better_kicker * (math.comb(4,1)**2))

                # card is kicker - better triple + any kicker with X
                better_triple_freq = len(better_triple_num) * math.comb(4,3)
                any_kicker = math.comb(len(num_list) - 1, 1) * (math.comb(4,1))

                freq_b = better_triple_freq * any_kicker

                return freq_a + freq_b
            # Y Z
            if retained_values[0] in given_kicker:
                # card is triple
                freq_a = 0
                if retained_values[0] > given_triple:
                    choose_x = math.comb(3,2)
                    any_kicker = math.comb(len(num_list), 2) * (math.comb(4,1)**2)

                    freq_a = choose_x * any_kicker

                # card is kicker
                freq_b = 0

                # better triple
                better_triple = len(better_triple_num) * math.comb(4,3)
                better_triple_freq = better_triple * math.comb(len(num_list) - 1, 1) * math.comb(4,1)

                # same triple + better kicker
                same_triple = math.comb(4,3)
                better_kicker = 0
                num_in_deck = num_list
                num_in_deck.remove(given_triple)

                for num in num_in_deck:
                    kicker = [retained_values[0], num]
                    kicker.sort(reverse=True)
                    if kicker[0] > given_kicker[0]:
                        better_kicker += 1
                    if kicker[0] == given_kicker[0] and kicker[1] > given_kicker[1]:
                        better_kicker += 1
                
                same_triple_freq = same_triple * (better_kicker * math.comb(4,1))

                freq_b = better_triple_freq + same_triple_freq

                return freq_a + freq_b

    def calc_total_better_two_pairs_combination(self, given_hand, retained_hand):
        """
        Conditions:
        - 2 pairs is ranked by
            - highest pair 
            - lowest pair
            - kicker
        Use the same method to compare the pairs as flush combo

        Scenario:
        - no retained card in hand
            - find same pair + better kicker
            - find better pair combo + any kicker
        - retained card in hand
            - XXYY
                - pair is predetermined
                - find better kicker
            - XXYZ
                - all values is predetermined
                - 1 pair is predetermined
                - calc all better combination where Y/Z becomes pair
            - XYZ
                - all values is predetermined
                - find all freq where kicker is promoted to pair and one of the pair is demoted to kicker
                    - Z > Y and Z > X
            - XXY XXZ YYX YYZ
                - 1 pair is predetermined
                - better combination where single becomes pair
                    - if single form same pair as given hand - find better kicker
                    - if single form better pair as given hand - find all kicker
                    - single stay as kicker - find all better pair
            - XX YY
                - same pair + better kicker
                - better pair + any kicker
            - XY XZ YZ
                - both card becomes pair 
                    - if pairs is same as given hand - only find better kicker
                    - if pair is better than given hand - find all kicker
                - 1 card becomes pair + any kicker
            - X Y Z
                - num is pair
                    - same pair as given hand - find better kicker
                    - better pair as given hand - any kicker
                - num is kicker
                    - find better pairs combo
            
        """
        if not self.is_two_pair(given_hand):
            return 0
        
        given_values = [card.value for card in given_hand]
        retained_values = [card.value for card in retained_hand]
        given_pair = []
        given_kicker = None

        for val in set(given_values):
            if given_values.count(val) == 2:
                given_pair.append(val)
            if given_values.count(val) == 1:
                given_kicker = val

        given_pair.sort(reverse=True)

        num_list = [num for num in list(range(2,15)) if num not in retained_values]

        # no retained card logic
        if len(retained_hand) == 0:
            # same pairs + better kicker
            choose_pairs = math.comb(4,2)**2
            num_in_deck = num_list[:]
            num_in_deck.remove(given_pair[0])
            num_in_deck.remove(given_pair[1])   

            better_kicker = [num for num in num_in_deck if num > given_kicker]
            better_kicker_freq = len(better_kicker) * math.comb(4,1)

            freq_a = choose_pairs * better_kicker_freq
            # better pairs + any kicker
            better_pairs = 0
            pair_combo = itertools.combinations(num_list, 2)
            for combo in pair_combo:
                combo_list = list(combo)
                combo_list.sort(reverse=True)
                if combo_list[0] > given_pair[0] or (combo_list[0] == given_pair[0] and combo_list[1] > given_pair[1]):
                    better_pairs += 1

            better_pairs_freq = better_pairs * (math.comb(4,2)**2)

            num_in_deck = num_list[:]
            any_kicker = (len(num_in_deck) - 2) * math.comb(4,1)
            freq_b = better_pairs_freq * any_kicker

            return freq_a + freq_b
        
        # retained card logic
        count_list = []
        for val in set(retained_values):
            count_list.append(retained_values.count(val))
        
        count_list.sort()
        # XXYY - 2 pair is predetermined
        if count_list == [2,2]:
            # find better kicker
            better_kicker = [num for num in num_list if num > given_kicker]
            return len(better_kicker) * math.comb(4,1)

        # XXYZ - all value is predetermined
        if count_list == [1,1,2]:
            y_val = None
            for val in given_pair:
                if retained_values.count(val) == 1:
                    y_val = val
            if given_kicker > y_val:
                return math.comb(3,1)
            return 0

        # XYZ - all value is predetermined
        if count_list == [1,1,1]:
            pair_combo = itertools.combinations(set(retained_values),2)

            better_pair = 0
            for combo in pair_combo:
                combo_list = list(combo)
                combo_list.sort(reverse=True)
                single = [num for num in retained_values if num not in combo_list][0]
                for i in range(2):
                    if combo_list[i] > given_pair[i]:
                        better_pair += 1
                        break
                    if combo_list[i] < given_pair[i]:
                        break
                
            return better_pair * (math.comb(3,1)**2)

        # XXY XXZ YYX YYZ
        if count_list == [1,2]:
            mulligan_pair = [num for num in given_pair if retained_values.count(num) != 2][0]
            single = [num for num in retained_values if retained_values.count(num) == 1][0]

            # single card becomes pair
            freq_a = 0
            if single == mulligan_pair:
                choose_single = math.comb(3,1)
                better_kicker = [num for num in num_list if num > given_kicker]
                freq_a = choose_single * (len(better_kicker) *  math.comb(4,1))
            if single > mulligan_pair:
                choose_single = math.comb(3,1)
                any_kicker = len(num_list) * math.comb(4,1)
                freq_a = choose_single * any_kicker

            # choose better pair
            better_pair = [num for num in num_list if num > mulligan_pair]
            freq_b = len(better_pair) * math.comb(4,2)

            return freq_a + freq_b

        # XX YY
        if count_list == [2]:
            # same pair + better kicker
            freq_a = 0
            choose_pair = math.comb(4,2)

            better_kicker = [num for num in num_list if num > given_kicker and num not in given_pair]

            freq_a = choose_pair * (len(better_kicker) * math.comb(4,1))
            # better pair + any kicker
            freq_b = 0
            mulligan_pair = [num for num in given_pair if retained_values.count(num) != 2][0]

            better_pair = [num for num in num_list if num > mulligan_pair]
            better_pair_freq = len(better_pair) * math.comb(4,2)
            any_kicker = (len(num_list) - 1) * math.comb(4,1)

            freq_b = better_pair_freq * any_kicker

            return freq_a + freq_b
        
        # XY XZ YZ
        if count_list == [1,1]:
            # retained single both becomes pair
            freq_a = 0
            # if retained hand is the pair - only find better kicker
            retained_values.sort(reverse=True)
            if retained_values == given_pair:
                choose_pair = math.comb(3,1)**2
                better_kicker = [num for num in num_list if num not in given_pair and num > given_kicker]

                freq_a = choose_pair * len(better_kicker) * math.comb(4,1)
            else:
                better_pair = 0
                for i in range(2):
                    if retained_values[i] > given_pair[i]:
                        better_pair += 1
                        break
                    if retained_values[i] < given_pair[i]:
                        break
                
                better_pair_freq = better_pair * (math.comb(3,1)**2)
                any_kicker = len(num_list) * math.comb(4,1)

                freq_a = better_pair_freq * any_kicker
            # 1x retained single becomes pair + any better pair
            freq_b = 0
            better_pair = 0
            pair_combo = itertools.product(num_list, retained_values)
            for combo in pair_combo:
                combo_list = list(combo)
                combo_list.sort(reverse=True)
                for i in range(2):
                    if combo_list[i] > given_pair[i]:
                        better_pair += 1
                        break
                    if combo_list[i] < given_pair[i]:
                        break

            freq_b = better_pair * math.comb(4,2) * math.comb(3,1)
            return freq_a + freq_b
        
        if count_list == [1]:
            # num is pair
            freq_a = 0
            retained_values.sort(reverse=True)
            for num in num_list:
                pair_combo = [num, retained_values[0]]
                pair_combo.sort(reverse=True)
                choose_pair = math.comb(4,2) * math.comb(3,1)
                any_kicker_freq = (len(num_list) - 1) * math.comb(4,1)

                # only include better kicker
                if pair_combo == given_pair:
                    better_kicker = [num for num in num_list if num > given_kicker and num not in given_pair]
                    better_kicker_freq = len(better_kicker) * math.comb(4,1)

                    freq_a += (choose_pair * better_kicker_freq)
                else:
                    # include any kicker
                    for i in range(2):
                        if pair_combo[i] > given_pair[i]:
                            freq_a += (choose_pair * any_kicker_freq)
                            break
                        if pair_combo[i] < given_pair[i]:
                            break

            # num is kicker  
            better_pair = 0
            pair_combo = itertools.combinations(num_list,2)

            for combo in pair_combo:
                combo_list = list(combo)
                combo_list.sort(reverse=True)
                for i in range(2):
                    if combo_list[i] > given_pair[i]:
                        better_pair += 1
                        break
                    if combo_list[i] < given_pair[i]:
                        break

            freq_b = better_pair * (math.comb(4,2)**2)

            return freq_a + freq_b
                
    def calc_total_better_one_pair_combination(self, given_hand, retained_hand):
        """
        Condition:
        - pair is ranked by
            - pair
            - if pair is the same - rank by its highest kicker to lowest kicker
        Use the same method to compare the kicker as flush combo
        
        Scenario:
        1. player didn't retained card:
            - all better pair + any kicker 
            - same pair + any kicker
        2. player did retained card:
            - XX(Y)(Z)(A)
                - pair is predetermined
                - find better kicker
            - XYZA
                - all value is predetermined
                - pair is either X Y Z or A
            - all other combinations
                - same pair + better kicker
                - retained kicker card becomes pair
                - all better pair + any kicker combination
        """
        if not self.is_one_pair(given_hand):
            return 0
        
        given_values = [card.value for card in given_hand]
        retained_values = [card.value for card in retained_hand]
        given_pair = None
        given_kicker = []

        for val in set(given_values):
            if given_values.count(val) == 2:
                given_pair = val
            if given_values.count(val) == 1:
                given_kicker.append(val)

        given_kicker.sort(reverse=True)

        num_list = list(range(2,15))
        num_list = [num for num in num_list if num not in retained_values]

        better_pair_num = [num for num in num_list if num > given_pair]

        if len(retained_hand) == 0:
            num_in_deck = num_list[:]
            # all better pair + any kicker 
            better_pair = len(better_pair_num) * math.comb(4,2)
            any_kicker = math.comb(len(num_in_deck) - 1, 3) * (math.comb(4,1)**3)
            better_pair_freq = better_pair * any_kicker

            # same pair + better kicker
            num_in_deck.remove(given_pair)

            choose_pair = math.comb(4,2)
            kicker_combo = itertools.combinations(num_in_deck,3)
            better_kicker = 0

            for combo in kicker_combo:
                combo_list = list(combo)
                combo_list.sort(reverse=True)

                for i in range(len(combo_list)):
                    if combo_list[i] > given_kicker[i]:
                        better_kicker += 1
                        break
                    if combo_list[i] < given_kicker[i]:
                        break

            better_kicker_freq = choose_pair * better_kicker * (math.comb(4,1)**3)

            return better_pair_freq + better_kicker_freq
        
        # retained card logic
        mulligan_kicker = [num for num in given_values if num not in retained_values and num != given_pair]
        mulligan_kicker.sort(reverse=True)
        count_list = []

        for val in set(retained_values):
            count_list.append(retained_values.count(val))
        
        count_list.sort()
        # XX XXY XXZ XXA XXYZ XXYA XXZA 
        if 2 in count_list:
            draw_num = 5 - len(retained_hand)
            redraw_kicker = itertools.combinations(num_list, draw_num)
            better_kicker = 0

            for kicker in redraw_kicker:
                kicker_list = list(kicker)
                kicker_list.sort(reverse=True)
                for i in range(len(kicker_list)):
                    if kicker_list[i] > mulligan_kicker[i]:
                        better_kicker += 1
                        break
                    if kicker_list[i] < mulligan_kicker[i]:
                        break

            return better_kicker * (math.comb(4,1)**draw_num)
        
        # XYZA
        if count_list == [1,1,1,1]:
            freq = 0
            for val in retained_values:
                if val > given_pair:
                    freq += math.comb(3,1)
            return freq

        # all other where count_list = [1], [1,1], [1,1,1]

        # same pair but better kicker
        num_in_deck = num_list[:]
        if given_pair in retained_values:
            choose_pair = math.comb(3,1)
            draw_num = 5 - len(retained_hand) - 1
        else:
            choose_pair = math.comb(4,2)
            draw_num = 5 - len(retained_hand) - 2
            num_in_deck.remove(given_pair)

        better_kicker = 0
        redraw_kicker = itertools.combinations(num_in_deck, draw_num)
        for redraw in redraw_kicker:
            redraw_list = list(redraw)
            redraw_list.sort(reverse=True)
            for i in range(len(redraw_list)):
                if redraw_list[i] > mulligan_kicker[i]:
                    better_kicker += 1
                    break
                if redraw_list[i] < mulligan_kicker[i]:
                    break
        
        freq_a = choose_pair * (better_kicker * math.comb(4,1)**draw_num)
        # Y/Z/A - retained card becomes pair
        freq_b = 0
        for val in retained_values:
            # val is pair
            if val > given_pair:
                # setup - draw 1 more val and decrease draw_num by 1
                choose_pair = math.comb(3,1)
                # -1 - draw extra card to form pair
                draw_num = 5 - len(retained_hand) - 1

                any_kicker = math.comb(len(num_list), draw_num) * (math.comb(4,1)**draw_num)

                freq_b += choose_pair * any_kicker

        # any other better pair + any kicker where better pair num not in retained_value
        num_in_deck = num_list[:]
        choose_pair = math.comb(4,2)
        better_pair_freq = len(better_pair_num) * math.comb(4,2)

        # -2 - because drew pair
        draw_num = 5 - len(retained_hand) - 2
        any_kicker = math.comb(len(num_list) - 1, draw_num) * (math.comb(4,1)**draw_num)

        freq_c = better_pair_freq * (any_kicker)

        return freq_a + freq_b + freq_c

    def calc_total_better_high_card_combination(self, given_hand, retained_hand):
        """
        Condition:
        high card are ranked by 
        - highest to lowest val

        1. generate all possible card draw 
        2. check if card draw is a straight and if it is a better val combo than given hand
        3. calc all better combinations with suit variation
        4. count for flushes
            - if no card in retained hand
                - remove 4 * number of better combos
            - if retained hand is all same suit and there is retained card in hand
                - remove number of better combos
            - if retained hand is not empty and they are different suit
                - return step 3
        """
        if not self.is_high_card(given_hand):
            return 0
        
        # setup - find all possible valid card draw
        given_values = [card.value for card in given_hand]
        retained_values = [card.value for card in retained_hand]
        given_values.sort(reverse=True)

        num_list = list(range(2,15))
        for num in retained_values:
            num_list.remove(num)

        num_card_to_draw = 5 - len(retained_values)
        better_num_combo = 0

        consecutive_value_combos = [[i, i+1, i+2, i+3, i+4] for i in range(2, 11)]
        [combo.sort(reverse=True) for combo in consecutive_value_combos]

        all_num_combo = itertools.combinations(num_list, num_card_to_draw)
        for combo in all_num_combo:
            combo_list = list(combo)
            hand = retained_values +  combo_list
            hand.sort(reverse=True)
            # remove straight
            straight = hand in consecutive_value_combos

            if not straight:
                for i in range(5):
                    if hand[i] > given_values[i]:
                        better_num_combo += 1
                        break
                    if hand[i] < given_values[i]:
                        break
        
        # all freq with suit
        freq = better_num_combo * (math.comb(4,1)**num_card_to_draw)
        # remove flushes

        # each num combinations would have 4 flush variation
        if len(retained_hand) == 0:
            return freq - (better_num_combo * 4)
        # if retained hand is all same suit, it has 1 flush variation for each num combinations
        elif self.is_same_suit(retained_hand):
            return freq - better_num_combo

        return freq

    # endregion calculate better combo if hand is already a given combo

