import random
from board import Board

class CombatEngine:
    def __init__(self, board, game, grid_size):
        self.board = board
        self.game = game
        self.grid_size = grid_size

    def complete_all_combats(self, order):
        print('order 69', order)
        if order != []:
            attacking_ship = order[0]
            defending_ship = order[random.randint(1, len(order))]

            self.ship_duel(attacking_ship, defending_ship)  # make 'em fight

    def ship_duel(self, ship_1, ship_2):
        print('FIGHT')
        if ship_1.status != 'Deceased' and ship_2.status != 'Deceased':

            if ship_1.fighting_class > ship_2.fighting_class:
                print("Player", ship_1.player.player_number, "'s", ship_1.name, ship_1.ID,
                      "vs Player", ship_2.player.player_number, "'s", ship_2.name, ship_2.ID)
                return self.hit_or_miss(ship_1, ship_2, 1)
            else:
                print("Player", ship_1.player.player_number, "'s", ship_1.name, ship_1.ID,
                      "vs Player", ship_2.player.player_number, "'s", ship_2.name, ship_2.ID)
                return self.hit_or_miss(ship_1, ship_2, 2)

            if ship_1.status == 'Deceased':
                print("Player", ship_1.player.player_number,
                      "'s unit was destroyed at co-ords", [ship_1.x, ship_1.y])
                found_creds = random.randint(1, 10)
                ship_1.player.creds -= found_creds
                ship_2.player.creds += found_creds
                print('Player', ship_2.player.player_number, 'found', found_creds,
                      'creds at co-ords', [ship_1.x, ship_1.y])
                print('-------------------------------------------')
                self.game.state_obsolete()

            elif ship_2.status == 'Deceased':
                print("Player", ship_2.player.player_number,
                      "'s unit was destroyed at co-ords", [ship_2.x, ship_2.y])
                found_creds = random.randint(1, 10)
                ship_1.player.creds += found_creds
                ship_2.player.creds -= found_creds
                print('Player', ship_1.player.player_number, 'found',
                      found_creds, 'creds at co-ords', [ship_2.x, ship_2.y])
                print('-------------------------------------------')
                self.game.state_obsolete()

    #helping combat function
    def hit_or_miss(self, ship_1, ship_2, first_to_shoot):
        print('fighting (hit or miss)')

        while ship_1.armor > 0 and ship_2.armor > 0:  # if neither are dead

            if first_to_shoot == 1:  # player 1 shoots first
                self.attack(ship_1, ship_2)  # player 1 attacks player 2
                self.attack(ship_2, ship_1)  # player 2 claps back at player 1

            elif first_to_shoot == 2:  # player 2 shoots first
                self.attack(ship_2, ship_1)  # player 2 attacks player 1
                self.attack(ship_1, ship_2)  # player 1 claps back at player 2

        if ship_1.armor < 0:  #
            ship_1.status = 'Deceased'  # change statuses
            return 2

        elif ship_2.armor < 0:  # of dead ships
            ship_2.status = 'Deceased'
            return 1
    
    def attack(self, ship_1, ship_2):
        player_1 = ship_1.player
        player_2 = ship_2.player
        hit_threshold = (ship_1.attack + player_1.attack_tech) - (ship_2.defense + player_2.defense_tech)
        die_roll = random.randint(1, 6)

        if die_roll == 1 or die_roll <= hit_threshold:
            print('Player', player_1.player_number,
                  'Hit their shot, targeting Player',
                  player_2.player_number, "'s unit", ship_2.name,
                  ship_2.ID)
            ship_2.armor -= 1  # player 2's ship loses some armor

        else:
            print('Player', player_2.player_number,
                    'Missed their shot, targeting Player',
                    player_1.player_number, "'s unit", ship_1.name,
                    ship_1.ID)

    def possible_fights(self):
        positions_of_ships = []

        for i in range(0, self.grid_size + 1):

            for j in range(0, self.grid_size + 1):

                if len(self.board.list_of_ships_at_x_y(self.board.players, i, j)) > 0:

                    positions_of_ships.append(self.board.list_of_ships_at_x_y(self.board.players, i, j))  # ex below
        # tuples so no change #(((1,1), (3, [ship_1, ship_2, ship_1])), ((2,3), (2, [ship_1, ship_2])))
        print('positions_of_ships', positions_of_ships)
        return positions_of_ships
