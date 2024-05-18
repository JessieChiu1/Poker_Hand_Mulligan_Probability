# The puzzle

**This was originally a coding challenge I completed!**

## Instructions

Imagine you are given a deck of playing cards (a regular 52 card deck), which is shuffled face down. Then you draw five cards off the top. That hand is a 5-card poker hand.

Now imagine you are allowed to place any number of your 5 cards back into the deck, shuffle the deck, and redraw that many cards for a chance at a better hand.

Your task is to write a function which outputs the following information (in whatever format you desire):

 - what is the optimal selection of cards to mulligan (discard and redraw)
 - what is the probability that the optimal mulligan will yield a stronger hand than originally drawn

Note: Your work will be graded on clarity of thought, completion, efficiency, and correctness. This is a tough problem, if you would prefer to use statistics rather than compute probabilities your answer will still be accepted, albeit "scored" lower (there are no real numeric scores, but you get it).

## TLDR: Running a Single Scenario
```
py main.py
```
This command will:
1. Generate one poker hand.
2. Calculate the probability of having a better hand for each retained hand scenario.
3. Print the best retained hand and its corresponding better hand probability.

## The Files

**classes:**
1. card.py
2. deck.py
3. player.py

**pytest unit test**
1. test_card.py
2. test_deck.py
3. test_player.py
4. test_specific.py (for testing one hardcoded poker hand draw)

**demo file**
1. main.py (run for single poker hand draw)
2. test.py 
    - option "Y" for 1000 simulated poker draw run
    - option "N" for hardcoded poker draw run
    - option "A" for all 2,598,960 poker draw run

## Libraries Used
- `itertools`: Used for generating iterations.
- `math`: Utilized for calculating combinatorial math and other mathematical functions.
- `pytest`: Employed for running unit test cases.
- `tqdm`: Implemented to display a progress bar during loops, particularly in the `all_iteration` testing function.

## Poker Hand Rankings

For clarity, standard poker hand rankings are referenced below. Note that the steel wheel A-2-3-4-5 is excluded.

1. **Royal Flush**: 10-J-Q-K-A of the same suit.
2. **Straight Flush**: Five consecutive cards of the same suit, excluding the royal flush.
3. **Four of a Kind**: Four cards of the same rank and one additional card (e.g., XXXXY).
4. **Full House**: Three cards of one rank and two of another (e.g., XXXYY).
5. **Flush**: Five cards of the same suit, excluding the above types.
6. **Straight**: Five consecutive cards of different suits.
7. **Three of a Kind**: Three cards of the same rank and two unrelated cards (e.g., XXXYZ).
8. **Two Pairs**: Two sets of two cards of the same rank and one unrelated card (e.g., XXYYZ).
9. **Pair**: Two cards of the same rank and three unrelated cards (e.g., XXYZA).
10. **High Card**: The highest-ranking single card.


## Q1 Part 2

This was a challenging question, requiring breaking down the problem carefully.

I started with Part 2 as it seemed more approachable to me. The objective here is to calculate the numerator and denominator:

\[ \frac{\text{Number of better combinations}}{\text{Total possible combinations}} \]

### 1. Total Possible Combinations

This is a basic probability calculation. Simply find the number of cards still in decks, and the number of cards you need to redraw.

```
math.comb(num_card_in_deck, num_card_redraw)
```

### 2. Number of better combinations
**Note: All methods pertaining to calculating combinations have docstrings with outlined logic. The following sections will only have the overall approach to the problem outlined.**

**There are two main sections of methods for calculating better combinations:**
1. Methods that take a one parameter (retained hand) and calculate all possible combinations you can make for a specific combo.
   - This will have naming convention of `calc_{combo}_total_combination`

```
def calc_four_of_a_kind_total_combination(self, retained_hand):
```
   - Calculate all four of a kind combinations that you can make with retained_hand.
   - **Use Case:** If given hand is any combinations below four of a kind - any four of a kind combinations are better than given hand.

2. Methods that take two parameters (given hand and retained hand) and calculate all possible combinations that are better than the given hand. This is for the scenario where the given hand is the same combination that the method checks for.
   - This will have naming convention of `calc_total_better_{combo}_combination`

```
def calc_total_better_four_of_a_kind_combination(self, given_hand, retained_hand):
```
   - Calculate all four of a kind combinations that you can make with the retained hand that is also better than the given hand.
   - **Use Case:** It is for when the given hand is already a four of a kind combo.

### Example:

Given a two-pair hand:

- Calculate all better two-pair combinations using `calc_total_better_two_pairs_combination`.
- Calculate all combinations superior to two pairs using `calc_{combo}_total_combination` - we can just find all combinations that can be made with retained hand because any of these combo will be better than given hand combo.
    - Three of a kind
    - Straight
    - Flush
    - Full House
    - Four of a kind
    - Straight flush
    - Royal flush

