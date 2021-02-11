import random
import math
from board import Board
from unit.decoy import Decoy
from unit.colony_ship import Colony_Ship
from unit.colony import Colony
from unit.miner import Miner
from unit.scout import Scout


class CombatEngine:
    def __init__(self, board, game, board_size, asc_or_dsc):
        self.board = board
        self.game = game
        self.board_size = board_size
        self.dice_roll_index = 0
        self.asc_or_dsc = asc_or_dsc
        if self.asc_or_dsc != 'random':
            if self.asc_or_dsc == 'asc':
                self.rolls = [1, 2, 3, 4, 5, 6]
            elif self.asc_or_dsc == 'dsc':
                self.rolls = [6, 5, 4, 3, 2, 1]
            self.current_roll = self.rolls[self.dice_roll_index]

    def complete_all_fights(self):
        if self.game.print_state_obsolete:
            print('-------------------------')
        possible_fights = self.possible_fights()
        for location, ships in possible_fights.items():
            if not self.game.game_won:
                self.complete_all_combats(location, ships)

    def complete_all_combats(self, location, ships):
        #screened_ships = ...
        fixed_ships = [ship for ship in ships if not ship.type == 'Colony' and not ship.type == 'Colony Ship' and not ship.type == 'Decoy' and not ship.type == 'Miner' and (ship.x, ship.y) == location]  # and not in screened_ships]
        for ship in [ship for ship in ships if ship not in fixed_ships and (ship.x, ship.y) == location]:
            if ship.type == 'Colony':
                ship.player.colonies.remove(ship)
            else:
                ship.player.ships.remove(ship)
        ships_that_shot = []
        while self.more_than_one_player_left_fighting(fixed_ships):
            self.game.generate_state(phase='Combat')
            if len(ships_that_shot) >= len(fixed_ships):
                ships_that_shot = []
            if self.asc_or_dsc != 'random':
                self.current_roll = self.rolls[self.dice_roll_index]
            else:
                self.current_roll = math.floor(10*random.random()) + 1
            attacking_ship, defending_ship = self.get_attacker_and_defender_ships(
                location, fixed_ships, ships_that_shot)
            if defending_ship != None and attacking_ship != None:
                hit_or_miss = self.start_fight(
                    attacking_ship, defending_ship)  # make'em fight
                if not defending_ship.is_alive:
                    if defending_ship.type == 'Shipyard':
                        defending_ship.player.ship_yards.remove(defending_ship)
                    elif defending_ship.type == 'Home Base':
                        defending_ship.is_alive = False
                        defending_ship.player.is_alive = False
                        if self.game.print_state_obsolete:
                            print('Player', attacking_ship.player.player_index, 'destroyed Player',
                                  defending_ship.player.player_index, "'s Home Base")
                            print('---------------------------------------------')
                        self.game.game_won = True
                        break
                    else:
                        defending_ship.player.ships.remove(defending_ship)
                    fixed_ships.remove(defending_ship)
                ships_that_shot.append(attacking_ship)
                '''
            if self.asc_or_dsc != 'random':
                self.dice_roll_index += 1
                if self.dice_roll_index > 5: self.dice_roll_index = 0
                self.current_roll = self.rolls[self.dice_roll_index]
            else:
                self.current_roll = math.floor(10*random.random()) + 1'''

    def get_attacker_and_defender_ships(self, location, fixed_ships, ships_that_shot):
        attacking_ship = self.get_next_ally_ship(fixed_ships, ships_that_shot)
        self.game.generate_state(phase='Combat', current_player=self.game.players[attacking_ship.player.player_index - 1])
        defending_ship_index = attacking_ship.player.strategy.decide_which_unit_to_attack(self.game.game_state['combat'][location], location, fixed_ships.index(attacking_ship))
        defending_ship = next(ship for ship in fixed_ships if self.combat_dict[location][defending_ship_index] == {'unit': ship.ID, 'player': ship.player.player_index})
        return attacking_ship, defending_ship

    def more_than_one_player_left_fighting(self, ships):
        if ships != []:
            players = [ships[0].player]
            for ship in ships[1:]:
                if ship.player not in players:
                    return True
        return False

    def get_next_ally_ship(self, fixed_ships, ships_that_shot):
        return next(ship for ship in fixed_ships if ship not in ships_that_shot)

    def start_fight(self, ship_1, ship_2):
        if self.game.print_state_obsolete:
            print("Player", ship_1.player.player_index, "'s", ship_1.type, ship_1.ID,
                  "vs Player", ship_2.player.player_index, "'s", ship_2.type, ship_2.ID)
        hit_or_miss = self.attack(ship_1, ship_2)
        if ship_2.hits_left < 1:
            if self.game.print_state_obsolete:
                print("Player", ship_2.player.player_index, "'s", ship_2.type,
                      ship_2.ID, "was destroyed at co-ords", [ship_2.x, ship_2.y])
                print('-------------------------')
            ship_2.is_alive = False
        return hit_or_miss

    # helping combat function
    def attack(self, ship_1, ship_2):
        player_1 = ship_1.player
        player_2 = ship_2.player
        hit_threshold = (ship_1.attack + player_1.technology['attack']) - (
            ship_2.defense + player_2.technology['defense'])
        if self.current_roll == 1 or self.current_roll <= hit_threshold:
            if self.game.print_state_obsolete:
                print('Player', player_1.player_index, 'Hit their shot, targeting Player',
                      player_2.player_index, "'s", ship_2.type, ship_2.ID)
            # player 2's ship loses some hits_left
            ship_2.hits_left -= ship_1.attack + ship_1.technology['attack']
            return True
        else:
            if self.game.print_state_obsolete:
                print('Player', player_1.player_index, 'Missed their shot, targeting Player',
                      player_2.player_index, "'s", ship_2.type, ship_2.ID)
            return False

    def possible_fights(self):
        positions_of_ships = {}
        positions = [(x, y) for x in range(0, self.board_size[0]) for y in range(
            0, self.board_size[1]) if (x, y) in self.board.ships_dict.keys()]
        for (x, y) in positions:
            if self.is_a_possible_fight_at_x_y(x, y):
                for ship in self.board.ships_dict[(x, y)]:
                    if self.if_it_cant_fight(ship):
                        if ship.type == 'Colony':
                            ship.player.colonies.remove(ship)
                        else:
                            ship.player.ships.remove(ship)
                positions_of_ships[(x, y)] = [ship for ship in self.game.board.simple_sort(
                    self.board.ships_dict[(x, y)]) if not self.if_it_cant_fight(ship)]
        return positions_of_ships

    def if_it_cant_fight(self, ship):
        return ship.type == 'Colony' and ship.type == 'Decoy' and ship.type == 'Miner' and ship.type == 'Colony Ship'

    def is_a_possible_fight_at_x_y(self, x, y):
        self.board.update_board()
        ships = self.board.ships_dict[(x, y)]
        player_1 = ships[0].player
        for ship in ships[0:]:
            if ship.player != player_1:
                return True
        return False

    def generate_combat_array(self):
        self.combat_dict = {}
        for coords, ships in self.possible_fights().items():
            self.combat_dict[coords] = [
                {'player': ship.player.player_index, 'unit': ship.ID} for ship in ships]
        return self.combat_dict
