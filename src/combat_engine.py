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
        self.asc_or_dsc = asc_or_dsc
        if self.asc_or_dsc != 'random':
            if self.asc_or_dsc == 'asc': self.rolls = [1, 2, 3, 4, 5, 6]
            elif self.asc_or_dsc == 'dsc': self.rolls = [6, 5, 4, 3, 2, 1]
            self.current_roll = self.rolls[self.dice_roll_index]

    def complete_all_fights(self, hidden_game_state, screen_ships):
        if self.game.print_state_obsolete: print('-------------------------')
        possible_fights = self.possible_fights()
        for _, ships in possible_fights.items():
            if not self.game.game_won:
                self.complete_all_combats(ships, hidden_game_state, screen_ships)

    def complete_all_combats(self, ships, hidden_game_state, screen_ships):
        #screened_ships = ...
        fixed_ships = [ship for ship in ships if not ship.type == 'Colony' and not ship.type == 'Colony Ship' and not ship.type == 'Decoy' and not ship.type == 'Miner']# and not in screened_ships]
        for ship in [ship for ship in ships if ship not in fixed_ships]:
            if ship.type == 'Colony': ship.player.colonies.remove(ship)
            else: ship.player.ships.remove(ship)
        ships_that_shot = []
        while self.more_than_one_player_left_fighting(fixed_ships):
            self.game.generate_full_state(phase='Combat')
            if len(ships_that_shot) >= len(fixed_ships): ships_that_shot = []
            if self.asc_or_dsc != 'random': self.current_roll = self.rolls[self.dice_roll_index]
            else: self.current_roll = random.randint(0,10)
            attacking_ship = self.get_next_ally_ship(fixed_ships, ships_that_shot)
            defending_ship_index = attacking_ship.player.strategy.decide_which_unit_to_attack(self.game.hidden_game_state_state, (attacking_ship.x, attacking_ship.y), fixed_ships.index(attacking_ship))
            defending_ship_dict = self.combat_dict[(attacking_ship.x, attacking_ship.y)][defending_ship_index]
            for ship in fixed_ships:
                if defending_ship_dict == {'unit': ship.ID, 'player': ship.player.player_index}:
                    defending_ship = ship
                    break
            if defending_ship != None and attacking_ship != None:
                hit_or_miss = self.start_fight(attacking_ship, defending_ship)  # make'em fight
                if not defending_ship.is_alive:
                    if defending_ship.type == 'Shipyard': defending_ship.player.ship_yards.remove(defending_ship)
                    elif defending_ship.type == 'Home Base':
                        defending_ship.is_alive = False
                        defending_ship.player.is_alive = False
                        if self.game.print_state_obsolete: 
                            print('Player', attacking_ship.player.player_index, 'destroyed Player', defending_ship.player.player_index, "'s Home Base")
                            print('---------------------------------------------')
                        self.game.game_won = True
                        break
                    else: defending_ship.player.ships.remove(defending_ship)
                    fixed_ships.remove(defending_ship)
                ships_that_shot.append(attacking_ship)
            if self.asc_or_dsc != 'random':
                self.dice_roll_index += 1
                if self.dice_roll_index > 5: self.dice_roll_index = 0
                self.current_roll = self.rolls[self.dice_roll_index]
            else:
                self.current_roll = random.randint(0,10)

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
        if self.game.print_state_obsolete: print("Player", ship_1.player.player_index, "'s", ship_1.type, ship_1.ID, "vs Player", ship_2.player.player_index, "'s", ship_2.type, ship_2.ID)
        hit_or_miss = self.attack(ship_1, ship_2)
        if ship_2.hits_left < 1:
            if self.game.print_state_obsolete: 
                print("Player", ship_2.player.player_index, "'s", ship_2.type, ship_2.ID, "was destroyed at co-ords", [ship_2.x, ship_2.y])
                print('-------------------------')
            ship_2.is_alive = False
        return hit_or_miss

    # helping combat function
    def attack(self, ship_1, ship_2):
        player_1 = ship_1.player
        player_2 = ship_2.player
        hit_threshold = (ship_1.attack + player_1.technology['attack']) - (ship_2.defense + player_2.technology['defense'])
        if self.current_roll == 1 or self.current_roll <= hit_threshold:
            if self.game.print_state_obsolete: print('Player', player_1.player_index, 'Hit their shot, targeting Player', player_2.player_index, "'s", ship_2.type, ship_2.ID)
            ship_2.hits_left -= ship_1.attack + ship_1.technology['attack']  # player 2's ship loses some hits_left
            return 'Hit'
        else:
            if self.game.print_state_obsolete: print('Player', player_1.player_index, 'Missed their shot, targeting Player', player_2.player_index, "'s", ship_2.type, ship_2.ID)
            return 'Miss'

    def possible_fights(self):
        positions_of_ships = {}
        for x in range(0, self.board_size[0] + 1):
            for y in range(0, self.board_size[1] + 1):
                if self.is_a_possible_fight_at_x_y(x, y):
                    for ship in self.board.ships_dict[(x, y)]:
                        if self.if_it_cant_fight(ship):
                            if ship.type == 'Colony': ship.player.colonies.remove(ship)
                            else: ship.player.ships.remove(ship)
                    positions_of_ships[(x, y)] = [ship for ship in self.game.board.simple_sort(self.board.ships_dict[(x, y)]) if not self.if_it_cant_fight(ship)]
        return positions_of_ships

    def if_it_cant_fight(self, ship): return ship.type == 'Colony' and ship.type == 'Decoy' and ship.type == 'Miner' and ship.type == 'Colony Ship'

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
        self.combat_dict = {}
        for coords, ships in self.possible_fights().items():
            combat_at_location_arr = []
            for ship in ships:
                combat_at_location_arr.append({'player': ship.player.player_index, 'unit': ship.ID})
            self.combat_dict[coords] = combat_at_location_arr
        return self.combat_dict
