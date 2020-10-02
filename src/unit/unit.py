from board import Planet
import random
import sys
sys.path.append('src')

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class Unit:
    def __init__(self, player, position, grid_size, can_move=True, attack_tech=0, defense_tech=0, movement_tech=0, ship_yard_tech=0):
        self.player = player
        self.ID = len(self.player.ships)
        self.x = position[0]
        self.y = position[1]
        self.grid_size = grid_size
        self.status = 'Playing'  # for ship yard and other stuffs
        self.can_move = can_move
        self.attack_tech = 0
        self.defense_tech = 0
        self.movement_tech = [1, 1, 1]
        self.ship_yard_tech = 0
        self.center = [(self.grid_size) // 2, (self.grid_size) // 2]

    def move_to_center(self, move_round):
        if self.can_move:
            for _ in range(0, self.movement_tech[move_round - 1]):
                if self.x != self.center[0]:
                    if self.x < self.center[0]:
                        self.x += 1
                    elif self.x > self.center[0]:
                        self.x -= 1
                elif self.y != self.center[1]:
                    if self.y < self.center[1]:
                        self.y += 1
                    elif self.y > self.center[1]:
                        self.y -= 1

    def dumb_move(self, move_round):
        # 0 is up   1 is right    2 is down   3 is left
        if self.can_move:
            for _ in range(0, self.movement_tech[move_round - 1]):
                if self.x < self.grid_size:
                    self.x += 1
                elif self.x > self.grid_size:
                    self.x -= 1

    def random_move(self, move_round):
        # 0 is up   1 is right    2 is down   3 is left
        direction = random.randint(0, 3)
        if self.can_move:
            for _ in range(0, self.movement_tech[move_round - 1]):
                if direction == UP:
                    if self.y > 0:
                        self.y -= 1
                    elif self.y <= 0:
                        self.y += 1
                elif direction == DOWN:
                    if self.y < self.grid_size - 1:
                        self.y += 1
                    elif self.y >= self.grid_size - 1:
                        self.y -= 1
                elif direction == RIGHT:
                    if self.x < self.grid_size - 1:
                        self.x += 1
                    elif self.x >= self.grid_size - 1:
                        self.x -= 1
                elif direction == LEFT:
                    if self.x > 0:
                        self.x -= 1
                    elif self.x <= 0:
                        self.x += 1

    def move_to_nearest_planet(self, move_round, board):
        for position, space_object in board.misc_dict.items():
            if isinstance(space_object, Planet):
                if space_object.is_claimed == False:
                    for _ in range(0, self.movement_tech[move_round - 1]):
                        if self.x != position[0]:
                            if self.x < position[0]:
                                self.x += 1
                            elif self.x > position[0]:
                                self.x -= 1
                        elif self.y != position[1]:
                            if self.y < position[1]:
                                self.y += 1
                            elif self.y > position[1]:
                                self.y -= 1
                    space_object.is_claimed = True

    def move_to_position(self, position, move_round):
        for _ in range(0, self.movement_tech[move_round - 1]):
            if self.x != position[0]:
                if self.x < position[0]:
                    self.x += 1
                elif self.x > position[0]:
                    self.x -= 1
            elif self.y != position[1]:
                if self.y < position[1]:
                    self.y += 1
                elif self.y > position[1]:
                    self.y -= 1
