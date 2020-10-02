from unit.unit import Unit


class Miner(Unit):
    def __init__(self, player, position, grid_size, can_move=True, movement_tech=0):
        super().__init__(player, position, grid_size, can_move, movement_tech)
        self.name = 'Miner'
        self.label = 'Miner'
        self.player = player
        self.hull_size = 1
        self.attack = 0
        self.defense = 0
        self.armor = 0
        self.cost = 5
        self.asteroid = []