\[ \frac{\text{Sum of the above methods}}{\text{calc total combinations method}} \]

### 3. Method to Filter out Relevant Methods to Run

I will need a method to determine which methods to run.

I achieve this by creating a list of dictionaries, each containing:
```json
{
"name": combo name,
"check": method to verify a specific combo,
"total": method to calculate all possible combinations,
"better": method to calculate better combinations
}

```
The generate_method_list method filters this list based on the given hand. It does so by running the check method, which returns a Boolean indicating whether the given hand matches a specific combo. Then, it slices the list to include only the methods relevant to those combinations.

### 4. Calculating Percentage of Better Combinations

The `calc_percent_of_better_combination` method computes the numerator and denominator as required.

This process has four parts:

1. Identifying which combinations a hand belongs to and thus determining which methods to run.
    - Step 3
2. Calculating the total number of **better** combinations when the given hand is already a specific combination.
    - `calc_total_better_{combo}_combination` + `calc_{superior_combo}_total_combination`
    - Step 2
3. Calculating the total number of specific combinations possible with a retained hand.
    - `calc_{combo}_total_combination`
    - Step 1
4. Returning the probabilities of better combinations for a given retained hand.


## Q1 Part 1

After completing Part 2, the next step is to find all possible retained hand combinations and compare their probabilities of better hands to identify the optimal hand to keep.

### Generating All Retained Hand Combinations and Looping Through Step 4 Part 1
1. Utilize `itertools.combinations` to generate all possible retained hand combinations.
    - Method: `generate_all_retained_hand_combination`
2. Loop through all retained hand combinations and return the retained hand combinations that yield the best percentage of better combinations.
    - Method: `find_best_retained_hand`
    - The `generate_all_retained_hand_combination` method will only require the `given_hand` parameter and will run `generate_method_list` (Step 3 from Part 2) to filter for relevant methods. It will then loop through all retained hand possibilities and run `calc_percent_of_better_combination` (Step 4 Part 2) for each iteration.

**I don't think this method is the best way to calculate the optimal retained hand:**
1. I want to take into account the average winning hand.
    - A better high card combination doesn't matter that much if a high card combination is weaker than the average hand.
2. Adding a weight to each combination would be better. Currently, as long as a pair and a royal flush are better than a given hand, they are both counted as one better combination. However, they are not equivalent. If we added a weight to the combination to better reflect the odds of winning based on the combination's strength, it would provide a more accurate assessment.

## Approach

### Class-Based

I decided to use classes because I find them helpful when brainstorming.

The `Card/Deck` class provides the basic functionality. The core of the functionality lies in the `Player` class, which defines what actions a player can take (draw a card, mulligan, etc.) and what the player can deduce (is this a royal flush, what are the probabilities of drawing certain combos, etc.).

This approach is particularly useful because developing the foundational logic for how a player thinks often leads to insights for the next steps or reveals gaps in logic.
- For example, I initially overlooked double-counting combos, such as including a straight flush in the count for straight combos.

### Common Logic Patterns

1. For consecutive number combinations (straight, straight flush, royal flush):
    - Generating all consecutive number combinations, which total only 9 (excluding the steel wheel), and checking if all cards in the retained hand have values in these combinations is a straightforward way to assess the number of combinations.
  
2. For pair/triple/quad combinations:
    - These combinations have a predetermined number of unique values. When a retained hand is a pair, triple, or quad, it narrows down the possibilities. Thus, creating a `count_list` is generally beneficial.
        - Predetermined number of unique values:
            - For instance, a full house and four of a kind can only have 2 unique values.
        - Predetermined pair/triple/quad:
            - For a full house, if the retained hand contains a triple, then the triple is predetermined. If the retained hand only contains a pair, it could be either a pair or a triple.
    - This approach is akin to Sudoku, where knowing one number in a row/column/square allows you to eliminate other possibilities.
  
3. Focus on checking which of the 13 card values are still valid, rather than what cards remain in the deck. Therefore, creating a `num_list` containing values from [2, 14] is generally a good idea.
    - For example, with a two pairs hand [2, 2, 3, 3, 4]:
        - If the retained hand is [2, 2, 3, 3], we can't draw 2s or 3s, as it would result in a full house. Thus, the relevant `num_list` is [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14].
  
4. When determining **better** combinations where the order of values matters (high card, flushes, kickers in three of a kind, pairs in two pairs, etc.):
    - **Generally**, you can compare the mulligan value with the redraw values.
    
