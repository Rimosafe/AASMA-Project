class Satellite:

    def __init__(self):
        self.map = None

    def check_shot(self, x, y):
        return self.map.matrix[x][y]['ship'] is not None

    def check_visible(self, x, y):
        return self.map.matrix[x][y]['visible']

    def check_sunk(self, x, y):
        return self.map.matrix[x][y]['ship'].is_sunk()