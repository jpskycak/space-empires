class MovementEngine:
    def __init__(self, board, game):
        self.board = board
        self.game = game

    def complete_all_movements(self, board, game_state):
        for player in self.game.players:
                player.check_colonization(self.board)
                for movement_round in range(0, 3):  # 3 rounds of movements
                    self.game.generate_state(phase='Movement', movement_round=movement_round)
                    for ship in player.ships:
                        for _ in ship.movement_tech:
                            x, y = player.strategy.decide_ship_movement(ship.__dict__, game_state)
                            ship.x += x
                            ship.y += y

    def generate_movement_state(self, movement_round):
        return {'round': movement_round}