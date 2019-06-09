from .exceptions import *
from random import choice


class GuessAttempt(object):
    def __init__(self, letter, hit=False, miss=False):
        self.letter = letter
        if hit == miss:
            raise InvalidGuessAttempt
        else:
            self.hit = hit

    def is_hit(self):
        return self.hit

    def is_miss(self):
        return not self.hit


class GuessWord(object):
    def __init__(self, answer):
        if len(answer) == 0:
            raise InvalidWordException
        self.answer = answer
        self.masked = '*' * len(answer)

    def perform_attempt(self, letter):
        if len(letter) != 1:
            raise InvalidGuessedLetterException
        if letter.lower() in self.answer.lower() and letter.lower() not in self.masked:
            _mask = ''
            for index, character in enumerate(self.answer.lower()):
                if character != letter.lower():
                    _mask += self.masked[index]
                else:
                    _mask += character
            self.masked = _mask
            return GuessAttempt(letter, hit=True)
        return GuessAttempt(letter, miss=True)


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']

    @classmethod
    def select_random_word(cls, wordlist):
        if len(wordlist) == 0:
            raise InvalidListOfWordsException
        return choice(wordlist)

    def __init__(self, word_list=WORD_LIST, number_of_guesses=5):
        if word_list:
            self.wordlist = word_list
        else:
            self.wordlist = HangmanGame.WORD_LIST
        self.word = GuessWord(HangmanGame.select_random_word(self.wordlist))
        self.previous_guesses = []
        self.remaining_misses = number_of_guesses

    def guess(self, letter):
        if self.is_finished():
            raise GameFinishedException
        self.previous_guesses.append(letter.lower())
        attempt = self.word.perform_attempt(letter.lower())
        if attempt.is_miss():
            self.remaining_misses -= 1
            if self.is_lost():
                raise GameLostException
        if self.is_won():
            raise GameWonException
        return attempt

    def is_finished(self):
        if '*' in self.word.masked and self.remaining_misses > 0:
            return False
        return True

    def is_won(self):
        if self.is_finished() and self.remaining_misses > 0:
            return True
        return False

    def is_lost(self):
        if self.is_finished() and self.remaining_misses == 0:
            return True
        return False
