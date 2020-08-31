import random
from board import Board


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

    def complete_all_combats(self, ships):
        while len(ships) > 1:
            print('order 69', ships)
            attacking_ship = ships[0]
            defending_ship = self.get_next_enemy_ship(ships, attacking_ship)
            print('defending_ship', defending_ship)
            defending_ship = ships[defending_ship]
            ship_who_won = self.setup_fight(attacking_ship, defending_ship)  # make 'em fight
            if ship_who_won == 1:
                ships.remove(defending_ship)
            else:
                ships.remove(attacking_ship)
        
    def get_next_enemy_ship(self, ships, attacking_ship):
        for ship in ships:
            if ship.player != attacking_ship.player:
                return ship

    def setup_fight(self, ship_1, ship_2):
        print('FIGHT')
        if ship_1.status != 'Deceased' and ship_2.status != 'Deceased':

            if ship_1.fighting_class > ship_2.fighting_class:
                print("Player", ship_1.player.player_number, "'s", ship_1.name, ship_1.ID, "vs Player", ship_2.player.player_number, "'s", ship_2.name, ship_2.ID)
                return self.hit_or_miss(ship_1, ship_2, 1)
            else:
                print("Player", ship_1.player.player_number, "'s", ship_1.name, ship_1.ID, "vs Player", ship_2.player.player_number, "'s", ship_2.name, ship_2.ID)
                return self.hit_or_miss(ship_1, ship_2, 2)

            if ship_1.status == 'Deceased':
                print("Player", ship_1.player.player_number, "'s unit was destroyed at co-ords", [ship_1.x, ship_1.y])
                print('-------------------------------------------')

            elif ship_2.status == 'Deceased':
                print("Player", ship_2.player.player_number, "'s unit was destroyed at co-ords", [ship_2.x, ship_2.y])
                print('-------------------------------------------')

    # helping combat function
    def hit_or_miss(self, ship_1, ship_2, first_to_shoot):
        print('fighting (hit or miss)')

        while ship_1.armor > 0 and ship_2.armor > 0:  # if neither are dead

            if first_to_shoot == 1:  # player 1 shoots first
                self.attack(ship_1, ship_2)  # player 1 attacks player 2
                self.attack(ship_2, ship_1)  # player 2 claps back at player 1

            elif first_to_shoot == 2:  # player 2 shoots first
                self.attack(ship_2, ship_1)  # player 2 attacks player 1
                self.attack(ship_1, ship_2)  # player 1 claps back at player 2

        if ship_2.armor <= 0:  # change statuses of dead ships
            ship_2.status = 'Deceased' 
            return 1

        elif ship_1.armor <= 0:
            ship_1.status = 'Deceased'
            return 2

    def attack(self, ship_1, ship_2):
        player_1 = ship_1.player
        player_2 = ship_2.player
        hit_threshold = (ship_1.attack + player_1.attack_tech) - (ship_2.defense + player_2.defense_tech)
        die_roll = self.get_die_roll

        if die_roll == 1 or die_roll <= hit_threshold:
            print('Player', player_1.player_number, 'Hit their shot, targeting Player', player_2.player_number, "'s unit", ship_2.name, ship_2.ID)
            ship_2.armor -= 1  # player 2's ship loses some armor

        else:
            print('Player', player_2.player_number, 'Missed their shot, targeting Player', player_1.player_number, "'s unit", ship_1.name, ship_1.ID)

    def possible_fights(self):
        positions_of_ships = {}

        for i in range(0, self.grid_size + 1):

            for j in range(0, self.grid_size + 1):
                self.board.ordered_list_of_ships_at_x_y(i, j)

                if len(self.board.ships_dict[(i, j)]) > 0:
                    positions_of_ships[(i, j)] = self.board.ships_dict[(i, j)]

        return positions_of_ships
