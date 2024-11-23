from typing import Dict, Tuple

from termcolor import colored

from src.enums import Direction, EntityType

BOARD_SIZE = 20

SPOT_TYPES = {
    -1: 'border',
    0: 'free',
    1: 'snake',
    2: 'food',
}

SPOT_VIEW: Dict[EntityType, str] = {
    EntityType.BORDER: colored('#', 'magenta'),
    EntityType.FREE: " ",
    EntityType.SNAKE: "X",
    EntityType.FOOD: colored('&', 'yellow'),
}

MOVES: Dict[Direction, Tuple[int, int]] = {
    Direction.UP: (-1, 0),
    Direction.DOWN: (1, 0),
    Direction.RIGHT: (0, 1),
    Direction.LEFT: (0, -1),
}

KEY_COMMANDS: Dict[str, Direction] = {
    'w': Direction.UP,
    's': Direction.DOWN,
    'a': Direction.LEFT,
    'd': Direction.RIGHT,
}

OPPOSITE_COMMANDS = {
    v: k for k, v in KEY_COMMANDS.items()
}
