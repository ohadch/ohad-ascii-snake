import os
import random
import select
import sys
import threading
import time

from pynput.keyboard import Listener

from src.enums import Direction
from src.settings import MOVES, KEY_COMMANDS, OPPOSITE_COMMANDS
from src.utils import row_to_view, getch


class Game:

    def __init__(self, size):
        self.size = size
        self.zone = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.add_borders()
        self.next_move: Direction = Direction.DOWN
        self.snake = [[self.size//2, self.size//2 - 1], [self.size//2, self.size//2]]
        self.play = True
        self.result = ""
        self.score = "Score: {}".format(len(self.snake) - 2)
        self.food_coordinates = ""
        self.rounds = 0
        self.timeout = 0.3 / (len(self.snake) - 1.0)
        self.food = {
            'y': 0,
            'x': 0,
        }

    def add_borders(self):
        self.zone.append([-1 for x in range(self.size + 2)])
        self.zone.insert(0, [-1 for x in range(self.size + 2)])

        for r in self.zone:
            if r[0] == 0:
                r.insert(0, -1)
                r.append(-1)

    def next_spot(self):
        next_spot_y = self.snake[-1][0] + MOVES[self.next_move][0]
        next_spot_x = self.snake[-1][1] + MOVES[self.next_move][1]
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
        a = random.randint(1, self.size)
        b = random.randint(1, self.size)

        if self.check_spot((a, b)) == 'free':
            self.zone[a][b] = 2
            self.food['y'] = a
            self.food['x'] = b
        else:
            return self.generate_food()

    def show(self):
        os.system('clear')
        for r in self.zone:
            print(row_to_view(r))

    def exec_round(self):
        self.rounds += 1
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

        def show(key):
            key = str(key).replace('"', "").replace("'", "").lower()
            if key in KEY_COMMANDS:
                if KEY_COMMANDS[key] != OPPOSITE_COMMANDS.get(self.next_move, None):
                    self.next_move = KEY_COMMANDS[key]
                else:
                    self.next_move = OPPOSITE_COMMANDS[KEY_COMMANDS[key]]

        # Collect all event until released
        with Listener(on_press=show) as listener:
            # listener.join()
            threading.Thread(target=listener.join).start()

            while self.play:
                self.timeout = 0.3 / (len(self.snake) - 1.0)
                start_time = time.time()
                while True:
                    # Check for keypress
                    if time.time() - start_time > self.timeout:
                        break

                self.exec_round()
                self.score = "Score: {}".format(len(self.snake) - 2)
                print(self.score)
        print(self.result)
