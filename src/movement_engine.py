class MovementEngine:
    def __init__(self, board, game):
        self.board = board
        self.game = game

    def complete_all_movements(self, board, game_state):
        for player in self.game.players:
                player.check_colonization(self.board, game_state)
                for movement_round in range(0, 3):  # 3 rounds of movements
                    for ship_index, ship in enumerate(player.ships):
                        for _ in range(0,ship.technology['movement'][movement_round] + 1):
                            x, y = player.strategy.decide_ship_movement(ship_index, game_state)
                            ship.x += x
                            ship.y += y
                            self.game.generate_state(phase='Movement', movement_round=movement_round)

    def generate_movement_state(self, movement_round):
        return {'movement_round': movement_round}