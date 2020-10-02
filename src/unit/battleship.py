from unit.unit import Unit


class Battleship(Unit):
    def __init__(self, player, position, grid_size, can_move, attack_tech=0, defense_tech=0, movement_tech=0):
        super().__init__(player, position, grid_size, can_move,
                         attack_tech, defense_tech, movement_tech)
        self.name = 'Battleship'
        self.label = 'BB'
        self.player = player
        self.hull_size = 5
        self.attack = 5
        self.defense = 2
        self.armor = 3
        self.cost = 20
        self.fighting_class = 4
