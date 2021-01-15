from unit.unit import Unit


class Ship_Yard(Unit):
    def __init__(self, player, position, board_size, can_move=False, attack_tech=0, defense_tech=0, ship_yard_tech=0):
        super().__init__(player, position, board_size, can_move,
                         attack_tech, defense_tech, ship_yard_tech)
        self.position = position
        self.name = 'Ship Yard'
        self.label = 'SY'
        self.player = player
        self.hull_size = 1
        self.attack = 3
        self.defense = 0
        self.armor = 1
        self.cost = 6
        self.fighting_class = 0
