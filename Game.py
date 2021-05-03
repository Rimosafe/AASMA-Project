from Ship import Ship
from Board import Board


class Game:
    COLS = 10
    ROWS = 10

    def __init__(self, *players):

        self.players = {}
        self.player1 = None
        self.player2 = None
        self.n_players = self.assign_players(players)

    def assign_players(self, players):

        if len(players) > 2:
            raise ValueError("Max 2 players.")

        for name in players:
            self.players[name] = {
                'board': Board(),
                'enemy_board': [['_' for _ in range(self.COLS)] for _ in range(self.ROWS)],
                'ships_sunk': 0
            }
        return 1

    def place_ships_manually(self, player):
        n_ships = 0
        while n_ships != 5:
            name, x, y, direction = input(" Enter ship of type: name x y direction ").split()
            self.players[player]['board'].add_ship_manually(name, int(x), int(y), direction)
            n_ships += 1

    def place_ships_auto(self, player):
        self.players[player]['board'].build_fleet_random()

    def game_over(self):
        if self.players == 1:
            return self.player1['ships_sunk'] == 5
        else:
            return self.player1['ships_sunk'] == 5 or self.player2['ships_sunk']

    def print_player_game(self, player):
        print(end="\n         ")
        print("My board:", end="                            ")
        print("Enemy board:")
        for r in range(self.ROWS):
            print("")
            for c in range(self.COLS):
                self.players[player]['board'].print_location(r, c)
            print(end="       ")
            for c in range(self.COLS):
                print(self.players[player]['enemy_board'][r][c], end="  ")
        print("\n")

g = Game('R', 'L')
g.place_ships_auto('R')
g.place_ships_auto('L')
g.print_player_game('R')
g.print_player_game('L')
