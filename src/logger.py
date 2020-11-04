import os
import difflib
import sys
import filecmp
sys.path.append('src')


class Logger:
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

    def log_info(self, game_state, log_colonies=False, log_ship_yards=False):
        #print(os.getcwd())  # what directory ur in (for debugging)
        turn_string = 'Turn: ' + str(game_state['turn']) + '\n'
        self.active_file.write(turn_string)
        for player in game_state['players']:
            player_string = 'Player: ' + str(player['player_number']) + '\nStatus: ' + str(player['status']) + '\n'
            self.active_file.write(player_string)
            for _, ship_attributes in player['ships'].items():
                ship_string = str(ship_attributes['name']) + ': Position: [' + str(ship_attributes['x']) + ',' + str(ship_attributes['y']) + '] \n'
                self.active_file.write(ship_string)
            if log_colonies:
                for _, colony_attributes in player['colonies'].items():
                    colony_string = str(colony_attributes['name']) + ' Colony ID:', str(colony_attributes['ID']) + ': [' + str(colony_attributes['x']) + str(colony_attributes['y']) + '] \n'
                    self.active_file.write(colony_string)
            if log_ship_yards:
                for _, ship_yard_attributes in player['ship_yards']:
                    ship_yard_string = 'Ship Yard ID:' + str(ship_yard_attributes['ID']) + ': [' + str(ship_yard_attributes['x']) + str(ship_yard_attributes['y']) + '] \n'
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
