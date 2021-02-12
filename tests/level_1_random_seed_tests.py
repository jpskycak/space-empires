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
import math

strat_choices = [FlankerStrategyLevel1, BerserkerStrategyLevel1]

def run_simuations(strats, number_of_simulations):
    first_half = run_half_simulations(strats, number_of_simulations // 2, 0)
    second_half = run_half_simulations(strats[::-1], number_of_simulations // 2, number_of_simulations // 2)
    draws = [game for game in (first_half + second_half) if game == None]# + [game for game in second_half if game is None]
    return first_half,second_half,(first_half.count(0) + second_half.count(1)) / ((number_of_simulations - len(draws)) * .01), draws

def run_half_simulations(strats, number_of_simulations, seed_offset):
    winner = []
    for i in range(seed_offset, number_of_simulations+seed_offset):
        random.seed(i+1)
        game = Game(strats, (5,5), 'random', print_state_obsolete=False, can_log=True, number_of_economic_phases=0, build_player_ship_yards=False, max_turns=5, number_of_movement_rounds=1)
        game.initialize_game()
        winner.append(game.play())
    return winner

games,games2, winrate, draws = run_simuations(strat_choices, 20)

print('\ngames,games2', games+games2)
print('game indices', [index for index, outcome in enumerate(games) if outcome == 0] + [index+10 for index, outcome in enumerate(games2) if outcome == 1])
print('\nFlanker Won', winrate, 'percent of the time against Berserker!')
print('Flanker drew against Berserker', len(draws), 'times!')
