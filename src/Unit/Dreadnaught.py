from Unit import Unit


class Dreadnaught(Unit):
    def __init__(self, ID, position, grid_size, can_move, attack_tech=0, defense_tech=0, speed_tech=0):
        super().__init__(ID, position, grid_size, can_move,
                         attack_tech, defense_tech, speed_tech)
        self.name = 'Dreadnaught'
        self.label = 'DN'
        self.hull_size = 6
        self.attack = 6
        self.defense = 3
        self.armor = 3
        self.cost = 24
        self.fighting_class = 4
