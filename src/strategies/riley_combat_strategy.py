class CombatStrategy:
    def __init__(self, player_index):
        self.player_index = player_index
        self.__name__ = 'CombatStrategy'

    def will_colonize(self, colony_ship_loc, game_state):
        return False

    def decide_ship_movement(self, ship_index, game_state):
        ship = game_state['players'][self.player_index]['units'][ship_index]
        if ship['location'][0] > 2:
            return (-1, 0)
        elif ship['location'][0] < 2:
            return (1, 0)
        elif ship['location'][1] > 2:
            return (0, -1)
        elif ship['location'][1] < 2:
            return (0, 1)
        else:
            return (0, 0)

    def decide_purchases(self, game_state):
        units = []
        tech = []
        ds = ['Destroyer', 9]
        sc = ['Scout', 6]
        ship_choice = ds
        creds = game_state['players'][self.player_index-1]['creds']
        ship_size_tech = game_state['players'][self.player_index]['technology']['ship_size'][0]
        while creds >= ship_choice[1]:
            if ship_size_tech < 2:
                ship_size_price = ((ship_size_tech + 1)*5)
                if creds > ship_size_price:
                    ship_size_tech += 1
                    tech.append('ship_size')
                    creds -= ship_size_price
            else:
                if creds >= ship_choice[1]:
                    units.append(ship_choice[0])
                    creds -= ship_choice[1]

                    if ship_choice == ds:
                        ship_choice = sc
                    elif ship_choice == sc:
                        ship_choice = ds
        return {'units': units, 'technology': []}

    def decide_removals(self, game_state):
        i = 0
        while True:
            if game_state['players'][self.player_index]['units'][i]['location'] != None:
                return game_state['players'][self.player_index]['units'][i]['unit_num']
            else:
                i += 1

    def decide_which_unit_to_attack(self, combat_state, location, attacking_ship_index):
        for entry in combat_state[location]:
            if entry['player'] != combat_state[location][attacking_ship_index]['player']:
                return combat_state[location].index(entry)

    def decide_which_units_to_screen(self, combat_state):
        return []
