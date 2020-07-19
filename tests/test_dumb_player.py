from logging import Logging
import sys
sys.path.append('src')


log = Logging()
example = Logging

log.get_current_active_file('space-empires/logs')

contents = log.read_info()

correct_example.get_current_active_file(
    'space-empires/test_logs', 'test_dumb_player')

test = correct_example.read_info()

# print lines that are different from the correct example
with log.active_file as text, correct_example.active_file as exc:
    exclusions = [line.rstrip('\n') for line in exc]
    for line in text:
        if not any(exclusion in line for exclusion in exclusions):
            print line

assert contents == test, "The dumb player isn't as dumb as you think"


print('Dumb Player Works!!!')
