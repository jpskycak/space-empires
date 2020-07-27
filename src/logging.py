import os
import sys
sys.path.append('src')


class Logger:
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
        print(os.getcwd())  # what directory ur in (for debugging)
        self.active_file = open(self.file_name, 'w+')

    def log_info(self, turn, log_colonies=False, log_ship_yards=False):
        print(os.getcwd())  # what directory ur in (for debugging)
        turn_string = 'Turn: ' + str(turn) + '\n'
        self.active_file.write(turn_string)
        for player in self.board.players:
            player_string = 'Player: ' + str(player.player_number) + '\nStatus: ' + str(player.status) + '\n'
            self.active_file.write(player_string)
            for ship in player.ships:
                ship_string = str(ship.name) + ' Ship ID: ' + str(ship.ID) + ' Position: [' + str(ship.x) + ',' + str(ship.y) + '] \n'
                self.active_file.write(ship_string)

            if log_colonies:
                for colony in player.colonies:
                    colony_string = str(colony.name) + ' Colony ID:', str(colony.ID) + ': [' + str(colony.x) + str(colony.y) + '] \n'
                    self.active_file.write(colony_string)

            if log_ship_yards:
                for ship_yard in player.ship_yards:
                    ship_yard_string = 'Ship Yard ID:' + str(ship_yard.ID) + ': [' + str(colony.x) + str(colony.y) + '] \n'
                    self.active_file.write(ship_yard_string)

            self.active_file.write('\n')

    def read_info(self):
        self.active_file = open(self.file_name, 'r')  #get file
        self.contents = self.active_file.read()
        return self.active_file.read() # return contents of file

    def get_correct_example(self, correct_example_file):
        self.correct_example = correct_example_file

    def compare_test_and_example(self):
        with self.active_file as text, self.correct_example.active_file as exc:
            exclusions = [line.rstrip('\n') for line in exc]
            for line in text:
                assert not any(exclusion in line for exclusion in exclusions), 'There is a difference in the current log, the line is \n {}'.format(line)
