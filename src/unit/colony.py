from unit.unit import Unit


class Colony(Unit):
    def __init__(self, player, position, board_size, ID, turn_built, home_base=False):
        super().__init__(player, position, board_size, ID)
        self.player = player
        self.is_alive = True
        if home_base:
            self.type = 'Home Base'
            self.income = 30
            self.attack = 0
            self.defense = 0
            self.hits_left = 1
            self.fighting_class = -1
        else:
            self.type = 'Colony'
            self.income = 5
        self.label = self.type, self.income
        self.armor = 0
        self.turn_built = turn_built
