from unit.unit import Unit


class Colony(Unit):
    def __init__(self, ID, position, grid_size, can_move=False):
        super().__init__(ID, position, grid_size, can_move)
        self.name = 'Colony'
        self.income = 5
        self.label = 'Colony' + str(self.income)
        self.armor = 0
