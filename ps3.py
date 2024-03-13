# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string
import sys

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 4

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    # Calculates the score of the first component as the SCRABBLE rules say (accounts for the score of each individual letter, as outlined in the dictionary)
    first_component = 0
    word = str.lower(word)
    for letter in word:
        first_component += SCRABBLE_LETTER_VALUES.get(letter)
    
    # Calculates the second component, and sets it to the largest of the two values. The formula for the calculation was provided
    second_component = 0
    wordlen = len(word)
    second_component = max((7 * wordlen) - (3 * (n - wordlen)), 1)

    return first_component * second_component

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    hand['*'] = hand.get('*', 0) + 1

    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    # Makes sure the word is all lowercase and creates a copy of the original hand
    word = str.lower(word)
    new_hand = hand.copy()

    # Make sure the word is valid and generate a dictionary based on the word, which holds the number of letters in each word
    try:
        word_dic = get_frequency_dict(word)
    except:
        print("update_hand(): The provided word is invalid")

    # Decrease the count from each letter in the hand if it is present in the word. If the count would return negative as a result of an invalid word, the count will still be reset to 0 in order to penalize the player
    for key in word_dic.keys():
        if key in new_hand:
            new_hand[key] = max(new_hand.get(key, 0) - word_dic.get(key, 0), 0)
    
    return new_hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word = str.lower(word)

    # First we check if the word can be built using the existing hand - If the player has less letters than what they used, their word will be considered invalid
    for char in word:
        if word.count(char) > hand.get(char, 0):
            return False

    # Check if the word is not in the word list and check for the case in which we have the wildcard character
    if word not in word_list and '*' not in word:
        return False
    elif '*' in word:
        # If we do have the wildcard character, check if we have at least one occurence in the word list that would match the built word (testing using vowels, as the wildcard would replace vowels only)
        count = 0
        for vowel in "aeiou":
            word_cpy = word.replace("*", vowel)
            if word_cpy in word_list:
                count += 1

        # If we have no occurence, invalidate the word
        if count == 0:
            return False

    return True

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    # Return the total size of the player's hand
    hand_length = 0
    for key in hand.keys():
        hand_length += hand[key]
    
    return hand_length

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings!
      returns: the total score for the hand
      
    """

    word = ""
    total_score = 0

    while True:
        hand_length = calculate_handlen(hand)
        if hand_length < 1:
            print(f"Ran out of letters. Total score: {total_score} points")
            break

        print(f"Current hand:", end=' ')
        display_hand(hand)

        word = input("Enter word, or ""!!"" to indicate that you are finished: ")

        if word == '!!':
            print(f"Total score: {total_score} points")
            break
        
        
        if not is_valid_word(word, hand, word_list):
            print("That is not a valid word. Please choose another word.")
            hand = update_hand(hand, word)
            continue
            
        hand = update_hand(hand, word)
        
        word_score = get_word_score(word, hand_length)
        total_score += word_score

        print(f"\"{word}\" earned {word_score}. Total: {total_score} points.")
    
    return total_score

    # Return the total score as result of function



#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    # Create a copy of the hand and generate the pool of letters
    copy_hand = hand.copy()
    all_letters = VOWELS + CONSONANTS
    
    # Check if the given letter is in the hand and we have at least one iteration of it
    if letter in copy_hand and copy_hand[letter] > 0:
        # Update the letter pool and remove the letters that are already in the hand 
        for key in copy_hand.keys():
            if copy_hand[key] > 0:
                all_letters = all_letters.replace(key, "")
        
        # Generate a random letter from the updated letter pool
        random_letter = random.choice(all_letters)

        # Get the count of the letter that needs to be replaced and update the new letter with the value 
        count = copy_hand.pop(letter)
        copy_hand[random_letter] = count
    else:
        print("Warning: No letter to substitute")
    return copy_hand

       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    print("Welcome to the 60001 Word Game")
    print("------------------")

    total_score = 0

    try:
        num_of_hands = int(input("Please enter the number of hands you would like to play: "))
    except:
        print("\nERROR: Please enter a numeric value")
        sys.exit(1)

    flag_replay = False 
    flag_substitute = False
    count = 0

    while count < num_of_hands:
        hand = deal_hand(HAND_SIZE)
        hand_replay = hand.copy()
        display_hand(hand)

        if flag_substitute == False:
            substitute = input("Would you like to substitute a letter? (yes/no) ")

            while str.lower(substitute) != 'yes' and str.lower(substitute) != 'no':
                print("This is not a valid answer, please try again.")
                substitute = input("Would you like to substitute a letter? (yes/no) ")

            if str.lower(substitute) == 'yes':
                flag_substitute = True
                letter = input("Please enter the letter you would like to substitute: ")
                hand = substitute_hand(hand, letter)

        hand_score = play_hand(hand, word_list)


        count += 1

        if flag_replay == False:
            replay = input("Would you like to replay a hand? (yes/no) ")

            while str.lower(replay) != 'yes' and str.lower(replay) != 'no':
                print("This is not a valid answer, please try again.")
                replay = input("Would you like to replay a hand? (yes/no) ")
            
            if str.lower(replay) == 'yes':
                hand_replay = hand.copy()
                old_hand_score = hand_score 
                hand_score = play_hand(hand_replay, word_list)
                hand_score = max(hand_score, old_hand_score)
                print("------------------")
                print(f"Total score after replay is: {hand_score}")
                flag_replay = True

        total_score += hand_score

    print(f"Game over! Your total score is {total_score}")
#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
