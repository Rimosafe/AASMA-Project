class Ship:

    def __init__(self, name, size):

        self.name = name
        self.locations = []
        self.hits = 0
        self.size = size
        self.direction = ''

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


"""s = Ship('Destroyer', 5)

print(s.print_location())

s.hit(2, 4)

print(s.print_location())

s.hit(1, 4)

print(s.print_location())

s.hit(3, 4)

s.hit(4, 4)

print(s.print_location())

print(s.is_sunk())

print(s)"""
