import sys
sys.path.append('src')
from strategies.level_1.berserker_strategy_level_1 import BerserkerStrategyLevel1
from strategies.level_1.random_strategy_level_1 import RandomStrategyLevel1
from strategies.level_1.dumb_strategy_level_1 import DumbStrategyLevel1
from strategies.level_1.colby_strategy_level_1 import ColbyStrategyLevel1
from strategies.level_1.flanker_strategy_level_1 import FlankerStrategyLevel1
from game import Game
from logger import Logger
import random

random.seed(0)

print('\nBerserker vs ...')

#Berserker vs Berserker
strat_choices = [[BerserkerStrategyLevel1, BerserkerStrategyLevel1], [BerserkerStrategyLevel1, BerserkerStrategyLevel1]]

winner_for_first_half = []
for i in range(0,500):
    game = Game(strat_choices[0], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_first_half.append(game.play())

winner_for_second_half = []
for i in range(0,500):
    game = Game(strat_choices[1], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_second_half.append(game.play())

print('\nBerserker Won', ((winner_for_first_half.count(0) + winner_for_second_half.count(1))/100)/100, 'percent of the time against Berserker!')

#Berserker vs Random
strat_choices = [[BerserkerStrategyLevel1, RandomStrategyLevel1], [RandomStrategyLevel1, BerserkerStrategyLevel1]]

winner_for_first_half = []

for _ in range(0,500):
    game = Game(strat_choices[0], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_first_half.append(game.play())

winner_for_second_half = []
for _ in range(0,500):
    game = Game(strat_choices[1], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_second_half.append(game.play())

print('\nBerserker Won', (winner_for_first_half.count(0) + winner_for_second_half.count(1))/100, 'percent of the time against Random!')

#Berserker vs Dumb
strat_choices = [[BerserkerStrategyLevel1, DumbStrategyLevel1], [DumbStrategyLevel1, BerserkerStrategyLevel1]]

winner_for_first_half = []
for _ in range(0,500):
    game = Game(strat_choices[0], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_first_half.append(game.play())

winner_for_second_half = []
for _ in range(0,500):
    game = Game(strat_choices[1], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_second_half.append(game.play())

print('\nBerserker Won', (winner_for_first_half.count(0) + winner_for_second_half.count(1))/100, 'percent of the time against Dumb!')

#Berserker vs Flanker
strat_choices = [[BerserkerStrategyLevel1, FlankerStrategyLevel1], [FlankerStrategyLevel1, BerserkerStrategyLevel1]]

winner_for_first_half = []
for _ in range(0,500):
    game = Game(strat_choices[0], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_first_half.append(game.play())

winner_for_second_half = []
for _ in range(0,500):
    game = Game(strat_choices[1], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_second_half.append(game.play())

print('\nBerserker Won', (winner_for_first_half.count(0) + winner_for_second_half.count(1))/100, 'percent of the time against Flanker!')

#Berserker vs Colby
strat_choices = [[BerserkerStrategyLevel1, ColbyStrategyLevel1], [ColbyStrategyLevel1, BerserkerStrategyLevel1]]

winner_for_first_half = []
for _ in range(0,500):
    game = Game(strat_choices[0], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_first_half.append(game.play())

winner_for_second_half = []
for _ in range(0,500):
    game = Game(strat_choices[1], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_second_half.append(game.play())

print('\nBerserker Won', (winner_for_first_half.count(0) + winner_for_second_half.count(1))/100, 'percent of the time against Colby!')

print('\nColby vs ...')

#Colby vs Berserker
strat_choices = [[ColbyStrategyLevel1, BerserkerStrategyLevel1], [BerserkerStrategyLevel1, ColbyStrategyLevel1]]

winner_for_first_half = []
for _ in range(0,500):
    game = Game(strat_choices[0], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_first_half.append(game.play())

winner_for_second_half = []
for _ in range(0,500):
    game = Game(strat_choices[1], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_second_half.append(game.play())

print('\nColby Won', (winner_for_first_half.count(0) + winner_for_second_half.count(1))/100, 'percent of the time against Berserker!')

#Colby vs Random
strat_choices = [[ColbyStrategyLevel1, RandomStrategyLevel1], [RandomStrategyLevel1, ColbyStrategyLevel1]]

winner_for_first_half = []
for _ in range(0,500):
    game = Game(strat_choices[0], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_first_half.append(game.play())

winner_for_second_half = []
for _ in range(0,500):
    game = Game(strat_choices[1], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_second_half.append(game.play())

print('\nColby Won', (winner_for_first_half.count(0) + winner_for_second_half.count(1))/100, 'percent of the time against Random!')

#Colby vs Dumb
strat_choices = [[ColbyStrategyLevel1, DumbStrategyLevel1], [DumbStrategyLevel1, ColbyStrategyLevel1]]

winner_for_first_half = []
for _ in range(0,500):
    game = Game(strat_choices[0], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_first_half.append(game.play())

winner_for_second_half = []
for _ in range(0,500):
    game = Game(strat_choices[1], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_second_half.append(game.play())

print('\nColby Won', (winner_for_first_half.count(0) + winner_for_second_half.count(1))/100, 'percent of the time against Dumb!')

#Colby vs Flanker
strat_choices = [[ColbyStrategyLevel1, FlankerStrategyLevel1], [FlankerStrategyLevel1, ColbyStrategyLevel1]]

winner_for_first_half = []
for _ in range(0,500):
    game = Game(strat_choices[0], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_first_half.append(game.play())

winner_for_second_half = []
for _ in range(0,500):
    game = Game(strat_choices[1], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_second_half.append(game.play())

print('\nColby Won', (winner_for_first_half.count(0) + winner_for_second_half.count(1))/100, 'percent of the time against Flanker!')

#Colby vs Colby
strat_choices = [[ColbyStrategyLevel1, ColbyStrategyLevel1], [ColbyStrategyLevel1, ColbyStrategyLevel1]]

winner_for_first_half = []
for _ in range(0,500):
    game = Game(strat_choices[0], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_first_half.append(game.play())

winner_for_second_half = []
for _ in range(0,500):
    game = Game(strat_choices[1], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_second_half.append(game.play())

print('\nColby Won', (winner_for_first_half.count(0) + winner_for_second_half.count(1))/100, 'percent of the time against Colby!')

print('\nFlanker vs ...')

#Flanker vs Berserker
strat_choices = [[FlankerStrategyLevel1, BerserkerStrategyLevel1], [BerserkerStrategyLevel1, FlankerStrategyLevel1]]

winner_for_first_half = []
for _ in range(0,500):
    game = Game(strat_choices[0], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_first_half.append(game.play())

winner_for_second_half = []
for _ in range(0,500):
    game = Game(strat_choices[1], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_second_half.append(game.play())

print('\nFlanker Won', (winner_for_first_half.count(0) + winner_for_second_half.count(1))/100, 'percent of the time against Berserker!')

#Flanker vs Random
strat_choices = [[FlankerStrategyLevel1, RandomStrategyLevel1], [RandomStrategyLevel1, FlankerStrategyLevel1]]

winner_for_first_half = []
for _ in range(0,500):
    game = Game(strat_choices[0], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_first_half.append(game.play())

winner_for_second_half = []
for _ in range(0,500):
    game = Game(strat_choices[1], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_second_half.append(game.play())

print('\nFlanker Won', (winner_for_first_half.count(0) + winner_for_second_half.count(1))/100, 'percent of the time against Random!')

#Flanker vs Dumb
strat_choices = [[FlankerStrategyLevel1, DumbStrategyLevel1], [DumbStrategyLevel1, FlankerStrategyLevel1]]

winner_for_first_half = []
for _ in range(0,500):
    game = Game(strat_choices[0], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_first_half.append(game.play())

winner_for_second_half = []
for _ in range(0,500):
    game = Game(strat_choices[1], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_second_half.append(game.play())

print('\nFlanker Won', (winner_for_first_half.count(0) + winner_for_second_half.count(1))/100, 'percent of the time against Dumb!')

#Flanker vs Flanker
strat_choices = [[FlankerStrategyLevel1, FlankerStrategyLevel1], [FlankerStrategyLevel1, FlankerStrategyLevel1]]

winner_for_first_half = []
for _ in range(0,500):
    game = Game(strat_choices[0], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_first_half.append(game.play())

winner_for_second_half = []
for _ in range(0,500):
    game = Game(strat_choices[1], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_second_half.append(game.play())

print('\nFlanker Won', (winner_for_first_half.count(0) + winner_for_second_half.count(1))/100, 'percent of the time against Flanker!')

#Flanker vs Colby
strat_choices = [[FlankerStrategyLevel1, ColbyStrategyLevel1], [FlankerStrategyLevel1, BerserkerStrategyLevel1]]

winner_for_first_half = []
for _ in range(0,500):
    game = Game(strat_choices[0], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_first_half.append(game.play())

winner_for_second_half = []
for _ in range(0,500):
    game = Game(strat_choices[1], (5,5), 'random', 3, print_state_obsolete=False, can_log=False)
    game.initialize_game()
    winner_for_second_half.append(game.play())

print('\nFlanker Won', (winner_for_first_half.count(0) + winner_for_second_half.count(1))/100, 'percent of the time against Colby!')