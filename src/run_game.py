from game import Game
from logging import Logging

game = Game(10, 4)
print('---------------------------------------------')
logs = Logging(game.board)
game.initialize_game()
game.play()
