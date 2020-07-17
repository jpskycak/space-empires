import os
import sys
sys.path.append('src')


class Logging:
    def __init__(self, board):  # the passing of Board gives me players and their ships
        self.board = board
        self.active_file = self.get_next_active_file()

    def get_next_active_file(self):
        # get number of files in the logs folder
        new_log_number = sum([len(files) for r, d, files in os.walk("space-empires/src/logs")])
        file_name = 'space-empires/src/logs/log_' + str(new_log_number) + '.txt'
        return open(file_name, 'a+')

    def log_info(self, log_colonies=False, log_ship_yards=False):
        # print(os.getcwd()) what directory ur in (for debugging)
        for player in self.board.players:
            player_string = 'Player:' + \
                str(player.player_number) + '| Type:' + \
                    str(player.type) + '| Status:' + str(player.status)
            self.active_file.write(player_string)
            for ship in player.ships:
                ship_string = str(ship.name) + ':' + 'Ship ID:' + \
                                  str(ship.ID) + \
                                      ': [' + str(ship.x) + ',' + str(ship.y) + ']'
                self.active_file.write(ship_string)

            if log_colonies:
                for colony in player.colonies:
                    colony_string = str(colony.name) + ':', 'Colony ID:', str(
                        colony.ID) + ': [' + str(colony.x) + str(colony.y) + ']'
                    self.active_file.write(colony_string)

            if log_ship_yards:
                for ship_yard in player.ship_yards:
                    ship_yard_string = 'Ship Yard ID:' + \
                        str(ship_yard.ID) + \
                            ': [' + str(colony.x) + str(colony.y) + ']'
                    self.active_file.write(ship_yard_string)
