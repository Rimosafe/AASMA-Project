from Board import Board
from Satellite import Satellite
from copy import deepcopy
import numpy as np


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
        self.satellite = Satellite()
        self.Qinit = np.ones((10*10, 4))

    def print_stats(self):
        print(end="\n")
        print(self.name)
        print("Hit shots: ", self.hit_shot)
        print("Miss shots: ", self.lost_shot)

        if len(self.consecutive_list) > 0:
            print("Max consecutive hits: ", max(self.consecutive_list))
        else:
            print("Max consecutive hits: ", 1)

 