from unit.unit import Unit


class Decoy(Unit):
    def __init__(self, player, ID, position, grid_size, can_move=True, movement_tech=0):
        super().__init__(player, ID, position, grid_size, can_move, movement_tech)
        self.name = 'Decoy'
        self.label = 'Decoy'
        self.player = player
        self.hull_size = 1
        self.attack = 0
        self.defense = 0
        self.armor = 0
        self.cost = 5
