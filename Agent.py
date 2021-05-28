from Player import Player
import random
import numpy as np
import math

np.set_printoptions(precision=2, suppress=True)


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def get_agent(self):
        if self.name == 'Random':
            return RandomAgent()
        elif self.name == 'ReactiveRandom':
            return ReactiveAgent()
        elif self.name == 'ReactiveParity':
            return ReactiveParityAgent()
        elif self.name == 'Learning':
            return LearningAgent()

class RandomAgent(Agent):

    def __init__(self):
        super().__init__('Random')

    def policy(self):

        x = random.randint(0, 9)
        y = random.randint(0, 9)

        # Check if already shooted that position
        while self.satellite.check_visible(x, y):
            x = random.randint(0, 9)
            y = random.randint(0, 9)

        return x, y


class ReactiveAgent(Agent):

    def __init__(self):
        super().__init__('ReactiveRandom')
        self.last_shooted = []
        self.to_explore = []
        self.first_shot = True

    def policy(self):
        # First shot
        if self.first_shot:
            self.first_shot = False
            x, y = self.seek()
            self.last_shooted.append(x)
            self.last_shooted.append(y)
            return x, y

        # Coordinates shooted on the previous turn
        x = self.last_shooted[0]
        y = self.last_shooted[1]

        # If the shot hit
        if self.satellite.check_shot(x, y):
            # Add neighbour cells to explore
            self.add_to_explore(x, y)

            # If there is coordinates to explore
            if len(self.to_explore) > 0:
                x, y = self.explore()

            else:
                x, y = self.seek()

        else:
            # If there is coordinates to explore
            if len(self.to_explore) > 0:
                x, y = self.explore()

            else:
                x, y = self.seek()

        self.last_shooted.clear()
        self.last_shooted.append(x)
        self.last_shooted.append(y)
        return x, y

    def add_to_explore(self, x, y):
        if y - 1 >= 0 and not self.satellite.check_visible(x, y - 1) and (x, y - 1) not in self.to_explore:
            self.to_explore.append((x, y - 1))

        if x - 1 >= 0 and not self.satellite.check_visible(x - 1, y) and (x - 1, y) not in self.to_explore:
            self.to_explore.append((x - 1, y))

        if y + 1 <= 9 and not self.satellite.check_visible(x, y + 1) and (x, y + 1) not in self.to_explore:
            self.to_explore.append((x, y + 1))

        if x + 1 <= 9 and not self.satellite.check_visible(x + 1, y) and (x + 1, y) not in self.to_explore:
            self.to_explore.append((x + 1, y))

    def explore(self):
        coordinates = self.to_explore[0]
        self.to_explore.pop(0)
        return coordinates[0], coordinates[1]

    def seek(self):
        x = random.randint(0, 9)
        y = random.randint(0, 9)

        # Check if already shooted that position
        while self.satellite.check_visible(x, y):
            x = random.randint(0, 9)
            y = random.randint(0, 9)

        return x, y


class ReactiveParityAgent(Agent):

    def __init__(self):
        super().__init__('ReactiveParity')
        self.first_shot = True
        self.last_shooted = []
        self.to_explore = []
        self.odd_cells = [(0, 0), (0, 2), (0, 4), (0, 6), (0, 8),
                          (1, 1), (1, 3), (1, 5), (1, 7), (1, 9),
                          (2, 0), (2, 2), (2, 4), (2, 6), (2, 8),
                          (3, 1), (3, 3), (3, 5), (3, 7), (3, 9),
                          (4, 0), (4, 2), (4, 4), (4, 6), (4, 8),
                          (5, 1), (5, 3), (5, 5), (5, 7), (5, 9),
                          (6, 0), (6, 2), (6, 4), (6, 6), (6, 8),
                          (7, 1), (7, 3), (7, 5), (7, 7), (7, 9),
                          (8, 0), (8, 2), (8, 4), (8, 6), (8, 8),
                          (9, 1), (9, 3), (9, 5), (9, 7), (9, 9)]

    def policy(self):
        # First shot
        if self.first_shot:
            self.first_shot = False
            x, y = self.seek()
            self.last_shooted.append(x)
            self.last_shooted.append(y)
            return x, y

        # Coordinates shooted on the previous turn
        x = self.last_shooted[0]
        y = self.last_shooted[1]

        # If the shot hit
        if self.satellite.check_shot(x, y):
            # Add neighbour cells to explore
            self.add_to_explore(x, y)

            # If there is coordinates to explore
            if len(self.to_explore) > 0:
                x, y = self.explore()

            else:
                x, y = self.seek()

        else:
            # If there is coordinates to explore
            if len(self.to_explore) > 0:
                x, y = self.explore()

            else:
                x, y = self.seek()

        self.last_shooted.clear()
        self.last_shooted.append(x)
        self.last_shooted.append(y)
        return x, y

    def add_to_explore(self, x, y):
        # Cell to the left
        if y - 1 >= 0 and not self.satellite.check_visible(x, y - 1) and (x, y - 1) not in self.to_explore:
            self.to_explore.append((x, y - 1))

        # Cell above
        if x - 1 >= 0 and not self.satellite.check_visible(x - 1, y) and (x - 1, y) not in self.to_explore:
            self.to_explore.append((x - 1, y))

        # Cell to the right
        if y + 1 <= 9 and not self.satellite.check_visible(x, y + 1) and (x, y + 1) not in self.to_explore:
            self.to_explore.append((x, y + 1))

        # Cell below
        if x + 1 <= 9 and not self.satellite.check_visible(x + 1, y) and (x + 1, y) not in self.to_explore:
            self.to_explore.append((x + 1, y))

    def explore(self):
        coordinates = self.to_explore[0]
        self.to_explore.pop(0)
        return coordinates[0], coordinates[1]

    def seek(self):
        coordinates = random.choice(self.odd_cells)

        # Check if already shooted that position
        while self.satellite.check_visible(coordinates[0], coordinates[1]):
            coordinates = random.choice(self.odd_cells)

        self.odd_cells.remove(coordinates)
        return coordinates[0], coordinates[1]


