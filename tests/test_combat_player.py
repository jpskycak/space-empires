import sys
sys.path.append('src')
from logger import Logger


log = Logger()

log.get_current_active_file('logs') #get current file

log.get_correct_example_file('test_logs/combat_player_correct_log.txt') #ingest correct test
print('')
if log.compare_test_and_example():  # should give assert error if they aren't the same and give the line the test and the correct example are different
    print('Combat Player Works!!!')
else:
    print('Combat Player doenst work...')

