import sys
sys.path.append('src')

from logging import Logging

log = Logging()

log.get_current_active_file('space-empires/src/logs')

contents = log.read_info()

log.get_current_active_file('space-empires/src/test_logs', 'test_dumb_player')

test = log.read_info()

assert contents == test, 'The dumb player is as dumb as you think'

print('Dumb Player Works!!!')
