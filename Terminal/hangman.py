# Problem Set 2, hangman.py
# Name: Wutduk?
# Collaborators: Caffeine and methylphenidate ER.
# Time spent: Somewhere between less than 15.
"""
An interactive game of Hangman for the command terminal.

How to play:

    At the start of the game, a word (secret_word) is chosen for the player to
    guess, one letter at a time. Each guessed letter is recorded and the
    remaining letters are displayed at the start of each guessing round.

    Each game starts with six guesses.

    During each guessing round, the guess is evaluated (invalid, incorrect, or
    correct) and each correcly guessed letter is revealed. If a guess is
    invalid (not an alpha character or more than one character*) or if it has
    already been guessed (within each game), the player is penalized by losing
    a warning. Once there are no warnings left, a guess will be lost instead.
    See warning_penalty() for details.

    *There is one exception to this rule. See Hints below.

    For each valid (i.e. single alpha character), but incorrect letter guessed
    (i.e. not in the word), the player will lose:
        *   one guess for all consonants
        *   two guesses for vowels ("y" is not a vowel for the purposes of this
            game).
    See guess_penalty() for details.

    The game is over once all guesses have been lost or all letters in the word
    have been guessed. If the game is won, a score will be returned (see
    total_score() for details).

    Hints:
    *   Entering an asterisk (*) as the guess returns a list of all possible
        matches in the wordlist based on the currently guesses word.
        See match_with_gaps(), show_possible_matches(), and get_guessed_word()
        for details.
    *   Entering an asterisk + a percent-sign (*%) as the guess will return a
        list of all letters that comprise the possible match words returned by
        entering *, but with the addition of the percentage of each letters
        representation in the overall count of letters.

    It's important to note that the words returned by * and the stats returned
    by *% will be comprised of ALL words in the wordlist that are possible
    matches based on the value of guessed_word. This does NOT take into
    remove any correct or incorrect letters already guessed, so take the hints
    with caution.

    ###TODO###
    Difficulty:

        There are four difficulty levels: Easy, Normal, Hard, and Expert.
            *   Easy:
                *   Five warnings
                *   Unlimited hints
                    *   No hint restrictions.
                *   Score multiplyer: 0.5 (cuts score in half).
            *   Normal:
                *   Three warnings
                *   Three hints
                    *   Hints will be restricted when the number of possible
                        matches is less than five.
                    *   Score multiplyer: 1.0 (full score value).
            *   Hard:
                *   One warning
                *   One hint
                    *   Hints will be restricted when the number of possible
                        matches is less than ten.
                    *   Score multiplyer: 1.5 (boosts score by half).
            *   Expert:
                *   No warnings
                *   No hints
                *   Score multiplyer: 2.0 (double score value).

    ? Keep playing until you die. Scores compound with each subsequent game. ?
"""

import os
import random
import string

PENALTY_STAGES = {
6: """    ____
    |  |
    |
    |
    |
  __|__
""",
5: """
    ____
    |  |
    |  0
    |
    |
  __|__
""",
4: """
    ____
    |  |
    |  0
    |  |
    |
  __|__
""",
3: """
    ____
    |  |
    |  0
    | /|
    |
  __|__
""",
2: """
    ____
    |  |
    |  0
    | /|\\
    |
  __|__
""",
1: """
    ____
    |  |
    |  0
    | /|\\
    | /
  __|__
""",
0: """
    ____
    |  |
    |  0
    | /|\\
    | / \\
  __|__
""",
-1: """
    ____
    |  |
    |  0
    | /|\\
    | / \\
  __|__
""",
"victory": """
    ____
    |  |
    |
    |      \\o/ "heee!"
    |       |
  __|__    / \\
"""
}


