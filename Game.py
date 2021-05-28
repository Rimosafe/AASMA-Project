from Player import Player
from Agent import *

class Game:
    COLS = 10
    ROWS = 10

    AGENT_TYPES = ['Random', 'ReactiveRandom', 'Learning', 'ReactiveParity']

    def __init__(self):
        self.players = []
        self.one_player = True

    def set_human_player(self):

        self.place_ships_auto(0)
        self.players.pop(1)

        name = ''
        while name == '':
            name = input("Name of player 1:\n")

        player1 = Player(name)

        self.players.append(player1)

        self.players[1].satellite.map = self.players[0].board

        place = int(input("Do you want to build the fleet your self or automatic?\n0 - Place own\n1 - Automatic\n"))

        if place == 0:
            self.place_ships_manually(1)
            print('Fleet build with success.')
        else:
            self.place_ships_auto(1)
            print('Fleet build with success.')

    def set_agent_players(self, agent1, agent2=None):
        player2 = None
        if agent1 not in self.AGENT_TYPES:
            print("Agent 1 invalid.")

        player1 = Agent(agent1).get_agent()
        self.players.append(player1)

        # If agent 2 was given
        if agent2:
            # If agent 2 type don't exist
            if agent2 in self.AGENT_TYPES:
                self.one_player = False
                player2 = Agent(agent2).get_agent()
                self.place_ships_auto(0)
                self.players.append(player2)
                self.players[1].satellite.map = self.players[0].board
            else:
                print('Agent 2 invalid.')
        else:
            player2 = Player('Bot')
            self.players.append(player2)

        self.place_ships_auto(1)
        
        self.players[0].satellite.map = self.players[1].board

    def place_ships_manually(self, player):
        self.players[player].board.build_fleet_manually()

    def place_ships_auto(self, player):
        self.players[player].board.build_fleet_random()

    def game_over(self):
        for player in self.players:
            if player.sunken_ships == 5:
                return True

    def play(self):
        mode = int(input("Which mode do you want to play?\n0 - Agent only\n1 - Agent vs Agent\n2 - Agent vs Human\n"))

        if mode == 0:
            agent = ''
            while agent not in self.AGENT_TYPES:
                agent = input("Chose one agent to play: Random, ReactiveRandom, ReactiveParity, Learning\n")
            self.set_agent_players(agent, None)
            self.agent_only()

        elif mode == 1:
            agent1 = ''
            agent2 = ''
            while agent1 not in self.AGENT_TYPES:
                agent1 = input("Chose the first agent: Random, ReactiveRandom, ReactiveParity, Learning\n")
            while agent2 not in self.AGENT_TYPES:
                agent2 = input("Chose an agent to play against the " + agent1 +
                               " agent: Random, ReactiveRandom, ReactiveParity, Learning\n")
            self.set_agent_players(agent1, agent2)
            self.agent_agent()

        elif mode == 2:
            agent = ''
            while agent not in self.AGENT_TYPES:
                agent = input("Chose one agent to play: Random, ReactiveRandom, ReactiveParity, Learning\n")
            self.set_agent_players(agent, None)
            self.set_human_player()
            self.human_agent()

        else:
            self.play()

    def agent_only(self):

        consecutive_hits = 0

        x, y = self.players[0].policy()

        while True:

            if self.players[0].satellite.check_shot(x, y):
                self.players[1].board.matrix[x][y]['ship'].hit(x, y)
                self.players[0].enemy_board[x][y] = 'X'
                self.players[0].hit_shot += 1
                consecutive_hits += 1

                # Ship sunk
                if self.players[0].satellite.check_sunk(x, y):
                    self.players[0].sunken_ships += 1

                if self.game_over():
                    break

            else:
                if consecutive_hits > 1:
                    self.players[0].consecutive_list.append(consecutive_hits)

                consecutive_hits = 0
                self.players[0].lost_shot += 1
                self.players[0].enemy_board[x][y] = 'O'

            self.players[0].satellite.map.matrix[x][y]['visible'] = True
            x, y = self.players[0].policy()

    def agent_agent(self):

        self.players[0].name = 'Agent 1'
        self.players[1].name = 'Agent 2'

        consecutive_hits1 = 0
        consecutive_hits2 = 0

        x1, y1 = self.players[0].policy()
        x2, y2 = self.players[1].policy()

        while not self.game_over():
            if self.players[0].satellite.check_shot(x1, y1):
                self.players[1].board.matrix[x1][y1]['ship'].hit(x1, y1)
                self.players[0].enemy_board[x1][y1] = 'X'
                self.players[0].hit_shot += 1
                consecutive_hits1 += 1

                # Ship sunk
                if self.players[0].satellite.check_sunk(x1, y1):
                    self.players[0].sunken_ships += 1

            else:
                if consecutive_hits1 > 1:
                    self.players[0].consecutive_list.append(consecutive_hits1)

                consecutive_hits1 = 0
                self.players[0].lost_shot += 1
                self.players[0].enemy_board[x1][y1] = 'O'

            if self.players[1].satellite.check_shot(x2, y2):
                self.players[0].board.matrix[x2][y2]['ship'].hit(x2, y2)
                self.players[1].enemy_board[x2][y2] = 'X'
                self.players[1].hit_shot += 1
                consecutive_hits2 += 1

                # Ship sunk
                if self.players[1].satellite.check_sunk(x2, y2):
                    self.players[1].sunken_ships += 1

            else:
                if consecutive_hits2 > 1:
                    self.players[1].consecutive_list.append(consecutive_hits2)

                consecutive_hits2 = 0
                self.players[1].lost_shot += 1
                self.players[1].enemy_board[x2][y2] = 'O'

            self.players[0].satellite.map.matrix[x1][y1]['visible'] = True
            self.players[1].satellite.map.matrix[x2][y2]['visible'] = True

            x1, y1 = self.players[0].policy()
            x2, y2 = self.players[1].policy()

        self.players[0].print_stats()
        self.players[1].print_stats()

        return 0

    def human_agent(self):

        self.players[0].name = 'Agent'

        consecutive_hits1 = 0
        consecutive_hits2 = 0

        x1, y1 = self.players[0].policy()
        sx2, sy2 = input(self.players[1].name + " is your turn! Insert coordinates of type: x y\n").split()
        x2, y2 = int(sx2), int(sy2)

        while x2 < 0 or x2 > 9 or y2 < 0 or y2 > 9:
            print("Coordinates must have values between 0 and 9, inclusive.\n")
            sx2, sy2 = input("Reinsert coordinates: \n").split()
            x2, y2 = int(sx2), int(sy2)

        while not self.game_over():
            if self.players[0].satellite.check_shot(x1, y1):
                self.players[1].board.matrix[x1][y1]['ship'].hit(x1, y1)
                self.players[0].enemy_board[x1][y1] = 'X'
                self.players[0].hit_shot += 1
                consecutive_hits1 += 1

                # Ship sunk
                if self.players[0].satellite.check_sunk(x1, y1):
                    self.players[0].sunken_ships += 1

            else:
                if consecutive_hits1 > 1:
                    self.players[0].consecutive_list.append(consecutive_hits1)

                consecutive_hits1 = 0
                self.players[0].lost_shot += 1
                self.players[0].enemy_board[x1][y1] = 'O'

            if self.players[1].satellite.check_shot(x2, y2):
                self.players[0].board.matrix[x2][y2]['ship'].hit(x2, y2)
                self.players[1].enemy_board[x2][y2] = 'X'
                self.players[1].hit_shot += 1
                consecutive_hits2 += 1

                # Ship sunk
                if self.players[1].satellite.check_sunk(x2, y2):
                    self.players[1].sunken_ships += 1

            else:
                if consecutive_hits2 > 1:
                    self.players[1].consecutive_list.append(consecutive_hits2)

                consecutive_hits2 = 0
                self.players[1].lost_shot += 1
                self.players[1].enemy_board[x2][y2] = 'O'

            self.players[0].satellite.map.matrix[x1][y1]['visible'] = True
            self.players[1].satellite.map.matrix[x2][y2]['visible'] = True

            x1, y1 = self.players[0].policy()
            sx2, sy2 = input(self.players[1].name + " is your turn! Insert coordinates of type: x y\n").split()
            x2, y2 = int(sx2), int(sy2)

            while x2 < 0 or x2 > 9 or y2 < 0 or y2 >9:
                print("Coordinates must have values between 0 and 9, inclusive.\n")
                sx2, sy2 = input("Reinsert coordinates: \n").split()
                x2, y2 = int(sx2), int(sy2)

        self.players[0].print_stats()
        self.players[1].print_stats()

        return 0


    def print_player_game(self, player):
        print(end="\n         ")
        print("My board:", end="                            ")
        print("Enemy board:")
        for r in range(self.ROWS):
            print("")
            for c in range(self.COLS):
                self.players[player].board.print_location(r, c)
            print(end="       ")
            for c in range(self.COLS):
                print(self.players[player].enemy_board[r][c], end="  ")
        print("\n")