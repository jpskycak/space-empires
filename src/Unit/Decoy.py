from Unit.Unit import Unit


class Decoy(Unit):
    def __init__(self, ID, position, grid_size, can_move=True, speed_tech=0):
        super().__init__(ID, position, grid_size, can_move, speed_tech)
        self.name = 'Decoy'
        self.label = 'Decoy'
        self.hull_size = 1
        self.attack = 0
        self.defense = 0
        self.armor = 0
        self.cost = 5
