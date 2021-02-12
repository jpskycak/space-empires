from unit.unit import Unit


class Battleship(Unit):
    def __init__(self, player, position, board_size, ID):
        super().__init__(player, position, board_size, ID)
        self.type = 'Battleship'
        self.label = 'BB'
        self.player = player
        self.hull_size = 5
        self.attack = 5
        self.defense = 2
        self.hits_left = 3
        self.cost = 20
        self.fighting_class = 4
        self.technology = {tech: level for tech, level in player.technology.items()} #{'attack': 0, 'defense': 0, 'movement': 1, 'tactics': 0}
