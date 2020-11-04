class MovementEngine:
    def __init__(self, board, game):
        self.board = board
        self.game = game

    def complete_all_movements(self, board, game_state):
        for player in self.game.players:
                player.check_colonization(self.board)
                for movement_round in range(0, 3):  # 3 rounds of movements
                    for ship in player.ships:
                        for _ in ship.movement_tech:
                            ship.x, ship.y = player.strategy.decide_ship_movement(ship.__dict__, game_state, movement_round)