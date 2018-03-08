import argparse
import random
import atexit

class Hangman(object):

  def __init__(self, _dict):
    self.dict = self.sample_words(_dict)
    self.next = -1

  def sample_words(self, _dict):
    with open(_dict, 'r') as f:
      lines = [l.rstrip() for l in f.readlines()]
      return [lines[i] for i in random.sample(range(len(lines)), 20)]


  def run(self):
    
    word = self.next_word()
    so_far = ['_' for i in range(len(word))]
    misses = []

    while (not self.game_over(misses, so_far)):
      self.print_stats(misses, so_far)
      guess = self.get_guess() 
      
      if (not guess in word):
        misses.append(guess)
      else:
        for i in range(len(word)):
          if (word[i] is guess):
            so_far[i] = guess
    
    if (len(misses) == 6):
      print('Game Over! The word was \"' + word + '\".')
    else:
      print('You won!')

  def game_over(self, misses, guessed):
    return len(misses) == 6 or not '_' in guessed

  def next_word(self):
    self.next += 1
    return self.dict[self.next]

  def print_stats(self, misses, guessed):
    print('------------------------------')
    print('Word: ' + ' '.join(guessed)) 
    print('Misses: ' + str(misses))

  def get_guess(self):
    guess = input('Guess: ')
    while (not guess.isalpha()):
      print('You can only play with letters, you dumbass!')
      guess = input('Guess: ')

    return guess



if __name__ == '__main__':

    @atexit.register
    def goodbye():
      print('...Oh, nvm! Goodbye!')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--dict', 
        default='/usr/share/dict/words',
        type=str,
        help='the dictionary source file to extract words.')
    args = parser.parse_args()
    
    game = Hangman(args.dict)
    while (True):
      try:
        game.run()
        if (input('Play again? [y/n] ') in ['n', 'no', 'N', 'NO']):
          break
      except EOFError:
        exit()




    
