from Player import Player
import random


class RandomAgent(Player):

    def __init__(self):
        super().__init__('Random')

    def policy(self, opponent_board):

        while self.sunken_ships != 5:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            self.shot(opponent_board, x, y)

        print(self.lost_shot)
        print(self.hit_shot)