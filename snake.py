from src.core.menu import Menu
from src.settings import BOARD_SIZE

if __name__ == '__main__':
    menu = Menu(board_size=BOARD_SIZE)
    menu.run()
