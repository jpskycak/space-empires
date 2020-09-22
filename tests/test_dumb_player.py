import sys
sys.path.append('src')
from logger import Logger
from game import Game

game = Game(4, 'asc', max_turns = 4)
print('---------------------------------------------')
logs = Logger(game.board)
game.initialize_game()
game.play()

log_1 = Logger()

log_1.get_current_active_file('logs')  # get current file

log_1.get_correct_example_file('test_logs/dumb_player_correct_log.txt')  # ingest correct test
print('')
if log_1.compare_test_and_example():  # should give assert error if they aren't the same and give the line the test and the correct example are different
    print('Dumb Player Works!!!')
else:
    print('Dumb Player doenst work...')
