from unit.unit import Unit


class Scout(Unit):
    def __init__(self, player, position, board_size, ID):
        super().__init__(player, position, board_size, ID)
        self.type = 'Scout'
        self.label = 'SC'
        self.hull_size = 1
        self.attack = 3
        self.defense = 0
        self.hits_left = 1
        self.cost = 6
        self.fighting_class = 0
        self.technology = {tech: level for tech, level in player.technology.items()} #{'attack': 0, 'defense': 0, 'movement': 1, 'tactics': 0}
