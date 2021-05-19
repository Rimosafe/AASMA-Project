from Board import Board
from Satellite import Satellite
from copy import deepcopy


class Player:

    def __init__(self, name):
        self.name = name
        self.board = Board()
        self.enemy_board = [['U' for _ in range(10)] for _ in range(10)]
        self.sunken_ships = 0
        self.lost_shot = 0
        self.hit_shot = 0
        self.consecutive_hits = 0
        self.consecutive_list = []
        self.consecutive = False
        self.satellite = Satellite()

    def print_stats(self):
        print(end="\n")
        print(self.name)
        print("Hit shots: ", self.hit_shot)
        print("Miss shots: ", self.lost_shot)

        if len(self.consecutive_list) > 0:
            print("Max consecutive hits: ", max(self.consecutive_list))
        else:
            print("Max consecutive hits: ", 1)

    '''def shot(self, opponent_board, x, y):

        # Access the satellite to check if the shot hit
        if not self.check_satellite(opponent_board, x, y):

            self.enemy_board[x][y] = 'Miss'
            return False

        # Hit the ship
        opponent_board.matrix[x][y]['ship'].hit(x, y)
        self.enemy_board[x][y] = 'Hit'
        self.hit_shot += 1
        print("Hit")
        self.consecutive = True

        if self.consecutive:
            self.consecutive_hits += 1

        # Ship sunk
        if opponent_board.matrix[x][y]['ship'].is_sunk():
            self.sunken_ships += 1

        return True'''