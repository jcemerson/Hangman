# Problem Set 2, hangman.py
# Name: Wutduk?
# Collaborators: Caffeine and methylphenidate ER.
# Time spent: Somewhere between less than 15.
"""
An interactive game of Hangman for the command terminal.

How to play:

At the start of the game, a word (secret_word) is chosen for the player to
guess, one letter at a time. Each guessed letter is recorded and the remaining
letters are displayed at the start of each guessing round.

If playing the "hangman_with_hints" version, entering * as the guess will
return a list of all possible matches in the wordlist based on the currently
guesses word. See match_with_gaps(), show_possible_matches(), and
get_guessed_word() for details.

Each game starts with three warnings.

During each guessing round, the guess is evaluated (invalid, incorrect, or
correct) and each correcly guessed letter is revealed. If a guess is invalid
(not an alpha character or more than one character) or it if has already been
guessed (during each game), the player is penalized by losing a warning. Once
there are no warnings left, a guess will be lost instead. See warning_penalty()
for details.

Each game starts with six guesses.

For each valid, but incorrect guess (guessed letter is not in the word), the
player will lose:
    *   one guess for all consonants
    *   two guesses for vowels ("y" is not a vowel for the purposes of this
        game).
See guess_penalty() for details.

The game is over once all guesses have been lost or all letters in the word
have been guessed. If the game is won, a score will be returned (see
total_score() for details).
"""

import random
import string

