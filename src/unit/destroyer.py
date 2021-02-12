from unit.unit import Unit


class Destroyer(Unit):
    def __init__(self, player, position, board_size, ID):
        super().__init__(player, position, board_size, ID)
        self.type = 'Destroyer'
        self.label = 'DD'
        self.player = player
        self.hull_size = 2
        self.attack = 4
        self.defense = 0
        self.hits_left = 1
        self.cost = 9
        self.fighting_class = 1
        self.technology = {tech: level for tech, level in player.technology.items()} #{'attack': 0, 'defense': 0, 'movement': 1, 'tactics': 0}
