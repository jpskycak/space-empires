import os
import difflib
import filecmp


class Logger:
    def get_next_active_file(self, path, name=None):
        # print(os.getcwd())  # what directory ur in (for debugging)
        new_log_number = sum([len(files) for r, d, files in os.walk(path)]) + 1
        if name == None:
            self.active_file_name = path + '/log_' + \
                str(new_log_number) + '.txt'
        else:
            self.active_file_name = path + name + '.txt'
        self.active_file = open(self.active_file_name, 'w+')

    def get_current_active_file(self, path, name=None, ):
        # print(os.getcwd())  # what directory ur in (for debugging)
        new_log_number = sum([len(files) for r, d, files in os.walk(path)])
        if name == None:
            self.active_file_name = path + '/log_' + \
                str(new_log_number) + '.txt'
        else:
            self.active_file_name = path + name + '.txt'
        self.active_file = open(self.active_file_name, 'r')

    def get_correct_example_file(self, correct_example_file_path):
        self.correct_example_file_path = correct_example_file_path
        self.correct_file = open(self.correct_example_file_path, 'r')

    def log_info(self, game_state, log_colonies=False, log_ship_yards=False):
        # print(os.getcwd())  # what directory ur in (for debugging)
        turn_string = 'Turn: ' + str(game_state['turn']) + '\n'
        self.active_file.write(turn_string)
        for player_index, player in game_state['players'].items():
            player_string = 'Player: ' + \
                str(player_index + 1) + '\nStatus: ' + \
                str(player['status']) + '\n'
            self.active_file.write(player_string)
            for ship_attributes in player['units']:
                ship_string = str(ship_attributes['type']) + ': Position: [' + str(
                    ship_attributes['coords'][0]) + ',' + str(ship_attributes['coords'][1]) + '] \n'
                self.active_file.write(ship_string)
            if log_colonies:
                for colony_attributes in player['colonies'].values():
                    colony_string = str(colony_attributes['name']) + ' Colony ID:', str(
                        colony_attributes['ID']) + ': [' + str(colony_attributes['coords'][0]) + str(colony_attributes['coords'][1]) + '] \n'
                    self.active_file.write(colony_string)
            if log_ship_yards:
                for ship_yard_attributes in player['ship_yards'].values():
                    ship_yard_string = 'Ship Yard ID:' + str(ship_yard_attributes['ID']) + ': [' + str(
                        ship_yard_attributes['coords'][0]) + str(ship_yard_attributes['coords'][1]) + '] \n'
                    self.active_file.write(ship_yard_string)
            self.active_file.write('\n')

    def read_info(self):  # To print stuff out
        self.active_file = open(self.active_file_name, 'r')  # get file
        return self.active_file.read()  # return contents of file

    # I couldn't find anyway to do this other than using filecmp
    def compare_test_and_example(self):
        active_file = self.active_file.readlines()
        correct_file = self.correct_file.readlines()
        for active, correct in zip(active_file, correct_file):
            if active != correct:
                return False
        return True
