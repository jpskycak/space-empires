from unit.unit import Unit


class Colony_Ship(Unit):
    def __init__(self, player, position, grid_size, can_move, attack_tech=0, defense_tech=0, movement_tech=0):
        super().__init__(player, position, grid_size, can_move,
                         attack_tech, defense_tech, movement_tech)
        self.name = 'Colony Ship'
        self.label = 'CO'
        self.player = player
        self.hull_size = 1
        self.attack = 0
        self.defense = 0
        self.armor = 0
        self.cost = 8
        self.fighting_class = 0
        self.terraform_tech = 0
