import argparse
import random
import atexit
import sys

assert sys.version_info >= (3, 0), "Please run with python 3"

class Hangman(object):

    def __init__(self, _dict):
        self.dict = self.sample_words(_dict)
        self.next = -1

    def sample_words(self, _dict):
        with open(_dict, 'r') as f:
            lines = [l.rstrip() for l in f.readlines()]
            return [lines[i] for i in random.sample(range(len(lines)), 20)]

    def play(self, guess):
        if guess not in self.word:
            self.misses.append(guess)
        else:
            self.guessed.append(guess)

    def game_over(self):
        return len(self.misses) == 6 or \
            all(l in self.guessed for l in self.word)

    def next_word(self):
        self.next += 1
        self.misses = []
        self.guessed = []
        self.word = self.dict[self.next]


# I/O utilities -------------------------------------------

def end_game_msg(misses, word):
    if len(misses) == 6:
        print('Game Over! The word was \"' + word + '\".')
    else:
        print('You won!\n\"' + word + '\"')


def print_status(misses, guessed, word):
    print('------------------------------')
    print('Word: ' + ' '.join(c if c in guessed else '_' for c in word))
    print('Misses: ' + str(misses))


def get_guess(tried):
    while True:
        guess = input('Guess: ')
        if not guess.isalpha():
            print('You can only play with letters, you dumbass!')
        elif len(guess) != 1:
            print('In my experience, a letter is one character...')
        elif guess in tried:
            print('You\'re asleep bruv?! You\'ve already tried that one!')
        else:
            return guess


@atexit.register
def goodbye():
    print('...Oh, nvm! Goodbye!')

# Main ----------------------------------------------------


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dict',
                        default='/usr/share/dict/words',
                        type=str,
                        help='the dictionary source file to extract words.')
    args = parser.parse_args()

    game = Hangman(args.dict)
    while True:
        try:
            game.next_word()
            while not game.game_over():
                print_status(game.misses, game.guessed, game.word)
                guess = get_guess(game.misses + game.guessed)
                game.play(guess)
            end_game_msg(game.misses, game.word)

            if input('Play again? [y/n] ') in ['n', 'no', 'N', 'NO']:
                break
        except EOFError:
            exit()
