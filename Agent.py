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
        self.orientation = False
        self.first_shot = True

    def policy(self):

        if self.first_shot:
            return self.random_seek()

        x = self.last_shooted[0]
        y = self.last_shooted[1]

        self.last_shooted.clear()

        # First shot hit
        if self.satellite.check_shot(x, y) and self.direction is None:
            self.direction = 'l'

            self.initial_shot.append(x)
            self.initial_shot.append(y)

            x, y = self.predict_next_shot(x, y)

        # Last shot hit and its not the first shot
        elif self.satellite.check_shot(x, y) and self.direction is not None:

            # Set orientation of ship. Horizontal or Vertical.
            if not self.orientation:
                self.define_orientation()

            # If still there is directions to explore
            if self.predict_next_shot() is not False:
                x, y = self.predict_next_shot(x, y)

            # Ship found. Proceed with random seek
            else:
                self.directions = ['l', 'u', 'r', 'd']
                self.initial_shot.clear()
                x, y = self.random_seek()

        # If last shot didnt hit and we are exploring a zone
        elif not self.satellite.check_shot(x, y) and self.direction is not None:

            # Check if there is another direction to explore
            if self.next_direction():

                # There is but it goes outside the board. Ship found.
                if self.predict_next_shot() is not False:
                    x, y = self.predict_next_shot(x, y)

                # Proceed with random seek.
                else:
                    self.directions = ['l', 'u', 'r', 'd']
                    self.initial_shot.clear()
                    x, y = self.random_seek()

            # Ship found. Proceed with random seek.
            else:
                self.directions = ['l', 'u', 'r', 'd']
                self.initial_shot.clear()
                x, y = self.random_seek()

        # If last shot didnt hit and we were not exploring a zone
        elif not self.satellite.check_shot(x, y) and self.direction is None:
            x, y = self.random_seek()

        self.last_shooted.append(x)
        self.last_shooted.append(y)
        return x, y

    def predict_next_shot(self, x, y):
        if self.direction == 'l':
            if x - 1 >= 0:
                return x - 1, y
            elif self.orientation:
                return self.initial_shot[0] + 1, self.initial_shot[1]
            else:
                self.next_direction()

        if self.direction == 'u':
            if y - 1 >= 0:
                return x, y - 1
            elif self.orientation:
                return self.initial_shot[0], self.initial_shot[1] + 1
            else:
                self.next_direction()

        if self.direction == 'r':
            if x + 1 <= 9:
                return x + 1, y
            else:
                self.next_direction()
                return False

        if self.direction == 'd':
            if y + 1 <= 9:
                return x, y + 1
            else:
                self.next_direction()
                return False

    def next_direction(self):
        directions = self.directions

        if directions.index(self.direction) + 1 > len(self.directions) - 1:
            return False

        self.direction = directions[directions.index(self.direction) + 1]
        return True

    def define_orientation(self):
        if self.direction == 'l':
            self.directions.remove('u')
            self.directions.remove('d')

        elif self.direction == 'u':
            self.directions.remove('l')
            self.directions.remove('r')

        self.orientation = True

    def random_seek(self):
        x = random.randint(0, 9)
        y = random.randint(0, 9)

        # Check if already shooted that position
        while self.satellite.check_visible(x, y):
            x = random.randint(0, 9)
            y = random.randint(0, 9)

        return x, y

class LearningAgent(Player):

    def __init__(self):
        super().__init__('Learning')

    def policy(self):
        return