def load_words():
    """
    Return a list of valid words. Words are strings of lowercase letters.

    Note: Depending on the size of the word list, this function may
    take a while to finish.
    """
    wordlist_filename = "words.txt"
    print("Loading word list from file...")
    wordlist_file = open(wordlist_filename, 'r')
    line = wordlist_file.readline()
    wordlist = line.split()
    wordlist_len = len(wordlist)
    print(f"{wordlist_len} words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    Return a word from wordlist at random.

    Parameters:
    * wordlist: List; A list of words (strings). All letters are converted
                to lowercase.
    """
    return random.choice(wordlist).lower()


def is_word_guessed(secret_word, letters_guessed):
    """
    Return True if all letters of secret_word in letters_guessed, else False.

    Parameters:
    * secret_word:     String; The word the user is guessing.  All letters
                       are lowercase.
    * letters_guessed: List; Which letters have been guessed so far.
                       All letters guessed are converted to lowercase.
    """
    unguessed_letters = set(secret_word) - set(letters_guessed)
    if len(unguessed_letters) > 0:
        return False
    else:
        return True


def get_guessed_word(secret_word, letters_guessed):
    """
    Return a string comprised of letters or underscores and spaces ('_ ') that
    represents which letters in secret_word have been guessed, or not, so far.

    Parameters:
    * secret_word:     String; The word the user is guessing.
    * letters_guessed: List; Which letters have been guessed so far.
    """
    # Return each letter from secret_word if letter is in letters_guessed,
    # else return '_ ' when letter is not.
    guessed = (l if l in letters_guessed else '_ ' for l in secret_word)
    return ''.join(guessed)


def get_available_letters(letters_guessed):
    """
    Return a string comprised of the letters not yet guessed.

    Parameters:
        * letters_guessed: List; Which letters have been guessed so far.
    """
    letters = string.ascii_lowercase
    available_letters = (l for l in letters if l not in letters_guessed)
    return ''.join(available_letters)


def guess_penalty(guesses_left, guessed_word, separator, type, guess=None):
    """
    Apply a penalty for guesses not in secret_word.

    Parameters:
    * guesses_left: Int; Remaining guesses before game is over.
    * guessed_word: String; Letters of secret_word that have been guessed and
                    not yet guessed. See get_guessed_word() for details.
    * separator:    String; Used to break-up guessing rounds.
    * type:         String; Describes the kind of guess penalty. One of three:
                        * invalid:   Either guess is not an alpha character, or
                                     more than one character.
                                     See "guess is None" below for details.
                        * re-guess:  A guess already played (stored in
                                     letters_guessed). See "guess is None"
                                     below for details.
                        * incorrect: A valid and unique guess that is not in
                                     secret_word.
    * guess:        String; The letter guessed (defaults to None).
                        * If guess is a vowel, subtract 2 points.
                        * If guess is a consonant, subtract 1 point.
                        * If guess is None (no value passed in call), the
                          guess penalty resulted from a warning, but the there
                          are no more warnings to subtract, so a guess is lost.
    """
    vowels = ('a', 'e', 'i', 'o', 'u')
    if guess in vowels:
        guesses_left -= 2
    else:
        guesses_left -= 1

    if type == 'invalid':
        message = "Oops! That is not a valid letter."
    elif type == 're-guess':
        message = "Oops! You've already guessed that letter."
    elif type == 'incorrect':
        message = "Oops! That letter is not in my word:"

    if guess is None:
        message = message + " You have no warnings left so you lose one guess:"

    print(f"{message} {guessed_word}{separator}")
    return guesses_left


def warning_penalty(warnings_left, guessed_word, separator, type):
    """
    Apply a penalty for invalid guesses and repeat guesses.

    Parameters:
    * warnings_left: Int; Remaining warnings. Once at 0, guesses are lost
                     instead.
    * guessed_word:  String; Letters of secret_word that have been guessed and
                     not yet guessed. See get_guessed_word() for details.
    * separator:     String; Used to break-up guessing rounds.
    * type:          String; Describes the kind of warning penalty.
                     One of two:
                        * invalid:   Either guess is not an alpha character, or
                                     more than one character.
                        * re-guess:  A guess already played (stored in
                                     letters_guessed).
    """
    warnings_left -= 1
    if type == 'invalid':
        message = "Oops! That is not a valid letter."
    elif type == 're-guess':
        message = "Oops! You've already guessed that letter."
    s = 's' if warnings_left != 1 else ''
    print(message, f"You have {warnings_left} warning{s} left:",
          f"{guessed_word}{separator}")
    return warnings_left


def total_score(secret_word, guesses_left):
    """Final score when the game is won."""
    unique_letter_count = len(set((l for l in secret_word)))
    total_score = unique_letter_count * guesses_left
    return total_score


def hangman(secret_word):
    """
    Start an interactive game of Hangman.

    Parameters:
    * secret_word:  String; The word to guess. Chosen at random from wordlist.
                    See load_words() and choose_word() for details.
    """
    warnings_left = 3
    guesses_left = 6
    victory = False
    letters_guessed = []
    guessed_word = get_guessed_word(secret_word, letters_guessed)
    separator = "\n------------"
    secret_word_len = len(secret_word)

    print("Welcome to the game Hangman!",
        f"I am thinking of a word that is {secret_word_len} letters long.",
        f"You have 3 warnings left.{separator}",
        sep="\n")

    # While the game is not over:
    while guesses_left > 0 and victory is False:
        available_letters = get_available_letters(letters_guessed)
        es = 'es' if guesses_left != 1 else ''
        print(f"You have {guesses_left} guess{es} left.",
              f"Available letters: {available_letters}",
              sep="\n")
        guess = input("Please guess a letter: ").lower()

        # Invalid guess (not alpha character).
        if not guess.isalpha() or len(guess) > 1:
            type = 'invalid'
            # If warnings remain, lose a warning.
            if warnings_left > 0:
                warnings_left = warning_penalty(
                    warnings_left,
                    guessed_word,
                    separator,
                    type)
            # If no warnings remain, lose a guess.
            else:
                guesses_left = guess_penalty(
                    guesses_left,
                    guessed_word,
                    separator,
                    type)
            continue

        #Re-guess (already guessed letter).
        if guess in letters_guessed:
            type = 're-guess'
            # If warnings remain, lose a warning.
            if warnings_left > 0:
                warnings_left = warning_penalty(
                    warnings_left,
                    guessed_word,
                    separator,
                    type)

            # If no warnings remain, lose a guess.
            else:
                guesses_left = guess_penalty(
                    guesses_left,
                    guessed_word,
                    separator,
                    type)
            continue

        # If incorrect guess (not in secret_word), lose a guess.
        if guess not in secret_word:
            letters_guessed.append(guess)
            guesses_left = guess_penalty(
                guesses_left,
                guessed_word,
                separator,
                'incorrect',
                guess)
        # Correct guess.
        else:
            letters_guessed.append(guess)
            guessed_word = get_guessed_word(secret_word, letters_guessed)
            print(f"Good guess: {guessed_word}{separator}")
            victory = is_word_guessed(secret_word, letters_guessed)

    # If victory is True, game is won, so get the score.
    if victory == True:
        score = total_score(secret_word, guesses_left)
        print("Congratulations, you won! \\o/",
              f"Your total score for this game is: {score}",
              sep="\n")
    # Else guesses are gone and the game is lost.
    else:
        print("Sorry, you ran out of guesses.",
            f"The word was '{secret_word}'.")


# -----------------------------------


def match_with_gaps(my_word, other_word):
    """
    Return True if all the actual letters of my_word match the
    corresponding letters of other_word, or the letter is the special
    symbol '_ ', and my_word and other_word are of the same length, otherwise
    return False.

    Parameters:
    *   my_word:    String; Current guess of secret_word. See get_guessed_word
                    for details.

    *   other_word: String; Word from wordlist.
    """
    trimmed_my_word = my_word.replace(' ','')
    if len(trimmed_my_word) != len(other_word):
        return False

    for l in set(trimmed_my_word.replace('_', '')):
        mw_l_count = trimmed_my_word.count(l)
        ow_l_count = other_word.count(l)
        if mw_l_count != ow_l_count:
            return False

    match_word = ''
    for i, l in enumerate(trimmed_my_word):
        if l == other_word[i]:
            match_word += l
        else:
            match_word += '_ '

    return True if my_word == match_word else False


def show_possible_matches(my_word):
    """
    Print every word in wordlist that matches my_word.
    """
    separator = "\n------------"
    matches = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            matches.append(word)
    print("Possible word matches are:\n",
          ' '.join(matches),
          separator,
          sep='')

def hangman_with_hints(secret_word):
    """
    Start an interactive game of Hangman.

    Parameters:
    * secret_word:  String; The word to guess. Chosen at random from wordlist.
                    See load_words() and choose_word() for details.
    """
    warnings_left = 3
    guesses_left = 6
    victory = False
    letters_guessed = []
    guessed_word = get_guessed_word(secret_word, letters_guessed)
    separator = "\n------------"
    secret_word_len = len(secret_word)

    print("Welcome to the game Hangman!",
        f"I am thinking of a word that is {secret_word_len} letters long.",
        f"You have 3 warnings left.{separator}",
        sep="\n")

    # While the game is not over:
    while guesses_left > 0 and victory is False:
        available_letters = get_available_letters(letters_guessed)
        es = 'es' if guesses_left != 1 else ''
        print(f"You have {guesses_left} guess{es} left.",
              f"Available letters: {available_letters}",
              sep="\n")
        guess = input("Please guess a letter: ").lower()

        # Request a hint; a list of possible matches.
        if guess == '*':
            show_possible_matches(guessed_word)
            continue

        # Invalid guess (not alpha character).
        if not guess.isalpha() or len(guess) > 1:
            type = 'invalid'
            # If warnings remain, lose a warning.
            if warnings_left > 0:
                warnings_left = warning_penalty(
                    warnings_left,
                    guessed_word,
                    separator,
                    type)
            # If no warnings remain, lose a guess.
            else:
                guesses_left = guess_penalty(
                    guesses_left,
                    guessed_word,
                    separator,
                    type)
            continue

        #Re-guess (already guessed letter).
        if guess in letters_guessed:
            type = 're-guess'
            # If warnings remain, lose a warning.
            if warnings_left > 0:
                warnings_left = warning_penalty(
                    warnings_left,
                    guessed_word,
                    separator,
                    type)

            # If no warnings remain, lose a guess.
            else:
                guesses_left = guess_penalty(
                    guesses_left,
                    guessed_word,
                    separator,
                    type)
            continue

        # If incorrect guess (not in secret_word), lose a guess.
        if guess not in secret_word:
            letters_guessed.append(guess)
            guesses_left = guess_penalty(
                guesses_left,
                guessed_word,
                separator,
                'incorrect',
                guess)
        # Correct guess.
        else:
            letters_guessed.append(guess)
            guessed_word = get_guessed_word(secret_word, letters_guessed)
            print(f"Good guess: {guessed_word}{separator}")
            victory = is_word_guessed(secret_word, letters_guessed)

    # If victory is True, game is won, so get the score.
    if victory is True:
        score = total_score(secret_word, guesses_left)
        print("Congratulations, you won! \\o/",
              f"Your total score for this game is: {score}",
              sep="\n")
    # Else guesses are gone and the game is lost.
    else:
        print("Sorry, you ran out of guesses.",
            f"The word was '{secret_word}'.")


if __name__ == "__main__":
    wordlist = load_words()
    secret_word = choose_word(wordlist)
    # hangman(secret_word)
    hangman_with_hints(secret_word)
