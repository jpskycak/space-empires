import sys
sys.path.append('src')
from strategies.level_2.attack_berserker_strategy_level_2 import AttackBerserkerStrategyLevel2
from strategies.level_2.defense_berserker_strategy_level_2 import DefenseBerserkerStrategyLevel2
from strategies.level_2.movement_berserker_strategy_level_2 import MovementBerserkerStrategyLevel2
from strategies.level_2.numbers_berserker_strategy_level_2 import NumbersBerserkerStrategyLevel2
from strategies.level_2.flanker_strategy_level_2 import FlankerStrategyLevel2
from strategies.level_2.colby_strategy_level_2 import ColbyStrategyLevel2
from game import Game
from logger import Logger
import random
import math

strat_choices_1 = [NumbersBerserkerStrategyLevel2, AttackBerserkerStrategyLevel2]
strat_choices_2 = [MovementBerserkerStrategyLevel2, DefenseBerserkerStrategyLevel2]

def run_simuations(strats, number_of_simulations, tue):
    first_half = run_half_simulations(strats, number_of_simulations // 2, 0, tue)
    second_half = run_half_simulations(strats[::-1], number_of_simulations // 2, number_of_simulations // 2, tue)
    draws = [game for game in (first_half + second_half) if game == None]# + [game for game in second_half if game is None]
    return first_half,second_half,(first_half.count(0) + second_half.count(1)) / ((number_of_simulations - len(draws)) * .01), draws

def run_half_simulations(strats, number_of_simulations, seed_offset, tue):
    winner = []
    for i in range(seed_offset, number_of_simulations+seed_offset):
        random.seed(i+1)
        if tue and i == 69: #debugging
            print('oi soi boi')
            game = Game(strats, (5,5), 'random', print_state_obsolete=True, can_log=True, number_of_economic_phases=1, build_player_ship_yards=True, max_turns=5, number_of_movement_rounds=1)
        else:
            game = Game(strats, (5,5), 'random', print_state_obsolete=False, can_log=True, number_of_economic_phases=1, build_player_ship_yards=True, max_turns=5, number_of_movement_rounds=1)
        game.initialize_game()
        winner.append(game.play())
    return winner

games,games2, winrate, draws = run_simuations(strat_choices_1, 20, False)

print('\ngames,games2', games+games2)
print('game indices', [index for index, outcome in enumerate(games) if outcome == 0] + [index+10 for index, outcome in enumerate(games2) if outcome == 1])
print('\nNumbers Berserker Won', winrate, 'percent of the time against Attack Berserker!')
print('Numbers Berserker drew against Attack Berserker', len(draws), 'times!')

games,games2, winrate, draws = run_simuations(strat_choices_2, 20, True)

print('\ngames,games2', games+games2)
print('game indices', [index for index, outcome in enumerate(games) if outcome == 0] + [index+10 for index, outcome in enumerate(games2) if outcome == 1])
print('\nMovement Berserker Won', winrate, 'percent of the time against Defense Berserker!')
print('Movement Berserker drew against Defense Berserker', len(draws), 'times!')
