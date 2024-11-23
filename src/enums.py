import enum


class Direction(enum.Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class EntityType(enum.Enum):
    BORDER = "border"
    FREE = "free"
    SNAKE = "snake"
    FOOD = "food"
