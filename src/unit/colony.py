from unit.unit import Unit


class Colony(Unit):
    def __init__(self, player, ID, position, grid_size, home_base = False, can_move=False):
        super().__init__(player, ID, position, grid_size, can_move)
        self.player = player
        self.status = 'Alive'
        if home_base:
            self.name = 'Home Base'
            self.income = 20
        else:
            self.name = 'Colony'
            self.income = 5
        self.label = self.name, self.income
        self.armor = 0
