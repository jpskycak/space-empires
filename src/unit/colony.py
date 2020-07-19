from unit.unit import Unit


class Colony(Unit):
    def __init__(self, player, ID, position, grid_size, can_move=False):
        super().__init__(player, ID, position, grid_size, can_move)
        self.name = 'Colony'
        self.player = player
        self.income = 5
        self.label = 'Colony' + str(self.income)
        self.armor = 0
