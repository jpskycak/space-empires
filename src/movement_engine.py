class MovementEngine:
    def __init__(self, board, game):
        self.board = board
        self.game = game

    def complete_all_movements(self, number_of_rounds):
        old_game_state = {key: value for key,value in self.game.game_state.items()}
        for movement_round in range(0, number_of_rounds):  # 3 rounds of movements
            for player in self.game.players:
                self.game.generate_state(phase='Movement', current_player=player)
                hidden_game_state = self.game.game_state
                for ship_index, ship in enumerate(player.ships):
                    for _ in range(0, self.get_movement_tech(ship.technology['movement'])[movement_round]):
                        x, y = player.strategy.decide_ship_movement(ship_index, hidden_game_state)
                        if 0 <= ship.x + x and 0 <= ship.y + y and ship.x + x <= hidden_game_state['board_size'][0] - 1 and ship.y + y <= hidden_game_state['board_size'][0] - 1 and x+y <= self.get_movement_tech(ship.technology['movement'])[movement_round]:
                            if not self.cant_move_due_to_combat(ship) and not player.check_colonization(ship, self.board, hidden_game_state):
                                #if self.game.print_state_obsolete:
                                ship.x += x
                                ship.y += y
                        else:
                            print('\n' + player.strategy.__name__, 'Tried to cheat and move to',
                                  (ship.x + x, ship.y + y), 'so the program was aborted.')
                            exit()
                        player.check_colonization(ship, self.board, hidden_game_state)
        self.game.generate_state(phase='Movement')
        if self.game.can_log: self.game.log.log_movement(old_game_state, self.game.game_state)

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

    def cant_move_due_to_combat(self, check_ship):
        for player in self.game.players:
            for ship in player.ships:
                if ship.ID != check_ship.ID and ship.player.player_index != check_ship.player.player_index:
                    if (ship.x, ship.y) == (check_ship.x, check_ship.y):
                        return True
        return False
