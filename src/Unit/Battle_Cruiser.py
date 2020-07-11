from unit.unit import Unit


class BattleCruiser(Unit):
    def __init__(self, ID, position, grid_size, can_move, attack_tech=0, defense_tech=0, movement_tech=0):
        super().__init__(ID, position, grid_size, can_move,
                         attack_tech, defense_tech, movement_tech)
        self.name = 'Battle Cruiser'
        self.label = 'BC'
        self.hull_size = 4
        self.attack = 5
        self.defense = 1
        self.armor = 2
        self.cost = 15
        self.fighting_class = 3
