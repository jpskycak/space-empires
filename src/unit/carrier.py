from unit.unit import Unit


class Carrier(Unit):
    def __init__(self, player, position, grid_size, can_move, attack_tech=0, defense_tech=0, movement_tech=0, stored_ships=[]):
        super().__init__(player, position, grid_size, can_move,
                         attack_tech, defense_tech, movement_tech)
        self.name = 'Carrier'
        self.label = 'CA'
        self.player = player
        self.attack = 1
        self.defense = 3
        self.armor = 1
        self.cost = 12
        self.fighting_class = 1
        self.stored_ships = stored_ships
