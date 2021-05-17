class Satellite:

    def __init__(self):
        self.boards = [None, None]

    def check_shot(self, player, x, y):
        return self.boards[player].matrix[x][y]['ship'] is not None

    def check_visible(self, player, x, y):
        return self.boards[player].matrix[x][y]['visible']

    def check_sunk(self, player, x, y):
        return self.boards[player].matrix[x][y]['ship'].is_sunk()