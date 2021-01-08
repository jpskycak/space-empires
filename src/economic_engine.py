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

    def complete_all_taxes(self, turn):
        for player in self.game.players:
            player.creds += self.income(player)
            print('Player', player.player_number, "'s income is", self.income(player))
            maintenance_cost = self.maintenance(player, turn)
            player.creds -= maintenance_cost
            print('Player', player.player_number, "'s maintenance is", maintenance_cost)
            purchase = player.strategy.decide_purchases(self.game.game_state)
            for unit in purchase['units']:
                ship = self.create_ship(player, unit, player.strategy.decide_ship_placement(
                        self.game.game_state), player.grid_size, player.new_ship_index)
                if player.creds >= ship.cost:
                    player.ships.append(ship)
                    player.creds -= ship.cost
                    print('Player', player.player_number, "bought a", ship.name)
                    player.new_ship_index += 1
            for technology in purchase['technology']:
                if player.creds > player.upgrade_costs(technology):
                    player.upgrade(technology)
            self.game.generate_state()

    def create_ship(self, player, ship, position, grid_size, ID):
        if isinstance(ship, Scout):
            return Scout(player, position, grid_size, ID, True)
        elif isinstance(ship, Destroyer):
            return Destroyer(player, position, grid_size, ID, True)
        elif isinstance(ship, Cruiser):
            return Cruiser(player, position, grid_size, ID, True)
        elif isinstance(ship, BattleCruiser):
            return BattleCruiser(player, position, grid_size, ID, True)
        elif isinstance(ship, Battleship):
            return Battleship(player, position, grid_size, ID, True)
        elif isinstance(ship, Dreadnaught):
            return Dreadnaught(player, position, grid_size, ID, True)
        elif isinstance(ship, Carrier):
            return Carrier(player, position, grid_size, ID, True)
        elif isinstance(ship, Colony_Ship):
            return Colony_Ship(player, position, grid_size, ID, True)
        else:
            return Scout(player, position, grid_size, ID, True)

    def can_upgrade(self, player):
        return player.creds > 10 * player.attack_tech \
            or player.creds > 10 * player.defense_tech \
            or player.creds > 5 * player.fighting_class_tech + 10 \
            or player.creds > 10 * player.movement_tech_upgrade_number + 10 \
            or player.creds > 10 * player.ship_yard_tech \
            or player.creds > 15 * player.terraform_tech \

    def income(self, player):
        income = 0
        for colony in player.colonies:
            income += colony.income
        income += player.home_base.income
        return income

    def maintenance(self, player, turn):
        total_cost = 0
        for ship in player.ships:
            if not isinstance(ship, Base) and not isinstance(ship, Colony) and not isinstance(ship, Colony_Ship) and not isinstance(ship, Decoy):
                cost = ship.defense_tech + ship.defense + ship.armor
                if player.creds >= cost:
                    total_cost += cost
        if total_cost > player.creds:
            removal_index = player.strategy.decide_removal(self.game.game_state, turn)
            print('Player', player.player_number, "couldn't maintain their", [('ID', index, 'Name', ship.name) for index, ship in enumerate(player.ships) if index == removal_index])
        player.ships = [ship for index, ship in enumerate(player.ships) if index !=  removal_index]
        return total_cost

    def generate_economic_state(self, player, turn):
        return [{'income': self.income(player), 'maintenance cost': self.maintenance(player, turn)}]
