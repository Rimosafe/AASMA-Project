from Player import Player
from Agent import *

class Game:
    COLS = 10
    ROWS = 10

    AGENT_TYPES = ['Random', 'Reactive', 'Learning', 'ReactivePattern']

    def __init__(self):
        self.players = []
        self.one_player = True

    def set_human_players(self):
        n_players = int(input("You will play with 1 or 2 players? "))

        if 0 > n_players > 2:
            raise ValueError("1 or 2 players.")

        elif n_players == 1:
            name = input("Name of player: ")
            player1 = Player(name)
            player2 = Player('Bot')
            self.players.append(player1)
            self.players.append(player2)
            self.place_ships_auto(1)
            print('Fleet build with success.')

        else:
            name = input("Name of player 1: ")

            self.one_player = False

            player1 = Player(name)

            self.players.append(player1)

            place = int(input("Do you want to build the fleet your self or automatic?\n0 - Place own\n1 - Automatic\n"))

            if place == 0:
                self.place_ships_manually(0)
                print('Fleet build with success.')
            else:
                self.place_ships_auto(0)
                print('Fleet build with success.')

            name = input("Name of player 2: ")

            player2 = Player(name)

            self.players.append(player2)

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

        player1 = get_type_agent(agent1)
        self.players.append(player1)

        # If agent 2 was given
        if agent2:
            # If agent 2 type don't exist
            if agent2 in self.AGENT_TYPES:
                self.one_player = False
                player2 = get_type_agent(agent2)
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
                print(player.name, "wins!")
                return True

    def play(self, agent1=None, agent2=None):
        if agent1 is None:
            self.set_human_players()

        self.set_agent_players(agent1, agent2)

        if self.one_player:
            self.agent_alone()
        else:
            self.agent_one_vs_one()

    def agent_alone(self):

        consecutive_hits = 0

        x, y = self.players[0].policy()

        while True:
            #print(self.print_player_game(0))
            #print("Numero navios acertados")
            #print(self.players[0].sunken_ships)
            
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

        self.players[0].print_stats()

    def agent_one_vs_one(self):

        self.players[0].name = 'Agent 1'
        self.players[1].name = 'Agent 2'

        consecutive_hits = 0

        x1, y1 = self.players[0].policy()
        x2, y2 = self.players[1].policy()

        while not self.game_over():
            #print("Numero navios acertados")
            #print(self.players[0].sunken_ships)

            if self.players[0].satellite.check_shot(x1, y1):
                self.players[1].board.matrix[x1][y1]['ship'].hit(x1, y1)
                self.players[0].enemy_board[x1][y1] = 'H'
                self.players[0].hit_shot += 1
                consecutive_hits += 1

                # Ship sunk
                if self.players[0].satellite.check_sunk(x1, y1):
                    self.players[0].sunken_ships += 1

            else:
                if consecutive_hits > 1:
                    self.players[0].consecutive_list.append(consecutive_hits)

                consecutive_hits = 0
                self.players[0].lost_shot += 1
                self.players[0].enemy_board[x1][y1] = 'M'

            if self.players[1].satellite.check_shot(x2, y2):
                self.players[0].board.matrix[x2][y2]['ship'].hit(x2, y2)
                self.players[1].enemy_board[x2][y2] = 'H'
                self.players[1].hit_shot += 1
                consecutive_hits += 1

                # Ship sunk
                if self.players[1].satellite.check_sunk(x2, y2):
                    print("navio afundou")
                    self.players[1].sunken_ships += 1

            else:
                if consecutive_hits > 1:
                    self.players[1].consecutive_list.append(consecutive_hits)

                consecutive_hits = 0
                self.players[1].lost_shot += 1
                self.players[1].enemy_board[x2][y2] = 'M'

            self.players[0].satellite.map.matrix[x1][y1]['visible'] = True
            self.players[1].satellite.map.matrix[x2][y2]['visible'] = True

            x1, y1 = self.players[0].policy()
            x2, y2 = self.players[1].policy()

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