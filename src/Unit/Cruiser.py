from Unit import Unit


class Cruiser(Unit):
    def __init__(self, ID, position, grid_size, can_move, attack_tech=0, defense_tech=0, movement_tech=0):
        super().__init__(ID, position, grid_size, can_move,
                         attack_tech, defense_tech, movement_tech)
        self.name = 'Cruiser'
        self.label = 'CV'
        self.hull_size = 3
        self.attack = 4
        self.defense = 1
        self.armor = 2
        self.cost = 12
        self.fighting_class = 2