class LearningAgent(Player):
    directions = ['l', 'u', 'r', 'd']

    def __init__(self):
        super().__init__('Learning')
        self.steps = 50
        self.current_state = 0
        self.num_actions = len(self.directions)
        self.num_states = 10 * 10  # size
        self.alpha = 0.3
        self.gamma = 0.8
        self.listCoordinates = []
        self.direction = None

    def policy(self):

        Q = self.Qinit

        state = 0

        for t in range(self.steps):

            # Choose action
            action = self.egreedy(Q, state, 0.05)
            self.getDirection(action)

            # choose next state
            while True:
                next_state = np.random.choice(self.num_states, 1)

                x = math.trunc(next_state[0] * 0.1)
                y = next_state[0] % 10

                if (not self.satellite.check_visible(x, y)):
                    reward = self.rewards(x, y)
                    break  # found coordinates not used
                else:
                    reward = -1

            # update Q
            Q[state, action] = Q[state, action] + self.alpha * (
                        reward + self.gamma * np.max(Q[next_state, :]) - Q[state, action])

            self.Qinit = Q

            state = next_state

        x = math.trunc(state[0] * 0.1)
        y = state[0] % 10

        return x, y

    def egreedy(self, Q, state, eps):
        p = np.random.random()

        if p < eps:
            action = np.random.choice(self.num_actions)
        else:
            action = np.argmax(Q[state, :])

        return action

    def getDirection(self, action):

        if (action == 0):
            self.direction = 'l'
        if (action == 1):
            self.direction = 'u'
        if (action == 2):
            self.direction = 'r'
        if (action == 3):
            self.direction = 'd'

    def rewards(self, x, y):
        reward = 0
        if self.direction == 'l':
            if (y - 1 >= 0) and (self.satellite.check_shot(x, y - 1) and (not self.satellite.check_sunk(x, y - 1))):
                reward = 1
            else:
                return 0

        if self.direction == 'u':
            if (x - 1 >= 0) and (self.satellite.check_shot(x - 1, y) and (not self.satellite.check_sunk(x - 1, y))):
                reward = 1
            else:
                return 0

        if self.direction == 'r':
            if (y + 1 <= 9) and (self.satellite.check_shot(x, y + 1) and (not self.satellite.check_sunk(x, y + 1))):
                reward = 1
            else:
                return 0

        if self.direction == 'd':
            if (x + 1 <= 9) and (self.satellite.check_shot(x + 1, y) and (not self.satellite.check_sunk(x + 1, y))):
                reward = 1
            else:
                return 0

        if (self.satellite.check_shot(x, y)):
            return reward + 1  # hit
        else:
            return 0  # miss

    def random_seek(self):
        print("well")
        x = random.randint(0, 9)
        y = random.randint(0, 9)

        # Check if already shooted that position
        while self.satellite.check_visible(x, y):
            x = random.randint(0, 9)
            y = random.randint(0, 9)

        return x, y


