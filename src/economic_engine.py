from unit.unit import Unit
from unit.scout import Scout
from unit.destroyer import Destroyer
from unit.cruiser import Cruiser
from unit.battle_cruiser import BattleCruiser
from unit.battleship import Battleship
from unit.dreadnaught import Dreadnaught
from unit.colony_ship import Colony_Ship
from unit.colony import Colony
from unit.ship_yard import Ship_Yard
from unit.base import Base
from unit.miner import Miner
from unit.decoy import Decoy
from unit.carrier import Carrier


class EconomicEngine:
    def __init__(self, board, game):
        self.board = board
        self.game = game

    def complete_all_taxes(self, game_state):
        for player in self.game.players:
            player.creds += self.income(player)
            if self.game.print_state_obsolete: print('Player', player.player_index,"'s income is", self.income(player))
            self.game.generate_full_state(phase='Economic')
            player.maintenance_cost = self.maintenance_cost(player, game_state)
            if player.creds < player.maintenance_cost:
                self.remove_ships(player)
            player.creds -= player.maintenance_cost
            if self.game.print_state_obsolete: print('Player', player.player_index, "'s maintenance is", player.maintenance_cost)
            self.game.generate_full_state(phase='Economic')
            purchases = player.strategy.decide_purchases(game_state)
            for technology in purchases['technology']:
                upgrade_cost = player.upgrade_cost(technology, game_state)
                if player.creds > upgrade_cost:
                    player.upgrade(technology, game_state)
                    player.creds -= upgrade_cost
            ship_yard_build_stats = []
            for unit in purchases['units']:
                can_build = False
                ship_placement = unit['coords']
                ship = self.create_ship(player, unit['type'], ship_placement, player.board_size, player.new_ship_index)
                ship_size = player.technology['shipsize']
                shipsize_needed = game_state['unit_data'][ship.type]['shipsize_needed']
                hull_size_needed = game_state['unit_data'][ship.type]['hullsize']
                hull_size_capibility = player.find_amount_of_hull_size_building_capibility(ship_placement)
                if player.creds >= ship.cost and shipsize_needed >= ship_size and hull_size_capibility >= hull_size_needed:
                    can_build = True
                if ship.type == 'Shipyard':
                    colonies_at_ship_coords = [colony for colony in player.colonies if (colony.x, colony.y) == ship['coords'] and game_state['turn'] > colony.turn_built]
                    if len(colonies_at_ship_coords) > 0 and (ship.x,ship.y) not in ship_yard_build_stats:
                        ship_yard_build_stats.append((ship.x,ship.y)) 
                        can_build = True
                    else:
                        can_build = False
                if can_build:
                    player.ships.append(ship)
                    player.creds -= ship.cost
                    if self.game.print_state_obsolete: print('Player', player.player_index, "bought a", ship.type)
                    player.new_ship_index += 1
            self.game.generate_full_state(phase='Economic')

    def create_ship(self, player, ship, position, board_size, ID):
        if ship == 'Scout':
            return Scout(player, position, board_size, ID)
        elif ship == 'Destroyer':
            return Destroyer(player, position, board_size, ID)
        elif ship == 'Cruiser':
            return Cruiser(player, position, board_size, ID)
        elif ship == 'BattleCruiser':
            return BattleCruiser(player, position, board_size, ID)
        elif ship == 'Battleship':
            return Battleship(player, position, board_size, ID)
        elif ship == 'Dreadnaught':
            return Dreadnaught(player, position, board_size, ID)
        elif ship == 'Carrier':
            return Carrier(player, position, board_size, ID)
        elif ship == 'Miner':
            return Miner(player, position, board_size, ID)
        elif ship == 'Colony_Ship':
            return Colony_Ship(player, position, board_size, ID)
        else:
            return Scout(player, position, board_size, ID)

    def income(self, player):
        income = 0
        for colony in player.colonies:
            income += colony.income
        income += player.home_base.income
        return income

    def remove_ships(self, player):
        total_cost = player.maintenance_cost
        removal_ids = []
        removal_id = None
        while total_cost > player.creds:
            self.game.generate_full_state(phase='Combat')
            hidden_game_state = self.game.hidden_game_state_state
            removal_id = player.strategy.decide_removal(hidden_game_state)
            ship = next([ship for ship in player.ships if ship.ID == removal_id])
            if self.game.print_state_obsolete: print('Player', player.player_index, "couldn't maintain their", ship.type, 'ID', index)
            removal_ids.append(removal_id)
        player.ships = [ship for ship in player.ships if ship.ID not in removal_ids]

    def maintenance_cost(self, player, game_state):
        total_cost = 0
        for ship in player.ships:
            if not isinstance(ship, Base) and not isinstance(ship, Colony) and not isinstance(ship, Colony_Ship) and not isinstance(ship, Decoy):
                cost = game_state['unit_data'][ship.type]['maintenance']
                total_cost += cost
        return total_cost

    def generate_economic_state(self, player, game_state):
        return [{'income': self.income(player), 'maintenance cost': self.maintenance_cost(player, game_state)}]
