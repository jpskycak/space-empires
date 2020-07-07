from Unit.Unit import Unit


class Scout(Unit):
    def __init__(self, ID, position, grid_size, can_move, attack_tech=0, defense_tech=0, speed_tech=0):
        super().__init__(ID, position, grid_size, can_move,
                         attack_tech, defense_tech, speed_tech)
        self.name = 'Scout'
        self.label = 'SC'
        self.hull_size = 1
        self.attack = 3
        self.defense = 0
        self.armor = 1
        self.cost = 6
        self.fighting_class = 0
