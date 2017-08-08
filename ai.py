from snake import *
from multiprocessing import Process
from threading import Thread
import SendKeys


# --------------------------------------


possible_commands = list('wasd')
key_to_hex = {
    'w': 0x57,
    'a': 0x41,
    's': 0x53,
    'd': 0x44,
}

# --------------------------------------


class Session:

    def __init__(self, game):
        self.game = game
        self.fitness = 0
        self.moves = []

    def play(self):
        game_process = Process(target=self.game.loop)
        game_process.start()
        while self.game.play:
            time.sleep(self.game.timeout)
            self.send_command()
        game_process.terminate()

    def send_command(self):
            curr_key = random.choice(possible_commands)
            self.moves.append(curr_key)
            SendKeys.SendKeys(curr_key)
