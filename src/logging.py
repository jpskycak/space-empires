import os
import sys
sys.path.append('src')

class Logging:
    def __init__(self, board): #the passing of Board gives me players and their ships
        self.board = board

    def log_info(self, log_colonies=False, log_ship_yards=False):
        #print(os.getcwd()) what directory ur in (for debugging)
        new_log_number = sum([len(files) for r, d, files in os.walk("space-empires/src/logs")]) #get number of files in the logs folder
        file_name = 'space-empires/src/logs/log_' + \
            str(new_log_number) + '.txt'
        f = open(file_name, 'a+') #create a new file
        for player in self.board.players:
            f.write('Player:', player.player_number, '| Type:',
                  player.type, '| Status:', player.status, file=f)
            for ship in player.ships:
                f.write(ship.name, ':', 'Ship ID:',
                      ship.ID, ':', [ship.x, ship.y], file=f)

            if log_colonies:
                for colony in player.colonies:
                    f.write(colony.name, ':', 'Colony ID:',
                        colony.ID, ':', [colony.x, colony.y], file=f)

            if log_ship_yards:
                for ship_yard in player.ship_yards:
                    f.write('Ship Yard ID:', ship_yard.ID,
                        ':', [ship_yard.x, ship_yard.y], file=f)
