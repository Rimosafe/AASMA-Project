class Ship:

    def __init__(self, name, coordinate1, coordinate2):

        self.name = name
        self.locations = []
        self.hits = 0

        if 0 <= coordinate1['x'] <= 10 and 0 <= coordinate1['y'] <= 10 and 0 <= coordinate2['x'] <= 10 and 0 <= \
                coordinate2['y'] <= 10:
            if coordinate1['x'] == coordinate2['x']:
                size = coordinate1['y'] - coordinate2['y']
            elif coordinate1['y'] == coordinate2['y']:
                size = coordinate1['x'] - coordinate2['x']
            else:
                raise ValueError("Ship must be placed horizontally or vertically.")

            if 2 <= abs(size) >= 5:
                raise ValueError("Size must have values between 2 and 5.")
        else:
            raise ValueError("Ship coordinates must have values between 0 and 10, inclusive.")

        self.size = size

        if coordinate1['x'] == coordinate2['x']:
            for i in range(abs(coordinate1['y']), abs(coordinate2['y']) + 1):
                self.locations.append({'x': coordinate1['x'], 'y': i, 'hit': False})
        elif coordinate1['y'] == coordinate2['y']:
            for i in range(abs(coordinate1['x']), abs(coordinate2['x']) + 1):
                self.locations.append({'x': i, 'y': coordinate1['y'], 'hit': False})

    def add_location(self, x, y, hit):
        if len(self.locations) > self.size:
            raise ValueError("The ship is not allowed to have more positions.")
        self.locations.append({'x': x, 'y': y, 'hit': hit})

    def hit(self, x, y):
        for loc in self.locations:
            if (x, y) == (loc['x'], loc['y']):
                loc['hit'] = True

    def is_sunk(self):
        return self.hits == self.size

    def print_location(self):
        ret = ''
        for loc in self.locations:
            if loc['hit']:
                ret += 'X - '
            else:
                ret += 'O - '
        return ret[:len(ret)-3]

    def __str__(self):
        locations = []
        for loc in self.locations:
            locations.append((loc['x'], loc['y']))
        return '<Ship: {} {}>'.format(self.name, locations)


s = Ship('Destroyer', {'x': 1, 'y': 4}, {'x': 4, 'y': 4})

print(s.print_location())

s.hit(2, 4)

print(s.print_location())

s.hit(1, 4)

print(s.print_location())

s.hit(3, 4)

s.hit(4, 4)

print(s.print_location())

print(s.is_sunk())

print(s)
