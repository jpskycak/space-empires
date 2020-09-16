import sys
sys.path.append('src')
from logger import Logger
from game import Game

game_1 = Game(5, 'asc', max_turns = 2)
print('---------------------------------------------')
logs = Logger(game_1.board)
game_1.initialize_game()
game_1.play()

log_1 = Logger()

log_1.get_current_active_file('logs')  # get current file

log_1.get_correct_example_file(
    'test_logs/asc_combat_player_log.txt')  # ingest correct test
print('')
if log_1.compare_test_and_example():  # should give assert error if they aren't the same and give the line the test and the correct example are different
    print('Ascending Die Combat Player Works!!!')
else:
    print('Ascending Die Combat Player doenst work...')

game_2 = Game(5, 'dsc', max_turns=2)
print('---------------------------------------------')
logs = Logger(game_2.board)
game_2.initialize_game()
game_2.play()

log_2 = Logger()

log_2.get_current_active_file('logs')  # get current file

log_2.get_correct_example_file(
    'test_logs/dsc_combat_player_log.txt')  # ingest correct test
print('')
if log_2.compare_test_and_example():  # should give assert error if they aren't the same and give the line the test and the correct example are different
    print('Descending Die Combat Player Works!!!')
else:
    print('Descending Die Combat Player doenst work...')

