from game import Game
from logging import Logger

game = Game(4, 'asc', max_turns = 2)
print('---------------------------------------------')
logs = Logger(game.board)
game.initialize_game()
game.play() 