class ReactivePatternAgent(Player):

    def __init__(self):
        super().__init__('ReactivePattern')
        self.last_shooted = []
        self.to_explore = []
        self.odd_cells = [(0, 0), (0, 2), (0, 4), (0, 6), (0, 8),
                          (1, 1), (1, 3), (1, 5), (1, 7), (1, 9),
                          (2, 0), (2, 2), (2, 4), (2, 6), (2, 8),
                          (3, 1), (3, 3), (3, 5), (3, 7), (3, 9),
                          (4, 0), (4, 2), (4, 4), (4, 6), (4, 8),
                          (5, 1), (5, 3), (5, 5), (5, 7), (5, 9),
                          (6, 0), (6, 2), (6, 4), (6, 6), (6, 8),
                          (7, 1), (7, 3), (7, 5), (7, 7), (7, 9),
                          (8, 0), (8, 2), (8, 4), (8, 6), (8, 8),
                          (9, 1), (9, 3), (9, 5), (9, 7), (9, 9)]
        self.first_shot = True

    def policy(self):

        if self.first_shot:
            self.first_shot = False
            x, y = self.seek()
            self.last_shooted.append(x)
            self.last_shooted.append(y)
            return x, y

        x = self.last_shooted[0]
        y = self.last_shooted[1]

        while self.satellite.check_visible(x, y):

            if self.satellite.check_shot(x, y):
                self.add_to_explore(x, y)

                if len(self.to_explore) > 0:
                    x, y = self.explore()

                else:
                    x, y = self.seek()

            else:
                if len(self.to_explore) > 0:
                    x, y = self.explore()

                else:
                    x, y = self.seek()

        self.last_shooted.clear()
        self.last_shooted.append(x)
        self.last_shooted.append(y)
        return x, y

    def add_to_explore(self, x, y):
        if y - 1 >= 0 and not self.satellite.check_visible(x, y - 1) and (x, y - 1) not in self.to_explore:
            self.to_explore.append((x, y - 1))

        if x - 1 >= 0 and not self.satellite.check_visible(x - 1, y) and (x - 1, y) not in self.to_explore:
            self.to_explore.append((x - 1, y))

        if y + 1 <= 9 and not self.satellite.check_visible(x, y + 1) and (x, y + 1) not in self.to_explore:
            self.to_explore.append((x, y + 1))

        if x + 1 <= 9 and not self.satellite.check_visible(x + 1, y) and (x + 1, y) not in self.to_explore:
            self.to_explore.append((x + 1, y))

    def explore(self):
        coordinates = self.to_explore[0]
        self.to_explore.pop(0)
        return coordinates[0], coordinates[1]

    def seek(self):
        coordinates = random.choice(self.odd_cells)

        # Check if already shooted that position
        while self.satellite.check_visible(coordinates[0], coordinates[1]):
            coordinates = random.choice(self.odd_cells)

        self.odd_cells.remove(coordinates)
        return coordinates[0], coordinates[1]


class LearningAgent(Agent):
    directions = ['l', 'u', 'r', 'd']

    def __init__(self):
        super().__init__('Learning')
        self.steps = 50
        self.current_state = 0
        self.num_actions = len(self.directions)
        self.num_states = 10 * 10  # size
        self.alpha = 0.3
        self.gamma = 0.8
        self.listCoordinates = []
        self.direction = None
        self.Qinit = np.zeros((10 * 10, 4))

    def policy(self):

        Q = self.Qinit

        state = 0

        for t in range(self.steps):

            # Choose action
            action = self.egreedy(Q, state, 0.05)
            self.getDirection(action)

            # choose next state
            while True:
                next_state = np.random.choice(self.num_states, 1)

                x = math.trunc(next_state[0] * 0.1)
                y = next_state[0] % 10

                if (not self.satellite.check_visible(x, y)):
                    reward = self.rewards(x, y)
                    break  # found coordinates not used
                else:
                    reward = -1

            # update Q
            Q[state, action] = Q[state, action] + self.alpha * (
                        reward + self.gamma * np.max(Q[next_state, :]) - Q[state, action])

            self.Qinit = Q

            state = next_state

        x = math.trunc(state[0] * 0.1)
        y = state[0] % 10

        return x, y

    def egreedy(self, Q, state, eps):
        p = np.random.random()

        if p < eps:
            action = np.random.choice(self.num_actions)
        else:
            action = np.argmax(Q[state, :])

        return action

    def getDirection(self, action):

        if (action == 0):
            self.direction = 'l'
        if (action == 1):
            self.direction = 'u'
        if (action == 2):
            self.direction = 'r'
        if (action == 3):
            self.direction = 'd'

    def rewards(self, x, y):
        reward = 0
        if self.direction == 'l':
            if (y - 1 >= 0) and (self.satellite.check_shot(x, y - 1) and (not self.satellite.check_sunk(x, y - 1))):
                reward = 1
            else:
                return 0

        if self.direction == 'u':
            if (x - 1 >= 0) and (self.satellite.check_shot(x - 1, y) and (not self.satellite.check_sunk(x - 1, y))):
                reward = 1
            else:
                return 0

        if self.direction == 'r':
            if (y + 1 <= 9) and (self.satellite.check_shot(x, y + 1) and (not self.satellite.check_sunk(x, y + 1))):
                reward = 1
            else:
                return 0

        if self.direction == 'd':
            if (x + 1 <= 9) and (self.satellite.check_shot(x + 1, y) and (not self.satellite.check_sunk(x + 1, y))):
                reward = 1
            else:
                return 0

        if (self.satellite.check_shot(x, y)):
            return reward + 1  # hit
        else:
            return 0  # miss

    def random_seek(self):
        print("well")
        x = random.randint(0, 9)
        y = random.randint(0, 9)

        # Check if already shooted that position
        while self.satellite.check_visible(x, y):
            x = random.randint(0, 9)
            y = random.randint(0, 9)

        return x, y