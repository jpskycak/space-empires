import random
from board import Board
from unit.decoy import Decoy
from unit.colony_ship import Colony_Ship
from unit.colony import Colony
from unit.miner import Miner

class CombatEngine:
    def __init__(self, board, game, grid_size, asc_or_dsc):
        self.board = board
        self.game = game
        self.grid_size = grid_size
        self.dice_roll_index = 0
        if asc_or_dsc == 'asc':
            self.rolls = [1, 2, 3, 4, 5, 6]
        elif asc_or_dsc == 'dsc':
            self.rolls = [6, 5, 4, 3, 2, 1]
        print('asc_or_dsc', asc_or_dsc)

    def complete_all_combats(self, ships):
        print('\nships', ships)
        fixed_ships = [ship for ship in ships if not isinstance(ship, Colony) and not isinstance(ship, Colony_Ship) and not isinstance(ship, Decoy) and not isinstance(ship, Miner)]
        while self.more_than_one_player_left_fighting(fixed_ships):
            print('\norder 69', fixed_ships)
            attacking_ship = fixed_ships[0]
            defending_ship = self.get_next_enemy_ship(fixed_ships[0:], attacking_ship)
            print('attacking_ship', attacking_ship)
            print('defending_ship', defending_ship) 
            if defending_ship != None and attacking_ship != None:
                ship_who_won = self.start_fight(attacking_ship, defending_ship)  # make 'em fight
                self.remove_loser_ship(fixed_ships, attacking_ship, defending_ship, ship_who_won)
                
    def remove_loser_ship(self, ships, attacking_ship, defending_ship, ship_who_won):
        if ship_who_won == 1:
            print(defending_ship in ships)
            print(defending_ship in defending_ship.player.ships)
            defending_ship.player.ships.remove(defending_ship)
            ships.remove(defending_ship)
        else: 
            print(attacking_ship in ships)
            print(attacking_ship in attacking_ship.player.ships)
            attacking_ship.player.ships.remove(attacking_ship)
            ships.remove(attacking_ship)

    def more_than_one_player_left_fighting(self, ships):
        players = [ships[0].player]
        for ship in ships[1:]:
            if ship.player not in players:
                return True
        return False

        
    def get_next_enemy_ship(self, ships, attacking_ship):
        for ship in ships:
            #print('ship.player', ship.player)
            #print('attacking_ship.player', attacking_ship.player)
            #print('ship.player = attacking_ship.player', ship.player != attacking_ship.player)
            if ship.player != attacking_ship.player:
                #print('hello')
                return ship

    def start_fight(self, ship_1, ship_2):
        #print('FIGHT')
        if ship_1.status != 'Deceased' and ship_2.status != 'Deceased':
            if self.ship_1_fires_first(ship_1, ship_2):
                print("Player", ship_1.player.player_number, "'s", ship_1.name, ship_1.ID, "vs Player", ship_2.player.player_number, "'s", ship_2.name, ship_2.ID)
                self.attack(ship_1, ship_2)
            else:
                print("Player", ship_1.player.player_number, "'s", ship_1.name, ship_1.ID, "vs Player", ship_2.player.player_number, "'s", ship_2.name, ship_2.ID)
                self.attack(ship_2, ship_1)
            #print('ship_1.armor', ship_1.armor)
            #print('ship_2.armor', ship_2.armor)
            if ship_1.armor < 1:
                print("Player", ship_1.player.player_number, "'s unit was destroyed at co-ords", [ship_1.x, ship_1.y])
                print('-------------------------')
                return 2
            elif ship_2.armor < 1:
                print("Player", ship_2.player.player_number, "'s unit was destroyed at co-ords", [ship_2.x, ship_2.y])
                print('-------------------------')
                return 1

    def ship_1_fires_first(self, ship_1, ship_2):
        if ship_1.fighting_class > ship_2.fighting_class: return True
        elif ship_1.fighting_class < ship_2.fighting_class: return False
        else:
            if ship_1.attack_tech > ship_2.attack_tech: return True
            elif ship_1.attack_tech < ship_2.attack_tech: return False
            else:
                if ship_1.attack > ship_2.attack: return True
                elif ship_1.attack < ship_2.attack: return False
                else: return True
    # helping combat function
    def attack(self, ship_1, ship_2):
        player_1 = ship_1.player
        player_2 = ship_2.player
        hit_threshold = (ship_1.attack + player_1.attack_tech) - (ship_2.defense + player_2.defense_tech)
        die_roll = self.get_die_roll()
        if die_roll == 1 or die_roll <= hit_threshold:
            print('Player', player_1.player_number, 'Hit their shot, targeting Player', player_2.player_number, "'s unit", ship_2.name, ship_2.ID)
            ship_2.armor -= 1  # player 2's ship loses some armor
        else:
            print('Player', player_2.player_number, 'Missed their shot, targeting Player', player_1.player_number, "'s unit", ship_1.name, ship_1.ID)
            

    def get_die_roll(self):
        if self.dice_roll_index == 5:
            self.dice_roll_index = 0
        else:
            self.dice_roll_index += 1
        return self.rolls[self.dice_roll_index]

    def possible_fights(self):
        positions_of_ships = {}
        for x in range(0, self.grid_size + 1):
            for y in range(0, self.grid_size + 1):
                if self.is_a_possible_fight_at_x_y(x, y):
                    #print('self.board.ships_dict[(x, y)]', self.board.ships_dict[(x, y)])
                    positions_of_ships[(x, y)] = self.game.player.screen_ships(self.board.ships_dict[(x, y)], self.board)
                    print('positions_of_ships[(x, y)]', positions_of_ships[(x, y)])
        return positions_of_ships

    def is_a_possible_fight_at_x_y(self, x, y):
        self.board.update_board()
        if (x, y) in self.board.ships_dict:
            #print('self.board.ships_dict[(x, y)]', self.board.ships_dict[(x, y)])
            ships = self.board.ships_dict[(x, y)]
            player_1 = ships[0].player
            for ship in ships[0:]:
                #print('player_1, ship.player', player_1, ship.player)
                if ship.player != player_1:
                    return True
                
        return False
