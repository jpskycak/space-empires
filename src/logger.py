import os
import difflib
import sys
import filecmp
sys.path.append('src')


class Logger:
    def __init__(self, board = None):  # the passing of Board gives me players and their ships
        self.board = board

    def get_next_active_file(self, path, name=None):
        #print(os.getcwd())  # what directory ur in (for debugging)
        new_log_number = sum([len(files) for r, d, files in os.walk(path)]) + 1
        if name == None:
            self.active_file_name = path + '/log_' + \
                str(new_log_number) + '.txt'
        else:
            self.active_file_name = path + name + '.txt'
        self.active_file = open(self.active_file_name, 'w+')

    def get_current_active_file(self, path, name=None, ):
        #print(os.getcwd())  # what directory ur in (for debugging)
        new_log_number = sum([len(files) for r, d, files in os.walk(path)])
        if name == None:
            self.active_file_name = path + '/log_' + str(new_log_number) + '.txt'
        else:
            self.active_file_name = path + name + '.txt'
        self.active_file = open(self.active_file_name, 'r')

    def get_correct_example_file(self, correct_example_file_path):
        self.correct_example_file_path = correct_example_file_path
        self.correct_file = open(self.correct_example_file_path, 'r')

    def log_info(self, turn, log_colonies=False, log_ship_yards=False):
        #print(os.getcwd())  # what directory ur in (for debugging)
        turn_string = 'Turn: ' + str(turn) + '\n'
        self.active_file.write(turn_string)
        for player in self.board.players:
            player_string = 'Player: ' + str(player.player_number) + '\nStatus: ' + str(player.status) + '\n'
            self.active_file.write(player_string)
            for ship in player.ships:
                ship_string = str(ship.name) + ': Position: [' + str(ship.x) + ',' + str(ship.y) + '] \n'
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

    def read_info(self): # To print stuff out
        self.active_file = open(self.active_file_name, 'r')  #get file
        return self.active_file.read() # return contents of file

    def compare_test_and_example(self): # I couldn't find anyway to do this other than using filecmp
        active_file = self.active_file.readlines()
        correct_file = self.correct_file.readlines()
        for active, correct in zip(active_file, correct_file):
            if active != correct:
                return False
        return True
        #return filecmp.cmp(self.active_file_name, self.correct_example_file_path, shallow=False)
