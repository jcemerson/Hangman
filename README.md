# Hangman

An interactive game of Hangman for the command terminal.

***How to play:***

At the start of the game, a word (secret_word) is chosen for the player to
guess, one letter at a time. Each guessed letter is recorded and the remaining
letters are displayed at the start of each guessing round.

If playing the "hangman_with_hints" version, entering * as the guess will
return a list of all possible matches in the wordlist based on the currently
guesses word. *See match_with_gaps(), show_possible_matches(), and
get_guessed_word() for details.*

**Each game starts with three warnings.**

During each guessing round, the guess is evaluated (invalid, incorrect, or
correct) and each correcly guessed letter is revealed. If a guess is invalid
(not an alpha character or more than one character) or it if has already been
guessed (during each game), the player is penalized by losing a warning. Once
there are no warnings left, a guess will be lost instead. *See warning_penalty()
for details.*

**Each game starts with six guesses.**

For each valid, but incorrect guess (guessed letter is not in the word), the
player will lose:
    *   one guess for all consonants
    *   two guesses for vowels ("y" is not a vowel for the purposes of this
        game).
*See guess_penalty() for details.*

The game is over once all guesses have been lost or all letters in the word
have been guessed. If the game is won, a score will be returned *(see
total_score() for details)*.
