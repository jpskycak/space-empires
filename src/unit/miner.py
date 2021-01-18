from unit.unit import Unit


class Miner(Unit):
    def __init__(self, player, position, board_size, ID):
        super().__init__(player, position, board_size, ID)
        self.type = 'Miner'
        self.label = 'Miner'
        self.player = player
        self.hull_size = 1
        self.attack = 0
        self.defense = 0
        self.hits_left = 0
        self.cost = 5
        self.asteroid = []
