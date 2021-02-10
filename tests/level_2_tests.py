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

def run_simuations(strats, number_of_simulations):
    first_half = run_half_simulations(strats, number_of_simulations // 2, 0)
    second_half = run_half_simulations(strats[::-1], number_of_simulations // 2, number_of_simulations // 2 + 1)
    draws = [game for game in (first_half + second_half) if game == None]# + [game for game in second_half if game is None]
    return (first_half.count(0) + second_half.count(1)) / ((number_of_simulations - len(draws)) * .01), draws

def run_half_simulations(strats, number_of_simulations, seed_offset):
    winner = []
    for i in range(0, number_of_simulations):
        random.seed(i+seed_offset)
        game = Game(strats, (5,5), 'random', print_state_obsolete=False, can_log=False, number_of_economic_phases=1, build_player_ship_yards=True, max_turns=5, number_of_movement_rounds=1)
        game.initialize_game()
        winner.append(game.play())
    return winner

print('\nBerserker vs Berserker')

#Attack Berserker vs Defense Berserker
strat_choices = [AttackBerserkerStrategyLevel2, DefenseBerserkerStrategyLevel2]
winrate, draws = run_simuations(strat_choices, 1000)
print('\nAttack Berserker Won', winrate, 'percent of the time against Defense Berserker!')
print('Attack Berserker drew against Defense Berserker', len(draws), 'times!')

#Attack Berserker vs Movement Berserker
strat_choices = [AttackBerserkerStrategyLevel2, MovementBerserkerStrategyLevel2]
winrate, draws = run_simuations(strat_choices, 1000)
print('\nAttack Berserker Won', winrate, 'percent of the time against Movement Berserker!')
print('Attack Berserker drew against Movement Berserker', len(draws), 'times!')

#Attack Berserker vs Numbers Berserker
strat_choices = [AttackBerserkerStrategyLevel2, NumbersBerserkerStrategyLevel2]
winrate, draws = run_simuations(strat_choices, 1000)
print('\nAttack Berserker Won', winrate, 'percent of the time against Numbers Berserker!')
print('Attack Berserker drew against Numbers Berserker', len(draws), 'times!')

#Defense Berserker vs Movement Berserker
strat_choices = [DefenseBerserkerStrategyLevel2, MovementBerserkerStrategyLevel2]
winrate, draws = run_simuations(strat_choices, 1000)
print('\nDefense Berserker Won', winrate, 'percent of the time against Movement Berserker!')
print('Defense Berserker drew against Movement Berserker', len(draws), 'times!')

#Defense Berserker vs Numbers Berserker
strat_choices = [DefenseBerserkerStrategyLevel2, NumbersBerserkerStrategyLevel2]
winrate, draws = run_simuations(strat_choices, 1000)
print('\nDefense Berserker Won', winrate, 'percent of the time against Numbers Berserker!')
print('Defense Berserker drew against Numbers Berserker', len(draws), 'times!')

#Movement Berserker vs Numbers Berserker
strat_choices = [MovementBerserkerStrategyLevel2, NumbersBerserkerStrategyLevel2]
winrate, draws = run_simuations(strat_choices, 1000)
print('\nMovement Berserker Won', winrate, 'percent of the time against Numbers Berserker!')
print('Movement Berserker drew against Numbers Berserker', len(draws), 'times!')

print('\nFlanker vs Berserker')

#Flanker vs Attack Berserker
strat_choices = [FlankerStrategyLevel2, AttackBerserkerStrategyLevel2]
winrate, draws = run_simuations(strat_choices, 1000)
print('\nFlanker Won', winrate, 'percent of the time against Attack Berserker!')
print('Flanker drew against Attack Berserker', len(draws), 'times!')

#Flanker vs Defense Berserker
strat_choices = [FlankerStrategyLevel2, DefenseBerserkerStrategyLevel2]
winrate, draws = run_simuations(strat_choices, 1000)
print('\nFlanker Won', winrate, 'percent of the time against Defense Berserker!')
print('Flanker drew against Defense Berserker', len(draws), 'times!')

#Flanker vs Movement Berserker
strat_choices = [FlankerStrategyLevel2, MovementBerserkerStrategyLevel2]
winrate, draws = run_simuations(strat_choices, 1000)
print('\nFlanker Won', winrate, 'percent of the time against Movement Berserker!')
print('Flanker drew against Movement Berserker', len(draws), 'times!')

#Flanker vs Numbers Berserker
strat_choices = [FlankerStrategyLevel2, NumbersBerserkerStrategyLevel2]
winrate, draws = run_simuations(strat_choices, 1000)
print('\nFlanker Won', winrate, 'percent of the time against Numbers Berserker!')
print('Flanker drew against Numbers Berserker', len(draws), 'times!')

print('\nColby vs ...')

#Colby vs Attack Berserker
strat_choices = [ColbyStrategyLevel2, AttackBerserkerStrategyLevel2]
winrate, draws = run_simuations(strat_choices, 1000)
print('\nColby Won', winrate, 'percent of the time against Attack Berserker!')
print('Colby drew against Attack Berserker', len(draws), 'times!')

#Colby vs Defense Berserker
strat_choices = [ColbyStrategyLevel2, DefenseBerserkerStrategyLevel2]
winrate, draws = run_simuations(strat_choices, 1000)
print('\nColby Won', winrate, 'percent of the time against Defense Berserker!')
print('Colby drew against Defense Berserker', len(draws), 'times!')

#Colby vs Movement Berserker
strat_choices = [ColbyStrategyLevel2, MovementBerserkerStrategyLevel2]
winrate, draws = run_simuations(strat_choices, 1000)
print('\nColby Won', winrate, 'percent of the time against Movement Berserker!')
print('Colby drew against Movement Berserker', len(draws), 'times!')

#Colby vs Numbers Berserker
strat_choices = [ColbyStrategyLevel2, NumbersBerserkerStrategyLevel2]
winrate, draws = run_simuations(strat_choices, 1000)
print('\nColby Won', winrate, 'percent of the time against Numbers Berserker!')
print('Colby drew against Numbers Berserker', len(draws), 'times!')

#Colby vs Flanker
strat_choices = [ColbyStrategyLevel2, FlankerStrategyLevel2]
winrate, _ = run_simuations(strat_choices, 1000)
print('\nColby Won', winrate, 'percent of the time against Flanker!')
print('Colby drew against Defense Flanker', len(draws), 'times!')