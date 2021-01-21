import sys
sys.path.append('src')
from game import Game
from logger import Logger
from strategies.eli_dumb_strategy import DumbStrategy


player_strategies = DumbStrategy

game = Game([player_strategies, player_strategies], 5, 'asc', 3, max_turns=2)
print('---------------------------------------------')
game.initialize_game()
game.play()
log = Logger()
log.get_current_active_file('logs')  # get current file
log.get_correct_example_file(
    'test_logs/asc_combat_player_log.txt')  # ingest correct test

print('')
if log.compare_test_and_example():  # should give assert error if they aren't the same and give the line the test and the correct example are different
    print('Dumb Player Works!!!')
else:
    print('Dumb Player doenst work...')