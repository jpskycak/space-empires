import sys
sys.path.append('src')
from logger import Logger
from game import Game

game = Game(4, 'asc', 1, max_turns = 4)
print('---------------------------------------------')
logs = Logger()
game.initialize_game()
game.play()

log = Logger()

log.get_current_active_file('logs')  # get current file
                            
log.get_correct_example_file('test_logs/dumb_player_correct_log.txt')  # ingest correct test
print('')
if log.compare_test_and_example():  # should give assert error if they aren't the same and give the line the test and the correct example are different
    print('Dumb Player Works!!!')
else:
    print('Dumb Player doenst work...')
