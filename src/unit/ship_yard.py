from unit.unit import Unit


class Ship_Yard(Unit):
    def __init__(self, player, position, board_size, ID):
        super().__init__(player, position, board_size, ID)
        self.position = position
        self.type = 'Shipyard'
        self.label = 'SY'
        self.player = player
        self.hull_size = 1
        self.attack = 3
        self.defense = 0
        self.hits_left = 1
        self.cost = 6
        self.fighting_class = 2
        self.can_move = False
        self.technology = {'attack': 0, 'defense': 0, 'movement': 1, 'tactics': 0}
