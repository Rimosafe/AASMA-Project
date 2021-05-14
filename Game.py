from Player import Player


class Game:
    COLS = 10
    ROWS = 10

    def __init__(self):
        self.players = []

    def set_players_game(self):
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

    def place_ships_manually(self, player):
        self.players[player].board.build_fleet_manually()

    def place_ships_auto(self, player):
        self.players[player].board.build_fleet_random()

    def game_over(self):
        for player in self.players:
            if player.ships_sunk == 5:
                return True

    def play(self):
        self.set_players_game()

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