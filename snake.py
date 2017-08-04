import os
import msvcrt
import time
import random
from termcolor import colored

# ----------------- Required Data -----------------

spot_types = {
    -1: 'border',
    0: 'free',
    1: 'snake',
    2: 'food',
}

spot_view = {
    'border': colored('#', 'red'),
    'free': " ",
    'snake': colored("O", 'cyan'),
    'food': colored('&', 'yellow'),
}

moves = {
    'up': (-1, 0),
    'down': (1, 0),
    'right': (0, 1),
    'left': (0, -1),
}

key_commands = {
    'w': 'up',
    's': 'down',
    'a': 'left',
    'd': 'right',
}

opposite_commands = {
    'up': 'down',
    'down': 'up',
    'right': 'left',
    'left': 'right',
}


# ---------------- Custom Functions ---------------


def num_to_view(num):
    return spot_view[spot_types[num]]


def row_to_view(row):
    return ' '.join([num_to_view(n) for n in row])


# -------------------- Classes ------------------


class Game(object):

    def __init__(self, size):
        self.size = size
        self.zone = [[0 for x in xrange(self.size)] for y in xrange(self.size)]
        self.add_borders()
        self.next_move = 'down'
        self.snake = [[self.size//2, self.size//2 - 1], [self.size//2, self.size//2]]
        self.play = True
        self.result = ""
        self.score = "Score: {}".format(len(self.snake) - 2)
        self.food_coordinates = ""
        
    def add_borders(self):
        self.zone.append([-1 for x in xrange(self.size + 2)])
        self.zone.insert(0, [-1 for x in xrange(self.size + 2)])

        for r in self.zone:
            if r[0] == 0:
                r.insert(0, -1)
                r.append(-1)

    def next_spot(self):
        next_spot_y = self.snake[-1][0] + moves[self.next_move][0]
        next_spot_x = self.snake[-1][1] + moves[self.next_move][1]
        return [next_spot_y, next_spot_x]

    def check_spot(self, spot):
        spot_value = self.zone[spot[0]][spot[1]]
        if spot_value == 0:
            return 'free'
        elif spot_value == 2:
            return 'eat'
        if spot_value == -1 or spot_value == 1:
            return 'crash'

    def clear_spot(self, spot):
        self.zone[spot[0]][spot[1]] = 0

    def draw_spot(self, spot, num):
        self.zone[spot[0]][spot[1]] = num

    def snake_move(self, eat):
        for spot in self.snake:
            self.clear_spot(spot)
        if not eat:
            self.snake.pop(0)

        self.snake.append(self.next_spot())
        for spot in self.snake:
            self.draw_spot(spot, 1)

        if eat:
            self.generate_food()

    def generate_food(self):
        a = random.randint(2, self.size - 1)
        b = random.randint(2, self.size - 1)

        if self.check_spot((a, b)) == 'free':
            self.zone[a][b] = 2
            self.food_coordinates = "Y: {} X: {}".format(a, b)
        else:
            return self.generate_food()

    def show(self):
        os.system('cls')
        for r in self.zone:
            print row_to_view(r)

    def exec_round(self):
        if self.check_spot(self.next_spot()) == 'free':
            self.snake_move(False)
        elif self.check_spot(self.next_spot()) == 'eat':
            self.snake_move(True)
        elif self.check_spot(self.next_spot()) == 'crash':
            self.play = False
            self.result = "You lose!"
        self.show()

    def loop(self):
        self.show()
        self.generate_food()
        self.snake_move(False)
        while self.play:
            timeout = 0.3 / (len(self.snake) - 1.0)
            start_time = time.time()
            while True:
                if msvcrt.kbhit():
                    inp = msvcrt.getch()
                    if inp in key_commands:
                        if not key_commands[inp] == opposite_commands[self.next_move]:
                            self.next_move = key_commands[inp]
                        else:
                            self.next_move = opposite_commands[key_commands[inp]]
                    break
                elif time.time() - start_time > timeout:
                    break
            self.exec_round()
            self.score = "Score: {}".format(len(self.snake) - 2)
            print self.score
        print self.result
    

class Menu(object):

    def __init__(self, board_size):
        self.board_size  = board_size
        self.game = Game(self.board_size)

    def run(self):
        self.game.loop()
        self.ask_for_restart()

    def ask_for_restart(self):
        i = raw_input("Would you like to restart? Y/N: ")
        if i.upper() == 'Y':
            return self.restart()
        elif i.upper() == 'N':
            print 'Thank you for playing! Ohad Chaet'
            exit()
        else:
            print 'Answer must be either "Y" or "N".'
            return self.ask_for_restart()

    def restart(self):
        self.game = Game(self.board_size)
        self.run()


# ------------------ Main ------------------


menu = Menu(20)
menu.run()
