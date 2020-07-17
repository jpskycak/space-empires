import os
import sys
sys.path.append('src')


class Logging:
    def __init__(self, board = None):  # the passing of Board gives me players and their ships
        self.board = board

    def get_current_active_file(self, path, name = None):
        new_log_number = sum([len(files) for r, d, files in os.walk(path)]) - 1
        if name == None:
            self.file_name = path + '/log_' + str(new_log_number) + '.txt'
        else:
            self.file_name = path + name + '.txt'
        self.active_file = open(self.file_name, 'w+')

    def get_next_active_file(self, path):
        # get number of files in the logs folder
        new_log_number = sum([len(files) for r, d, files in os.walk(path)])
        self.file_name = path + '/log_' + str(new_log_number) + '.txt'
        self.active_file = open(self.file_name, 'w+')

    def log_info(self, log_colonies=False, log_ship_yards=False):
        # print(os.getcwd()) what directory ur in (for debugging)
        for player in self.board.players:
            player_string = 'Player:' + str(player.player_number) + 'Status:' + str(player.status)
            self.active_file.write(player_string)
            for ship in player.ships:
                ship_string = str(ship.name) + ':' + 'Ship ID:' + str(ship.ID) + ': [' + str(ship.x) + ',' + str(ship.y) + ']'
                self.active_file.write(ship_string)

            if log_colonies:
                for colony in player.colonies:
                    colony_string = str(colony.name) + ':', 'Colony ID:', str(colony.ID) + ': [' + str(colony.x) + str(colony.y) + ']'
                    self.active_file.write(colony_string)

            if log_ship_yards:
                for ship_yard in player.ship_yards:
                    ship_yard_string = 'Ship Yard ID:' + str(ship_yard.ID) + ': [' + str(colony.x) + str(colony.y) + ']'
                    self.active_file.write(ship_yard_string)

    def read_info(self):
        self.active_file = open(self.file_name, 'r')  #get file
        self.contents = self.active_file.read()
        return self.active_file.read() # return contents of file
