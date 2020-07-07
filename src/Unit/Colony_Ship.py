from Unit.Unit import Unit


class Colony_Ship(Unit):
    def __init__(self, ID, position, grid_size, can_move, attack_tech=0, defense_tech=0, speed_tech=0):
        super().__init__(ID, position, grid_size, can_move,
                         attack_tech, defense_tech, speed_tech)
        self.name = 'Colony Ship'
        self.label = 'CO'
        self.hull_size = 1
        self.attack = 0
        self.defense = 0
        self.armor = 0
        self.cost = 8
        self.fighting_class = 0
