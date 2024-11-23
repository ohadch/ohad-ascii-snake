import sys
import termios
import tty

from src.enums import EntityType
from src.settings import SPOT_VIEW, SPOT_TYPES


def num_to_view(num):
    return SPOT_VIEW[EntityType(SPOT_TYPES[num])]


def row_to_view(row):
    return ' '.join([num_to_view(n) for n in row])


# Helper function to read a single character
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch