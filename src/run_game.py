from game import Game
from logging import Logger

game = Game(5, 4)
print('---------------------------------------------')
logs = Logger(game.board)
game.initialize_game()
game.play()
 