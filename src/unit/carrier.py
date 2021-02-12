from unit.unit import Unit


class Carrier(Unit):
    def __init__(self, player, position, board_size, ID):
        super().__init__(player, position, board_size, ID)
        self.type = 'Carrier'
        self.label = 'CA'
        self.player = player
        self.attack = 1
        self.defense = 3
        self.hits_left = 1
        self.cost = 12
        self.fighting_class = 1
        self.stored_ships = stored_ships
        self.technology = {tech: level for tech, level in player.technology.items()} #{'attack': 0, 'defense': 0, 'movement': 1, 'tactics': 0}
