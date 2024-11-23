from src.core.game import Game


class Menu:

    def __init__(self, board_size):
        self.board_size  = board_size
        self.game = Game(self.board_size)

    def run(self):
        self.game.loop()
        self.ask_for_restart()

    def ask_for_restart(self):
        i = input("Would you like to restart? Y/N: ")
        if i.upper() == 'Y':
            return self.restart()
        elif i.upper() == 'N':
            print('Thank you for playing!')
            exit()
        else:
            print('Answer must be either "Y" or "N".')
            return self.ask_for_restart()

    def restart(self):
        self.game = Game(self.board_size)
        self.run()
