from Unit import Unit


class Destroyer(Unit):
    def __init__(self, ID, position, grid_size, can_move, attack_tech=0, defense_tech=0, speed_tech=0):
        super().__init__(ID, position, grid_size, can_move,
                         attack_tech, defense_tech, speed_tech)
        self.name = 'Destroyer'
        self.label = 'DD'
        self.hull_size = 2
        self.attack = 4
        self.defense = 0
        self.armor = 1
        self.cost = 9
        self.fighting_class = 1
