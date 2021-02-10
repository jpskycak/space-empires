import sys
sys.path.append('src')
#from strategies.classmate_strats.combat_strategy import CombatStrategy
#from strategies.classmate_strats.eli_combat_strategy import CombatStrategy
#from strategies.classmate_strats.riley_combat_strategy import CombatStrategy
from strategies.classmate_strats.george_combat_strategy import CombatStrategy
#from strategies.classmate_strats.david_combat_strategy import CombatStrategy
from game import Game
from logger import Logger

player_strategies = CombatStrategy

game_1 = Game([player_strategies, player_strategies], (5,5), 'asc', 3, max_turns=2)
print('---------------------------------------------')
game_1.initialize_game()
game_1.play()
log_1 = Logger()
log_1.get_current_active_file('logs')  # get current file
log_1.get_correct_example_file(
    'test_logs/asc_combat_player_log.txt')  # ingest correct test

game_2 = Game([player_strategies, player_strategies], (5,5), 'dsc', 3, max_turns=2)
print('---------------------------------------------')
game_2.initialize_game()
game_2.play()
log_2 = Logger()
log_2.get_current_active_file('logs')  # get current file
log_2.get_correct_example_file(
    'test_logs/dsc_combat_player_log.txt')  # ingest correct test

print('')

if log_1.compare_test_and_example():  # should give assert error if they aren't the same and give the line the test and the correct example are different
    print('Ascending Die Combat Player Works!!!')
else:
    print('Ascending Die Combat Player doenst work...')

if log_2.compare_test_and_example():  # should give assert error if they aren't the same and give the line the test and the correct example are different
    print('Descending Die Combat Player Works!!!')
else:
    print('Descending Die Combat Player doenst work...')

print('')