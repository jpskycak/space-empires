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
            self.maintenance(player, turn)
            purchase = player.strategy.decide_purchases(self.game.game_state)
            if not isinstance(purchase, int):  # if its not an upgrade
                ship = self.create_ship(player, purchase, player.strategy.decide_ship_placement(
                    self.game.game_state), player.grid_size, len(player.ships))
                while player.creds >= ship.cost:
                    purchase = player.strategy.decide_ship_purchases(
                        self.game.game_state)
                    ship = self.create_ship(player, purchase, player.strategy.decide_ship_placement(
                        self.game.game_state), self.game.grid_size, len(player.ships))
                    player.ships.append(ship)
                    player.creds -= ship.cost
            else:  # if it is an upgrade
                while self.can_upgrade(player):
                    upgrade = player.strategy.decide_purchases(
                        self.game.game_state)
                    player.upgrade(upgrade)

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
            and player.creds > 10 * player.defense_tech \
            and player.creds > 5 * player.fighting_class_tech + 10 \
            and player.creds > 10 * player.movement_tech_upgrade_number + 10 \
            and player.creds > 10 * player.ship_yard_tech \
            and player.creds > 15 * player.terraform_tech \

    def income(self, player):
        income = 0
        for colony in player.colonies:
            income += colony.income
        income += player.home_base.income
        return income

    def maintenance(self, player, turn):
        removals = []
        total_cost = 0
        for ship in player.ships:
            if not isinstance(ship, Base) and not isinstance(ship, Colony) and not isinstance(ship, Colony_Ship) and not isinstance(ship, Decoy):
                cost = ship.defense_tech + ship.defense + ship.armor
                if player.creds >= cost:
                    player.creds -= cost
                    total_cost += cost
                else:
                    removals.append(player.strategy.decide_removals(
                        self.game.game_state, turn))
                    #print('Player', player.player_number, "couldn't maintain their", ship.name)
        player.ships = [
            ship for ship in player.ships if ship.__dict__ not in removals]
        return total_cost

    def generate_economic_state(self, player, turn):
        return [{'income': self.income(player), 'maintenance cost': self.maintenance(player, turn)}]
