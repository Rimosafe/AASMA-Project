import random
from Ship import Ship
from copy import deepcopy


class Board:

    SHIP_TYPES = [
        {'name': 'Carrier', 'size': 5},
        {'name': 'Battleship', 'size': 4},
        {'name': 'Cruiser', 'size': 3},
        {'name': 'Submarine', 'size': 3},
        {'name': 'Destroyer', 'size': 2},
    ]

    def __init__(self):

        self.rows = 10
        self.columns = 10
        self.default_loc = {'ship': None, 'shooted': False, 'visible': False}
        self.matrix = self.init_board()
        self.ships = []
        self.sunken_ships = 0

    def init_board(self):
        m = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.columns):
                default_loc = deepcopy(self.default_loc)
                m[r][c] = default_loc
        return m

    def add_ship_manually(self, name, x, y, direction):
        ship = None

        for s in self.SHIP_TYPES:
            if s['name'] == name:
                ship = Ship(**s)

        if not ship:
            print("Invalid ship name.")
            return

        for s in self.ships:
            if s.name == name:
                print("Already exists a " + name + " ship")
                return

        if not self.validate_ship_position(ship.size, direction, x, y):
            print("Invalid coordinate.")
            return

        ship.direction = direction
        init_position = y if direction == 'h' else x
        end_position = init_position + ship.size

        for loc in range(init_position, end_position):
            if direction == 'h':
                coordinates = (x, loc)
            else:
                coordinates = (loc, y)

            ship.add_location(*coordinates, False)
            self.matrix[coordinates[0]][coordinates[1]]['ship'] = ship

        self.ships.append(ship)

    def add_ship_random(self, name):
        for s in self.ships:
            if s.name == name:
                return False

        ship = None
        for s in self.SHIP_TYPES:
            if s['name'] == name:
                ship = Ship(**s)

        if not ship:
            raise ValueError("Invalid ship name.")

        direction = random.choice(['v', 'h'])
        ship.direction = direction
        x = random.randint(0, self.columns - ship.size)
        y = random.randint(0, self.rows - ship.size)

        if self.validate_ship_position(ship.size, direction, x, y) is False:
            return False

        init_position = y if direction == 'h' else x
        end_position = init_position + ship.size

        for loc in range(init_position, end_position):
            if direction == 'h':
                coordinates = (x, loc)
            else:
                coordinates = (loc, y)

            ship.add_location(*coordinates, False)
            self.matrix[coordinates[0]][coordinates[1]]['ship'] = ship

        self.ships.append(ship)

    def validate_ship_position(self, size, direction, x, y):
        init_position = y if direction == 'h' else x
        end_position = init_position + size
        board_limit = self.columns if direction == 'h' else self.rows

        if end_position > board_limit:
            print("Invalid coordinate. Ship out of board.")
            return False

        for loc in range(init_position, end_position):
            if direction == 'h':
                coordinates = (x, loc)
            else:
                coordinates = (loc, y)
            if not self.matrix[coordinates[0]][coordinates[1]] == deepcopy(self.default_loc):
                return False
        return True

    def build_fleet_random(self):
        for s in self.SHIP_TYPES:
            success = False
            while success is False:
                success = self.add_ship_random(s['name'])

    def build_fleet_manually(self):
        while len(self.ships) != 5:
            try:
                name, x, y, direction = input(" Enter ship of type: name x y direction ").split()
                self.add_ship_manually(name, int(x), int(y), direction)
            except ValueError:
                print('Missing values.')

    def remove_ship(self, ship):
        for position in ship.locations:
            self.matrix[position['x']][position['y']] = deepcopy(self.default_loc)

    def print_location(self, x, y):
        if self.matrix[x][y]['ship'] is not None:
            print(self.matrix[x][y]['ship'].name[0], end="  ")
        else:
            print('_', end="  ")

    def __str__(self):
        board = ''
        for r in range(self.rows):
            print("")
            for c in range(self.columns):
                self.print_location(r, c)
        return board
