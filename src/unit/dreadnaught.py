from unit.unit import Unit


class Dreadnaught(Unit):
    def __init__(self, player, ID, position, grid_size, can_move, attack_tech=0, defense_tech=0, movement_tech=0):
        super().__init__(player, ID, position, grid_size, can_move,
                         attack_tech, defense_tech, movement_tech)
        self.name = 'Dreadnaught'
        self.label = 'DN'
        self.player = player
        self.hull_size = 6
        self.attack = 6
        self.defense = 3
        self.armor = 3
        self.cost = 24
        self.fighting_class = 4
