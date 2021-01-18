from unit.unit import Unit


class Dreadnaught(Unit):
    def __init__(self, player, position, board_size, ID):
        super().__init__(player, position, board_size, ID)
        self.type = 'Dreadnaught'
        self.label = 'DN'
        self.player = player
        self.hull_size = 6
        self.attack = 6
        self.defense = 3
        self.hits_left = 3
        self.cost = 24
        self.fighting_class = 4
