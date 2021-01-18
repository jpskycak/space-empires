from unit.unit import Unit


class Base(Unit):
    def __init__(self, player, position, board_size, ID):
        super().__init__(player, position, board_size, ID)
        self.type = 'Base'
        self.label = 'Base'
        self.player = player
        self.hull_size = 2
        self.attack = 7
        self.defense = 2
        self.hits_left = 3
        self.cost = 12
        self.fighting_class = 4
        self.can_move = False
