WORD GAME

==================

This is a simple word building game, played in the terminal. The player chooses the number of hands they want to play, and receive a number of letters based on the HAND_SIZE, including a wildcard (*) element, which can be used to replace any vowel.

The round starts off with the newly generated hand, and gives the player an option to substitute one of the letters from their hand. This option is available once per game, and once used, other hands will need to be played without this option.

The player then builds the words from the provided letters. 

If they input a word that's not found in the word list, or if the word contains invalid letters (more letters than provided, different letters), their answer will amount to 0 points and the letters used will be removed from the hand (if present).

If the player inserts a valid word, it's score will be calculated and displayed at the end of each hand.

The player can either end a round when his hand is empty, or when pressing '!!'. In either case, they will be shown the score of that specific hand at the end.

The player also has the option of replaying a hand. If they choose to do that, the substitute option will not work, and they will be dealt the initial hand. This option is avaialble once per game as well.

The replay option will pick the highest of the two scores for that hand.

At the end of the game, when the specified number of hands has been played, the player will receive their final score, comprised of the sum of the points for all the hands played.