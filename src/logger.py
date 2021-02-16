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

    def log_turn(self, game_state, log_colonies=False, log_ship_yards=True, log_technology=True):
        # print(os.getcwd())  # what directory ur in (for debugging)
        turn_string = '\nTurn: ' + str(game_state['turn']) + '\n'
        self.active_file.write(turn_string)
        for player_index, player in enumerate(game_state['players']):
            player_string = player['name'] + '\nIs Alive: ' + \
                str(player['Is Alive']) + '\n'
            self.active_file.write(player_string)
            home_base_string = 'Home Base : Position: [' + \
                str(player['home_base']['coords'][0]) + ',' + \
                str(player['home_base']['coords'][1]) + '] \n'
            self.active_file.write(home_base_string)
            for ship_attributes in player['units']:
                ship_string = str(ship_attributes['type']) + ' : Ship ID : ' + str(ship_attributes['id']) + ' : Position : [' + \
                    str(ship_attributes['coords'][0]) + ',' + str(ship_attributes['coords'][1]) + '] \n'
                self.active_file.write(ship_string)

            if log_colonies:
                for colony_attributes in player['colonies'].values():
                    colony_string = str(colony_attributes['type']) + ' : Colony ID : '+ str(colony_attributes['id']) + ' : Position : [' + \
                    str(colony_attributes['coords'][0]) + ',' + str(colony_attributes['coords'][1]) + '] \n'
                    self.active_file.write(colony_string)

            if log_ship_yards:
                for ship_yard_attributes in player['ship_yards']:
                    ship_yard_string = str(ship_yard_attributes['type']) + ' : Ship Yard ID: ' + str(ship_yard_attributes['id']) + ' : Position : [' + \
                    str(ship_yard_attributes['coords'][0]) + ',' + str(ship_yard_attributes['coords'][1]) + '] \n'
                    self.active_file.write(ship_yard_string)
            
            if log_technology:
                for tech, level in player['technology'].items():
                    tech_string = str(tech) + ' : Level : ' + str(level) + '\n'
                    self.active_file.write(tech_string)

            self.active_file.write('\n')

    def log_movement(self, old_game_state, game_state, log_colonies=False, log_ship_yards=True):
        for player_index, player in enumerate(game_state['players']):
            player_string = '\n' + str(player['name']) + '\nIs Alive: ' + \
                str(player['Is Alive']) + '\n'

            self.active_file.write(player_string)

            home_base_string = 'Home Base : Position : [' + \
                str(player['home_base']['coords'][0]) + ',' + \
                str(player['home_base']['coords'][1]) + '] \n' 

            self.active_file.write(home_base_string)

            old_player = old_game_state['players'][player_index]

            for ship_index, ship_attributes in enumerate(player['units']):
                ship_string = str(ship_attributes['type']) + ' : Ship ID : ' + str(ship_attributes['id']) + ' : Position Changes : [' + \
                    str(old_player['units'][ship_index]['coords'][0]) + ',' + str(old_player['units'][ship_index]['coords'][1]) + '] -> [' + \
                    str(ship_attributes['coords'][0]) + ',' + str(ship_attributes['coords'][1]) + '] \n'
                self.active_file.write(ship_string)

            if log_colonies:
                for colony_index, colony_attributes in enumerate(player['colonies']):
                    colony_string = str(colony_attributes['type']) + ' : Colony ID : '+ str(colony_attributes['id']) + ' : Position Changes : [' + \
                    str(old_player['colonies'][colony_index]['coords'][0]) + ',' + str(old_player['colonies'][colony_index]['coords'][1]) + '] -> [' + \
                    str(colony_attributes['coords'][0]) + ',' + str(colony_attributes['coords'][1]) + '] \n'
                    self.active_file.write(colony_string)

            if log_ship_yards:
                for ship_yard_index, ship_yard_attributes in enumerate(player['ship_yards']):
                    ship_yard_string = str(ship_yard_attributes['type']) + ' : Ship Yard ID: ' + str(ship_yard_attributes['id']) + ' : Position Changes : [' + \
                    str(old_player['ship_yards'][ship_yard_index]['coords'][0]) + ',' + str(old_player['ship_yards'][ship_yard_index]['coords'][1]) + '] -> [' + \
                    str(ship_yard_attributes['coords'][0]) + ',' + str(ship_yard_attributes['coords'][1]) + '] \n'
                    self.active_file.write(ship_yard_string)
            self.active_file.write('\n')

    def log_combat(self, player_1, ship_1, player_2, ship_2, did_ship_1_hit):
        if did_ship_1_hit:
            combat_string = str(player_1['name']) + "'s " + str(ship_1['type']) + ' ' + str(ship_1['id']) + ' shot ' + str(player_2['name']) + "'s " + str(ship_2['type']) + ' ' + str(ship_2['id'])
            if ship_2['hits_left'] < 1:
                combat_string += '\n' + str(player_2['name']) + "'s " + str(ship_2['type']) + ' ' +  str(ship_2['id']) + ' was destroyed at coords [' + str(ship_2['coords'][0]) + ',' + str(ship_2['coords'][1]) + ']'
        else:
            combat_string = str(player_1['name']) + "'s " + str(ship_1['type']) + ' ' +  str(ship_1['id']) + ' missed their shot on ' + str(player_2['name']) + "'s " + str(ship_2['type']) + ' ' +  str(ship_2['id'])
        
        self.active_file.write(combat_string)

        self.active_file.write('\n')

    def log_economic(self, game_state, player_index, player_maintenance, player_income, purchases):
        player_string = '\n' + str(game_state['players'][player_index]['name']) + \
            ' : Maintenance : ' + str(player_maintenance) + \
            ' : Income : ' + str(player_income) + \
            '\nTechnology Purchases : \n'

        for tech in purchases['technology']:
            player_string += '    ' + str(tech) + '\n'

        player_string += 'Unit Purchases : \n'

        for unit in purchases['units']:
            player_string += '    ' + str(unit['type']) + '\n'

        self.active_file.write(player_string)

        #self.active_file.write('\n')

    def end_logs(self, player_who_won):
        if player_who_won != None:
            self.active_file.write(str(player_who_won['name']) + ' Won!!!')
        else:
            self.active_file.write('The game ended in a draw... :pepehands:')
        self.active_file.close()

    def read_info(self):  # To print stuff out
        self.active_file = open(self.active_file_name, 'r')  # get file
        return self.active_file.read()  # return contents of file

    def compare_test_and_example(self):
        active_file = self.active_file.readlines()
        correct_file = self.correct_file.readlines()
        for active, correct in zip(active_file, correct_file):
            if active != correct:
                return False
        return True
