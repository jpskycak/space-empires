from unit.unit import Unit


class Destroyer(Unit):
    def __init__(self, player, position, grid_size, can_move, attack_tech=0, defense_tech=0, movement_tech=0):
        super().__init__(player, position, grid_size, can_move,
                         attack_tech, defense_tech, movement_tech)
        self.name = 'Destroyer'
        self.label = 'DD'
        self.player = player
        self.hull_size = 2
        self.attack = 4
        self.defense = 0
        self.armor = 1
        self.cost = 9
        self.fighting_class = 1
