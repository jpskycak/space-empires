from unit.unit import Unit


class Cruiser(Unit):
    def __init__(self, player, position, board_size, ID):
        super().__init__(player, position, board_size, ID)
        self.type = 'Cruiser'
        self.label = 'CV'
        self.player = player
        self.hull_size = 3
        self.attack = 4
        self.defense = 1
        self.hits_left = 2
        self.cost = 12
        self.fighting_class = 2
        self.technology = {tech: level for tech, level in player.technology.items()} #{'attack': 0, 'defense': 0, 'movement': 1, 'tactics': 0}
