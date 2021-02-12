from unit.unit import Unit


class BattleCruiser(Unit):
    def __init__(self, player, position, board_size, ID):
        super().__init__(player, position, board_size, ID)
        self.type = 'Battle Cruiser'
        self.label = 'BC'
        self.player = player
        self.hull_size = 4
        self.attack = 5
        self.defense = 1
        self.hits_left = 2
        self.cost = 15
        self.fighting_class = 3
        self.technology = {tech: level for tech, level in player.technology.items()} #{'attack': 0, 'defense': 0, 'movement': 1, 'tactics': 0}
