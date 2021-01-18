from unit.unit import Unit


class Colony(Unit):
    def __init__(self, player, position, board_size, ID, home_base=False):
        super().__init__(player, position, board_size, ID)
        self.player = player
        self.status = 'Alive'
        if home_base:
            self.type = 'Home Base'
            self.income = 20
        else:
            self.type = 'Colony'
            self.income = 5
        self.label = self.type, self.income
        self.armor = 0