>Example since this logic might be difficult to follow:
given_value = [11,10,8,5,4]
retained_value = [10,5,4]
mulligan_value = [11,8]
card that can be draw from deck = [2,3,6,7,8,9,11,12,13,14]
<br>
**Example with actual numbers: Comparing only the mulligan value with possible redraw values**
Example of 4 redraws:
*(num > 11) + any num*
*(num == 11) + (num > 8)*
<br>
**Example with ACTUAL numbers: Only comparing mulligan value with possible redraw value**
Example of 4 redraw:
    [14,3]
    [11,9]
    [11,3]
    [3,2]
<br>
*For each possible combination, you just need to compare the mulligan value with the combination's value to determine if it's better.*
<br>
**[14,3] compare with [11,8]**
*14 > 8*
*new draw - [14,10,5,4,3] vs given - [11,10,8,5,4]*
<br>
**[11,9] compare with [11,8]**
*11 = 11 -> compare 9 > 8*
*new draw - [11,10,9,5,4] vs given - [11,10,8,5,4]*
<br>
**[11,3] compare with [11,8]**
*11 = 11 -> compare 3 < 8*
*new draw - [11,10,5,4,3] vs given - [11,10,8,5,4]*
<br>
**[3,2] compare with [11,8]**
*3 < 11*
*new draw - [10,5,4,3,2] vs given - [11,10,8,5,4]*
<br>
**Based on the above example [i, j], you can see the pattern of needing to find any combination of numbers where:**
*num > i (and j can be any number)*
*num = i and num2 > j*
*num < i - never a better combo*

## Pytest

Given the complexity, I used Pytest to cross-check my combinatorics math.

Run Pytest with:

```
pytest --vv 
```
I relied on [Wikipedia](https://en.wikipedia.org/wiki/Poker_probability) and [YouTube tutorials](https://www.youtube.com/playlist?list=PL6ZxDcgthxgLWbRPb_x3u_r_260FOsfjO) to refresh my understanding of these concepts.

### Test Case Approach

For all test cases in `test_card.py` and `test_deck.py`, I used hardcoded scenarios.

When testing whether a given hand is a specific combo, I also employed hardcoded test cases.

---
- For any given retained hand, calculate the total number of specific combos that the retained hand can form.
- If the given hand is already a specific combo, calculate the total number of **better** combinations.

To test the two categories of methods mentioned above, I needed a different approach to calculate the total combinations. Since the methods primarily rely on combinatorics mathematics, I chose to iteratively check all possible combinations against a given hand or retained hand for the test cases. All test cases follow the methodologies outlined below:

1. Generate all combinations of combos (all full houses, all high cards, etc.).
    - All combinations undergo a sanity check corresponding to the total number of possible combinations shown on [Wikipedia](https://en.wikipedia.org/wiki/Poker_probability).
  
2. Use a helper function, `hand_in_valid_combination`, to determine which valid combos can be formed with the retained hand.
  
3. When checking for **better** combos, employ a helper function, `find_better_combo`, to filter out combinations that are not superior to the given hand.
  
4. Assert that the number of combos aligns with the combinatorics calculation.

**Note**: Many of the unit testing helper functions feature an optional parameter, `print_result`, to assist in double-checking the combinations I might be overlooking.

I find these test cases incredibly useful, especially when there's an error in my combinatorics calculations. I trust the iterative method to be correct and can work backward from the answer to identify any discrepancies.

Technically, I'm approaching this problem in two ways: iteratively generating all possibilities and comparing them with a given hand, and using combinatorics mathematics. I opted for the class methods to utilize combinatorics because it should theoretically be faster than iteratively generating all possibilities, and I believe it offers a more efficient solution.

### Final Test Case

To ensure thoroughness, I calculated all 2,598,960 poker hand possibilities to determine the best retained hand for each. 
1. This was to identify any probabilities exceeding 100%, which would indicate calculation errors.
2. If any of my calculating combinations functions is returning None, it will result in a error because you can't add None with int type
    - This is to account for scenario that I didn't forsee.

**While I could technically loop through all 2,598,960 poker hands and conduct a unit test for each, simply looping through all poker hands to check for probabilities exceeding 100% already took over 6 hours on my slow computer. Therefore, I decided against this approach.**

```
py test.py
```

`test.py` provides three options:

1. **"Y"** - Generate 1000 (the number can be changed) poker draw scenarios.
  
2. **"N"** - Hardcode a specific test case for focused testing:
    - This is useful when you encounter a particular test case that fails or results in probabilities over 100%.
    - You can encode the scenario in `test_specific.py` to run all test cases related to this poker hand.
    - After resolving the issue, you can rerun this option to ensure everything is corrected.
  
3. **"A"** - Calculate all 2,598,960 poker draw scenarios:
    - Warning: This will take a considerable amount of time.
