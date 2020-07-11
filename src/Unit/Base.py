from unit.unit import Unit


class Base(Unit):
    def __init__(self, ID, position, grid_size, can_move=False, attack_tech=0, defense_tech=0):
        super().__init__(ID, position, grid_size, can_move, attack_tech, defense_tech)
        self.name = 'Base'
        self.label = 'Base'
        self.hull_size = 2
        self.attack = 7
        self.defense = 2
        self.armor = 3
        self.cost = 12
        self.fighting_class = 4
