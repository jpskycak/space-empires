from unit.unit import Unit


class Decoy(Unit):
    def __init__(self, player, position, board_size, ID):
        super().__init__(player, position, board_size, ID)
        self.type = 'Decoy'
        self.label = 'Decoy'
        self.player = player
        self.hull_size = 1
        self.attack = 0
        self.defense = 0
        self.hits_left = 0
        self.cost = 5
