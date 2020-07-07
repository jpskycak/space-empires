import random

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class Unit:
    def __init__(self, ID, position, grid_size, can_move=True, attack_tech=0, defense_tech=0, speed_tech=0, ship_yard_tech=0):
        self.ID = ID
        self.x = position[0]
        self.y = position[1]
        self.grid_size = grid_size
        self.status = 'Playing'  # for ship yard and other stuffs
        self.can_move = can_move
        self.attack_tech = 0
        self.defense_tech = 0
        self.speed_tech = 0
        self.ship_yard_tech = 0

    def move(self):
        print('moving')
        # 0 is up   1 is right    2 is down   3 is left
        direction = random.randint(0, 3)
        if self.can_move:
            for _ in range(0, self.speed_tech):
                if direction == UP:
                    if self.y > 0:
                        self.y -= 1
                    elif self.y <= 0:
                        self.y += 1
                elif direction == DOWN:
                    if self.y < self.grid_size:
                        self.y += 1
                    elif self.y >= self.grid_size:
                        self.y -= 1
                elif direction == RIGHT:
                    if self.x < self.grid_size:
                        self.x += 1
                    elif self.x >= self.grid_size:
                        self.x -= 1
                elif direction == LEFT:
                    if self.x > 0:
                        self.x -= 1
                    elif self.x <= 0:
                        self.x += 1


class Scout(Unit):
    def __init__(self, ID, position, grid_size, can_move, attack_tech=0, defense_tech=0, speed_tech=0):
        super().__init__(ID, position, grid_size, can_move,
                         attack_tech, defense_tech, speed_tech)
        self.name = 'Scout'
        self.label = 'SC'
        self.hull_size = 1
        self.attack = 3
        self.defense = 0
        self.armor = 1
        self.cost = 6
        self.fighting_class = 0


class Destroyer(Unit):
    def __init__(self, ID, position, grid_size, can_move, attack_tech=0, defense_tech=0, speed_tech=0):
        super().__init__(ID, position, grid_size, can_move,
                         attack_tech, defense_tech, speed_tech)
        self.name = 'Destroyer'
        self.label = 'DD'
        self.hull_size = 2
        self.attack = 4
        self.defense = 0
        self.armor = 1
        self.cost = 9
        self.fighting_class = 1


class Cruiser(Unit):
    def __init__(self, ID, position, grid_size, can_move, attack_tech=0, defense_tech=0, speed_tech=0):
        super().__init__(ID, position, grid_size, can_move,
                         attack_tech, defense_tech, speed_tech)
        self.name = 'Cruiser'
        self.label = 'CV'
        self.hull_size = 3
        self.attack = 4
        self.defense = 1
        self.armor = 2
        self.cost = 12
        self.fighting_class = 2


class BattleCruiser(Unit):
    def __init__(self, ID, position, grid_size, can_move, attack_tech=0, defense_tech=0, speed_tech=0):
        super().__init__(ID, position, grid_size, can_move,
                         attack_tech, defense_tech, speed_tech)
        self.name = 'Battle Cruiser'
        self.label = 'BC'
        self.hull_size = 4
        self.attack = 5
        self.defense = 1
        self.armor = 2
        self.cost = 15
        self.fighting_class = 3


class Battleship(Unit):
    def __init__(self, ID, position, grid_size, can_move, attack_tech=0, defense_tech=0, speed_tech=0):
        super().__init__(ID, position, grid_size, can_move,
                         attack_tech, defense_tech, speed_tech)
        self.name = 'Battleship'
        self.label = 'BB'
        self.hull_size = 5
        self.attack = 5
        self.defense = 2
        self.armor = 3
        self.cost = 20
        self.fighting_class = 4


class Dreadnaught(Unit):
    def __init__(self, ID, position, grid_size, can_move, attack_tech=0, defense_tech=0, speed_tech=0):
        super().__init__(ID, position, grid_size, can_move,
                         attack_tech, defense_tech, speed_tech)
        self.name = 'Dreadnaught'
        self.label = 'DN'
        self.hull_size = 6
        self.attack = 6
        self.defense = 3
        self.armor = 3
        self.cost = 24
        self.fighting_class = 4


class Colony_Ship(Unit):
    def __init__(self, ID, position, grid_size, can_move, attack_tech=0, defense_tech=0, speed_tech=0):
        super().__init__(ID, position, grid_size, can_move,
                         attack_tech, defense_tech, speed_tech)
        self.name = 'Colony Ship'
        self.label = 'CO'
        self.hull_size = 1
        self.attack = 0
        self.defense = 0
        self.armor = 0
        self.cost = 8
        self.fighting_class = 0


class Colony(Unit):
    def __init__(self, ID, position, grid_size, can_move=False):
        super().__init__(ID, position, grid_size, can_move)
        self.name = 'Colony'
        self.income = 5
        self.label = 'Colony' + str(self.income)
        self.armor = 0


class Ship_Yard(Unit):
    def __init__(self, ID, position, grid_size, can_move=False, attack_tech=0, defense_tech=0, ship_yard_tech=0):
        super().__init__(ID, position, grid_size, can_move,
                         attack_tech, defense_tech, ship_yard_tech)
        self.name = 'Ship Yard'
        self.label = 'SY'
        self.hull_size = 1
        self.attack = 3
        self.defense = 0
        self.armor = 1
        self.cost = 6
        self.fighting_class = 0


class Miner(Unit):
    def __init__(self, ID, position, grid_size, can_move=True, speed_tech=0):
        super().__init__(ID, position, grid_size, can_move, speed_tech)
        self.name = 'Miner'
        self.label = 'Miner'
        self.hull_size = 1
        self.attack = 0
        self.defense = 0
        self.armor = 0
        self.cost = 5
        self.asteroid = []


class Base(Unit):
    def __init__(self, ID, position, grid_size, can_move=False, attack_tech=0, defense_tech=0):
        super().__init__(ID, position, grid_size, can_move, attack_tech, defense_tech)
        self.name = 'Base'
        self.label = 'Base'
        self.hull_size = 2
        self.attack = 7
        self.defense = 2
        self.armor = 3
        self.cost = 12
        self.fighting_class = 4


class Decoy(Unit):
    def __init__(self, ID, position, grid_size, can_move=True, speed_tech=0):
        super().__init__(ID, position, grid_size, can_move, speed_tech)
        self.name = 'Decoy'
        self.label = 'Decoy'
        self.hull_size = 1
        self.attack = 0
        self.defense = 0
        self.armor = 0
        self.cost = 5


class Carrier(Unit):
    def __init__(self, ID, position, grid_size, can_move, attack_tech=0, defense_tech=0, speed_tech=0, stored_ships=[]):
        super().__init__(ID, position, grid_size, can_move,
                         attack_tech, defense_tech, speed_tech)
        self.name = 'Carrier'
        self.label = 'CA'
        self.attack = 1
        self.defense = 3
        self.armor = 1
        self.cost = 12
        self.fighting_class = 1
        self.stored_ships = stored_ships
