import random
import sys
sys.path.append('src')

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class Unit:
    def __init__(self, player, position, board_size, ID):
        self.player = player
        self.ID = ID
        self.x = position[0]
        self.y = position[1]
        self.board_size = board_size
        self.is_alive = True  # for ship yard and other stuffs
        self.technology = {'attack': 0, 'defense': 0, 'movement': 1, 'tactics': 0}
        #self.attack_tech = 0
        #self.defense_tech = 0
        #self.movement_tech = [1, 1, 1]
        self.ship_yard_tech = 0
        self.center = [self.board_size[0] // 2, self.board_size[1] // 2]
'''
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
                if self.x < self.board_size:
                    self.x += 1
                elif self.x > self.board_size:
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
                    if self.y < self.board_size - 1:
                        self.y += 1
                    elif self.y >= self.board_size - 1:
                        self.y -= 1
                elif direction == RIGHT:
                    if self.x < self.board_size - 1:
                        self.x += 1
                    elif self.x >= self.board_size - 1:
                        self.x -= 1
                elif direction == LEFT:
                    if self.x > 0:
                        self.x -= 1
                    elif self.x <= 0:
                        self.x += 1

    def move_to_nearest_planet(self, move_round, board, planet_class):
        for position, space_object in board.misc_dict.items():
            if isinstance(space_object, planet_class):
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
'''