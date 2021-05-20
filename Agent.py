from Player import Player
import random
import numpy as np
np.set_printoptions(precision = 2, suppress = True)


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

    def policy(self):

        x = random.randint(0, 9)
        y = random.randint(0, 9)

        # Check if already shooted that position
        while self.satellite.check_visible(x, y):
            x = random.randint(0, 9)
            y = random.randint(0, 9)

        return x, y


class ReactiveAgent(Player):

    directions = ['l', 'u', 'r', 'd']

    def __init__(self):
        super().__init__('Reactive')
        self.last_shooted = []
        self.initial_shot = []
        self.direction = None
        self.first_shot = True

    def policy(self):

        if self.first_shot:
            self.first_shot = False
            x, y = self.random_seek()
            self.last_shooted.append(x)
            self.last_shooted.append(y)
            return x, y

        x = self.last_shooted[0]
        y = self.last_shooted[1]

        while self.satellite.check_visible(x, y):

            # First shot hit
            if self.satellite.check_shot(x, y) and self.direction is None:
                self.direction = 'l'

                self.initial_shot.append(x)
                self.initial_shot.append(y)

                x, y = self.predict_next_shot(x, y)

            # Last shot hit and its not the first shot
            elif self.satellite.check_shot(x, y) and self.direction is not None:

                # If still there is directions to explore
                if self.predict_next_shot(x, y) is not False:
                    x, y = self.predict_next_shot(x, y)

                # Ship found. Proceed with random seek
                else:
                    self.direction = None
                    self.directions = ['l', 'u', 'r', 'd']
                    self.initial_shot.clear()
                    x, y = self.random_seek()

            # If last shot didnt hit and we are exploring a zone
            elif not self.satellite.check_shot(x, y) and self.direction is not None:

                # Check if there is another direction to explore
                if self.next_direction() is not False:

                    x, y = self.initial_shot[0], self.initial_shot[1]

                    if self.predict_next_shot(x, y) is not False:
                        x, y = self.predict_next_shot(x, y)

                    # Proceed with random seek.
                    else:
                        self.direction = None
                        self.directions = ['l', 'u', 'r', 'd']
                        self.initial_shot.clear()
                        x, y = self.random_seek()

                # Ship found. Proceed with random seek.
                else:
                    self.direction = None
                    self.directions = ['l', 'u', 'r', 'd']
                    self.initial_shot.clear()
                    x, y = self.random_seek()

            # If last shot didnt hit and we were not exploring a zone
            elif not self.satellite.check_shot(x, y) and self.direction is None:
                x, y = self.random_seek()

        self.last_shooted.clear()
        self.last_shooted.append(x)
        self.last_shooted.append(y)
        return x, y

    def predict_next_shot(self, x, y):
        if self.direction == 'l':
            if y - 1 >= 0:
                return x, y - 1
            else:
                x, y = self.next_direction()

        if self.direction == 'u':
            if x - 1 >= 0:
                return x - 1, y
            else:
                x, y = self.next_direction()

        if self.direction == 'r':
            if y + 1 <= 9:
                return x, y + 1
            else:
                x, y = self.next_direction()

        if self.direction == 'd':
            if x + 1 <= 9:
                return x + 1, y
            else:
                return False

    def next_direction(self):
        directions = self.directions

        if directions.index(self.direction) + 1 > len(self.directions) - 1:
            return False

        self.direction = directions[directions.index(self.direction) + 1]
        return self.initial_shot[0], self.initial_shot[1]

    def random_seek(self):
        x = random.randint(0, 9)
        y = random.randint(0, 9)

        # Check if already shooted that position
        while self.satellite.check_visible(x, y):
            x = random.randint(0, 9)
            y = random.randint(0, 9)

        return x, y


class LearningAgent(Player):
    directions = ['l', 'u', 'r', 'd']

    def __init__(self):
        super().__init__('Learning')
        self.steps = 10000
        self.current_state = 0
        self.num_actions = len(self.directions)
        self.num_states = 10 * 10 #size
        self.alpha = 0.3
        self.gamma = 0.9
        self.last_shooted = []
        self.initial_shot = []
        self.first_shot = True


    def policy(self):

        Q = np.ones((self.num_states, self.num_actions))

        state = 0

        x , y = self.random_seek()

        self.initial_shot[0] = x
        self.initial_shot[1] = y




        for t in range(self.steps):
            # Choose action
            action = self.egreedy(Q,state, 0.05)

            #choose next state
            next_state = np.random.choice(self.num_states, p = P[action][state, :])



            # obtain reward
            reward = self.rewards(self.getDirection(action))

            # update Q
            Q[state, action] += self.alpha * (reward + self.gamma * max(Q[next_state, :]) - Q[state, action])

            state = next_state

        print(Q)
        return

    def egreedy(self, Q, state,eps):
        p = np.random.random()

        if p < eps:
            action = np.random.choice(self.num_actions)
        else:
            action = np.argmax(Q[state,:])

        return action

    def getDirection(action):
              
       return{
           'l':0,
           'u':1,
           'r':2,
           'd':3
       }[action]


    def rewards(self, x, y):
        if(self.satellite.check_shot(x, y)):
            return 1  #hit
        elif(self.satellite.check_sunk(x, y)):
            return -1  #sunk
        else:
            return 0   #miss
            



    def random_seek(self):
        x = random.randint(0, 9)
        y = random.randint(0, 9)

        # Check if already shooted that position
        while self.satellite.check_visible(x, y):
            x = random.randint(0, 9)
            y = random.randint(0, 9)

        self.first_shot = False

        return x, y



    