def load_words():
    """
    Return a list of valid words. Words are strings of lowercase letters.

    Note: Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("\nLoading word list from file...")
    file_path = os.path.dirname(os.path.realpath(__file__))
    wordlist_filename = "words.txt"
    wordlist_file_path = os.path.join(file_path, wordlist_filename)
    wordlist_file = open(wordlist_file_path, 'r')
    line = wordlist_file.readline()
    wordlist = line.split()
    wordlist_len = len(wordlist)
    print(f"{wordlist_len} words loaded.", end='')
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
    guessed = (ltr if ltr in letters_guessed else '_ ' for ltr in secret_word)
    return ''.join(guessed)


def get_available_letters(letters_guessed):
    """
    Return a string comprised of the letters not yet guessed.

    Parameters:
        * letters_guessed: List; Which letters have been guessed so far.
    """
    letters = string.ascii_lowercase
    available_letters = (ltr for ltr in letters if ltr not in letters_guessed)
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

    print(f"\n{message} {guessed_word}{separator}")
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
    print(f"\n{message}", f"You have {warnings_left} warning{s} left:",
          f"{guessed_word}{separator}")
    return warnings_left


def total_score(secret_word, guesses_left):
    """Final score when the game is won."""
    unique_letter_count = len(set((ltr for ltr in secret_word)))
    total_score = unique_letter_count * guesses_left
    return total_score


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

    for ltr in set(trimmed_my_word.replace('_', '')):
        mw_ltr_count = trimmed_my_word.count(ltr)
        ow_ltr_count = other_word.count(ltr)
        if mw_ltr_count != ow_ltr_count:
            return False

    match_word = ''
    for i, ltr in enumerate(trimmed_my_word):
        if ltr == other_word[i]:
            match_word += ltr
        else:
            match_word += '_ '
    return my_word == match_word


def show_possible_matches(my_word, print_out=True):
    """
    Print every word in wordlist that matches my_word.

    *   my_word:    String; Current guess of secret_word. See get_guessed_word
                    for details.

    *   print_out: Boolean; Return a value if False. Defaults to True.
    """
    matches = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            matches.append(word)
    if print_out:
        print("\nPossible word matches are:\n\n",
              ' '.join(matches),
              f"\n~~~~~~~~~~~~~~~",
              sep='')
    if not print_out:
        return matches


def get_letter_stats(matches):
    """
    Print a statistical breakdown of the presence of each letter in the
    current list of possible matches from wordlist to secret_word, sorted
    highest to lowest occurrence.

    Parameters:
    *   matches:    List; All possible matches in wordlist for guessed word.
                    See get_guessed_word(), match_with_gaps(), and
                    show_possible_matches() for details.
    """
    matches_string = "".join(matches)
    total_ltr_count = len(matches_string)
    unique_letters = set(matches_string)
    ltr_stats = []
    for ltr in unique_letters:
        ltr_count = matches_string.count(ltr)
        ltr_percent = ltr_count/total_ltr_count
        ltr_stats.append((ltr, ltr_percent))

    ltr_stats.sort(key=lambda ltr: ltr[1], reverse=True)

    final_stats = []
    for ltr_stat in ltr_stats:
        ltr = ltr_stat[0]
        pcnt = ltr_stat[1]*100
        final_stats.append(f"{ltr}: {pcnt:.2f}%")
    print("\nLetter stats for the possible matches:\n",
          "; ".join(final_stats),
          "~~~~~~~~~~~~~~~",
          sep="\n")


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
    separator = "\n~~~~~~~~~~~~~~~"
    secret_word_len = len(secret_word)

    print(f"{separator}",
          f"Welcome to the game Hangman!\n",
          f"I am thinking of a word that is {secret_word_len} letters long."
        + f"{separator}",
          f"You have 3 warnings left.{separator}",
          sep="\n")

    # While the game is not over:
    while guesses_left > 0 and victory is False:
        available_letters = get_available_letters(letters_guessed)
        es = 'es' if guesses_left != 1 else ''
        print(f"You have {guesses_left} guess{es} left.{separator}\n",
              f"Available letters: {available_letters}\n",
              PENALTY_STAGES[guesses_left],
              sep="")
        guess = input("Please guess a letter: ").lower()

        # Request a hint; a list of possible matches.
        if guess == '*':
            show_possible_matches(guessed_word)
            print(f"{guessed_word}",
                  f"{separator}")
            continue
        # Secret hint of letter stats.
        elif guess == '*%':
            matches = show_possible_matches(guessed_word, False)
            get_letter_stats(matches)
            print(f"{guessed_word}",
                  f"{separator}")
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
            print(f"\nGood guess: {guessed_word}{separator}")
            victory = is_word_guessed(secret_word, letters_guessed)

    # If victory is True, game is won, so get the score.
    if victory == True:
        score = total_score(secret_word, guesses_left)
        print("Congratulations, you won!",
              PENALTY_STAGES["victory"],
              f"Your total score for this game is: {score}",
              sep="\n")
    # Else guesses are gone and the game is lost.
    else:
        print("Sorry, you ran out of guesses.",
              PENALTY_STAGES[guesses_left],
              f"\nThe word was '{secret_word}'.")


if __name__ == "__main__":
    wordlist = load_words()
    secret_word = choose_word(wordlist)
    hangman(secret_word)
