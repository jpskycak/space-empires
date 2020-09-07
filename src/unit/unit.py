import random

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class Unit:
    def __init__(self, player, ID, position, grid_size, can_move=True, attack_tech=0, defense_tech=0, movement_tech=0, ship_yard_tech=0):
        self.ID = ID
        self.player = player
        self.x = position[0]
        self.y = position[1]
        self.grid_size = grid_size
        self.status = 'Playing'  # for ship yard and other stuffs
        self.can_move = can_move
        self.attack_tech = 0
        self.defense_tech = 0
        self.movement_tech = [1, 1, 1]
        self.ship_yard_tech = 0
        self.centre = [(self.grid_size) // 2, (self.grid_size) // 2]

    def move_to_centre(self):
        if self.can_move:
            for i in range(0, len(self.movement_tech)):
                for _ in range(0, self.movement_tech[i]):
                    if self.x != self.centre[0]:
                        if self.x < self.centre[0]:
                            print(self.player.player_number, self.ID, 'move right')
                            self.x += 1
                        elif self.x > self.centre[0]:
                            print(self.player.player_number, self.ID, 'move left')
                            self.x -= 1
                    elif self.y != self.centre[1]:
                        if self.y < self.centre[1]:
                            print(self.player.player_number, self.ID, 'move down')
                            self.y += 1
                        elif self.y > self.centre[1]:
                            print(self.player.player_number, self.ID, 'move up')
                            self.y -= 1

    def dumb_move(self):
        # 0 is up   1 is right    2 is down   3 is left
        if self.can_move:
            for i in range(0, len(self.movement_tech)):

                for _ in range(0, self.movement_tech[i]):

                    if self.x < self.grid_size - 1:
                        self.x += 1
                    elif self.x >= self.grid_size - 1:
                        self.x -= 1

    def random_move(self):
        # 0 is up   1 is right    2 is down   3 is left
        direction = random.randint(0, 3)
        if self.can_move:
            for i in range(0, len(self.movement_tech)):
                for _ in range(0, self.movement_tech[i]):
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

    def move_to_nearest_planet(self, misc_dict, planet_class):
        for position, space_object in misc_dict.items():
            if isinstance(space_object, planet_class):
                if space_object.is_claimed != True:
                    space_object.is_claimed = True
                    for i in range(0, len(self.movement_tech)):
                        for _ in range(0, self.movement_tech[i]):
                            if self.x != position[0]:
                                if self.x < position[0]:
                                    print(self.player.player_number, self.ID, 'move right')
                                    self.x += 1
                                elif self.x > position[0]:
                                    print(self.player.player_number, self.ID, 'move left')
                                    self.x -= 1
                            elif self.y != position[1]:
                                if self.y < position[1]:
                                    print(self.player.player_number, self.ID, 'move down')
                                    self.y += 1
                                elif self.y > position[1]:
                                    print(self.player.player_number, self.ID, 'move up')
                                    self.y -= 1
