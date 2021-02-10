import sys
sys.path.append('src')
#from strategies.classmate_strats.dumb_strategy import DumbStrategy
#from strategies.classmate_strats.eli_dumb_strategy import DumbStrategy
#from strategies.classmate_strats.riley_dumb_strategy import DumbStrategy
from strategies.classmate_strats.george_dumb_strategy import DumbStrategy
#from strategies.classmate_strats.david_dumb_strategy import DumbStrategy
from logger import Logger
from game import Game


player_strategies = DumbStrategy

game = Game([player_strategies, player_strategies], (5,5), 'asc', 3, max_turns=2)
print('---------------------------------------------')
game.initialize_game()
game.play()
log = Logger()
log.get_current_active_file('logs')  # get current file
log.get_correct_example_file(
    'test_logs/dumb_player_correct_log.txt')  # ingest correct test

print('')
if log.compare_test_and_example():  # should give assert error if they aren't the same and give the line the test and the correct example are different
    print('Dumb Player Works!!!')
else:
    print('Dumb Player doenst work...')
