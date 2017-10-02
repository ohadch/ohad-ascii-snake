from snake import *
from multiprocessing import Process
import SendKeys
import json


# --------------------------------------


possible_commands = list('wasd')
key_to_hex = {
    'w': 0x57,
    'a': 0x41,
    's': 0x53,
    'd': 0x44,
}


# --------------------------------------


def game_dict():
    f = open('log.txt', 'r').read()
    return json.loads(f)


# --------------------------------------


class Session:

    def __init__(self):
        self.game = Game(10)
        self.fitness = 0
        self.moves = []
        self.distances = []

    def play(self):
        game_process = Process(target=self.game.loop)
        game_process.start()
        first = True
        while True:
            if first:
                first = False
                continue
            elif not game_dict()['play']:
                break
            self.send_command()
        game_process.terminate()

    def send_command(self):
        curr_key = random.choice(possible_commands)
        self.moves.append(curr_key)
        SendKeys.SendKeys(curr_key)

    def head_distance_from_food(self):
        head_y = game_dict()['snake'][-1][0]
        head_x = game_dict()['snake'][-1][1]


    # def evaluate(self):
    #     return game_dict()['score'] *