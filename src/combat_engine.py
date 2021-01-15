import random
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
        if asc_or_dsc == 'asc':
            self.rolls = [1, 2, 3, 4, 5, 6]
        elif asc_or_dsc == 'dsc':
            self.rolls = [6, 5, 4, 3, 2, 1]
        self.current_roll = self.rolls[self.dice_roll_index]

    def complete_all_fights(self):
        possible_fights = self.possible_fights()
        for _, ships in possible_fights.items():
            self.complete_all_combats(ships)

    def complete_all_combats(self, ships):
        fixed_ships = [ship for ship in ships if not isinstance(ship, Colony) and not isinstance(
            ship, Colony_Ship) and not isinstance(ship, Decoy) and not isinstance(ship, Miner)]
        for ship in [ship for ship in ships if ship not in fixed_ships]:
            ship.player.ships.remove(ship)
        ships_that_shot = []
        while self.more_than_one_player_left_fighting(fixed_ships):
            if len(ships_that_shot) == len(fixed_ships):
                ships_that_shot = []
            self.current_roll = self.rolls[self.dice_roll_index]
            attacking_ship = self.get_next_ally_ship(fixed_ships, ships_that_shot)
            defending_ship_dict = attacking_ship.player.strategy.decide_which_unit_to_attack(
                self.generate_combat_array(), attacking_ship.player.ships.index(attacking_ship), (attacking_ship.x, attacking_ship.y))
            for ship in self.game.players[defending_ship_dict['player']-1].ships:
                if ship.ID == defending_ship_dict['unit']:
                    defending_ship = ship
                    break
            if defending_ship != None and attacking_ship != None:
                hit_or_miss = self.start_fight(
                    attacking_ship, defending_ship)  # make'em fight
                if not defending_ship.is_alive:
                    defending_ship.player.ships.remove(defending_ship)
                    fixed_ships.remove(defending_ship)
                ships_that_shot.append(attacking_ship)
            self.dice_roll_index += 1
            if self.dice_roll_index > 5:
                self.dice_roll_index = 0
            self.current_roll = self.rolls[self.dice_roll_index]

    def more_than_one_player_left_fighting(self, ships):
        if ships != []:
            players = [ships[0].player]
            for ship in ships[1:]:
                if ship.player not in players:
                    return True
        return False

    def get_next_ally_ship(self, fixed_ships, ships_that_missed):
        for ship in fixed_ships:
            if ship not in ships_that_missed:
                return ship

    def start_fight(self, ship_1, ship_2):
        print("Player", ship_1.player.player_number, "'s", ship_1.name, ship_1.ID,
              "vs Player", ship_2.player.player_number, "'s", ship_2.name, ship_2.ID)
        hit_or_miss = self.attack(ship_1, ship_2)
        if ship_2.armor < 1:
            print("Player", ship_2.player.player_number,
                  "'s unit was destroyed at co-ords", [ship_2.x, ship_2.y])
            print('-------------------------')
            ship_2.is_alive = False
        return hit_or_miss

    # helping combat function
    def attack(self, ship_1, ship_2):
        player_1 = ship_1.player
        player_2 = ship_2.player
        hit_threshold = (ship_1.attack + player_1.attack_tech) - \
            (ship_2.defense + player_2.defense_tech)
        die_roll = self.rolls[self.dice_roll_index]
        if die_roll == 1 or die_roll <= hit_threshold:
            print('Player', player_1.player_number, 'Hit their shot, targeting Player',
                  player_2.player_number, "'s unit", ship_2.name, ship_2.ID)
            ship_2.armor -= 1  # player 2's ship loses some armor
            return 'Hit'
        else:
            print('Player', player_1.player_number, 'Missed their shot, targeting Player',
                  player_2.player_number, "'s unit", ship_2.name, ship_2.ID)
            return 'Miss'

    def possible_fights(self):
        positions_of_ships = {}
        for x in range(0, self.board_size + 1):
            for y in range(0, self.board_size + 1):
                if self.is_a_possible_fight_at_x_y(x, y):
                    for ship in self.board.ships_dict[(x, y)]:
                        if not self.if_it_can_fight(ship):
                            ship.player.ships.remove(ship)
                    positions_of_ships[(x, y)] = [ship for ship in self.game.board.simple_sort(self.board.ships_dict[(x, y)]) if not isinstance(
                        ship, Colony) and not isinstance(ship, Colony_Ship) and not isinstance(ship, Decoy) and not isinstance(ship, Miner)]
        return positions_of_ships

    def if_it_can_fight(self, ship): return not isinstance(ship, Colony_Ship) and not isinstance(
        ship, Decoy) and not isinstance(ship, Miner) and not isinstance(ship, Colony)

    def is_a_possible_fight_at_x_y(self, x, y):
        self.board.update_board()
        if (x, y) in self.board.ships_dict:
            ships = self.board.ships_dict[(x, y)]
            player_1 = ships[0].player
            for ship in ships[0:]:
                if ship.player != player_1:
                    return True

        return False

    def generate_combat_array(self):
        combat_dict = {}
        for location, ships in self.possible_fights().items():
            combat_at_location_arr = []
            for ship in ships:
                combat_at_location_arr.append(
                    {'player': ship.player.player_number, 'unit': ship.ID})
            combat_dict[location] = combat_at_location_arr
        return combat_dict
