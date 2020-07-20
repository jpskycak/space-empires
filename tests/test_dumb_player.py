import sys
sys.path.append('src')
from logging import Logging


log = Logging()

log.get_current_active_file('space-empires/logs') #get current file

log.get_correct_example(open('space-empires/test_logs/dumb_player_correct_log.txt', 'r')) #ingest correct test

log.compare_test_and_example() #should give assert error if they aren't the same and give the line the test and the correct example are different

print('Dumb Player Works!!!')
