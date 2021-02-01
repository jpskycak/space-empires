class MovementEngine:
    def __init__(self, board, game):
        self.board = board
        self.game = game

    def complete_all_movements(self, board, hidden_game_state, number_of_rounds):
        for player in self.game.players:
            player.check_colonization(self.board, hidden_game_state)
            for movement_round in range(0, number_of_rounds):  # 3 rounds of movements
                for ship_index, ship in enumerate(player.ships):
                    for _ in range(0, self.get_movement_tech(ship.technology['movement'])[movement_round]):
                        x, y = player.strategy.decide_ship_movement(ship_index, hidden_game_state)
                        if 0 <= ship.x + x and 0 <= ship.y + y and ship.x + x <= hidden_game_state['board_size'][0]-1 and ship.y + y <= hidden_game_state['board_size'][0]-1 and x+y <= self.get_movement_tech(ship.technology['movement'])[movement_round]:
                            ship.x += x
                            ship.y += y
                        else:
                            print('\n',player.strategy.__name__, player.player_index, 'Tried to cheat and move to', (ship.x + x, ship.y + y), 'so the program was aborted.')
                            exit()
                        self.game.generate_full_state(phase='Movement', movement_round=movement_round)

    def generate_movement_state(self, movement_round):
        return {'round': movement_round}

    def get_movement_tech(self, ship_movement_level):
        if ship_movement_level == 1:
            return [1, 1, 1]
        elif ship_movement_level == 2:
            return [1, 1, 2]
        elif ship_movement_level == 3:
            return [1, 2, 2]
        elif ship_movement_level == 4:
            return [2, 2, 2]
        elif ship_movement_level == 5:
            return [2, 2, 3]
        elif ship_movement_level == 5:
            return [2, 3, 3]
