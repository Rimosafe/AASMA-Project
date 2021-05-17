from Player import Player
import random


def get_type_agent(agent):
    if agent == 'Random':
        return RandomAgent()
    elif agent == 'Reactive':
        return ReactiveAgent()
    elif agent == 'Learning':
        return LearningAgent()


class RandomAgent(Player):

    def __init__(self):
        super().__init__('Random')

    def policy(self, satellite, player):

        x = random.randint(0, 9)
        y = random.randint(0, 9)

        # Check if already shooted that position
        while satellite.check_visible(player, x, y):
            x = random.randint(0, 9)
            y = random.randint(0, 9)

        return x, y


class ReactiveAgent(Player):

    def __init__(self):
        super().__init__('Reactive')

    def policy(self):
        return


class LearningAgent(Player):

    def __init__(self):
        super().__init__('Learning')

    def policy(self):
        return