from Board import Board
from copy import deepcopy


class Player:

    def __init__(self, name):
        self.name = name
        self.board = Board()
        self.enemy_board = [['_' for _ in range(10)] for _ in range(10)]
        self.sunken_ships = 0
        self.lost_shot = 0
        self.hit_shot = 0
        self.consecutive_hits = 0
        self.consecutive_list = []
        self.consecutive = False

    def check_satellite(self, opponent_board, x, y):
        position = deepcopy(opponent_board.matrix[x][y])

        # Shot didn't hit
        if position['ship'] is None:
            return False

        return True

    def shot(self, opponent_board, x, y):

        # Check if already shooted that position
        if self.enemy_board[x][y] == 'x' or self.enemy_board[x][y] == 'o':
            return False

        # Access the satellite to check if the shot hit
        if not self.check_satellite(opponent_board, x, y):
            self.lost_shot += 1

            if self.consecutive_hits > 1:
                self.consecutive_list.append(self.consecutive_hits)

            self.consecutive = False
            self.enemy_board[x][y] = 'o'
            return False

        # Hit the ship
        opponent_board.matrix[x][y]['ship'].hit(x, y)
        self.enemy_board[x][y] = 'x'
        self.hit_shot += 1

        if self.consecutive:
            self.consecutive_hits += 1

        self.consecutive = True

        # Ship sunk
        if opponent_board.matrix[x][y]['ship'].is_sunk():
            self.sunken_ships += 1

        return True