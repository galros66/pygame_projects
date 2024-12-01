from enum import Enum


class Color(Enum):
    BLACK = (0, 0, 0, 255)
    GRAY = (200, 180, 200, 255)
    RED = (255, 0, 0, 255)
    GREEN = (0, 170, 0, 255)
    YELLOW = (255, 255, 0, 255)
    DARK_PURPLE = (85, 0, 85, 255)
    ORANGE = (255, 85, 0, 255)
    PURPLE = (170, 0, 170, 255)
    PINK = (255, 0, 170, 255)
    BLUE = (0, 0, 255, 255)
    LIGHT_BLUE = (0, 170, 255, 255)
    BROWN = (85, 0, 0, 255)
    PEACH = (255, 170, 85, 255)
    WHITE = (255, 255, 255, 255)
    BANANA = (255, 255, 170, 255)
    LIGHT_PEACH = (255, 170, 170, 255)
    NAVY = (0, 0, 85, 255)
    LIGHT_PURPLE = (170, 170, 255, 255)
    LIGHT_PINK = (255, 170, 255, 255)
    LIGHT_ORANGE = (255, 170, 0, 255)
    YELLOW_LIME = (170, 255, 85, 255)
    TURQUOISE = (0, 170, 170, 255)
    DARK_GREEN = (0, 85, 0, 255)
    BORDON = (170, 85, 85, 255)
    LIGHT_BROWN = (170, 85, 0, 255)
    OLIVE = (102, 102, 0, 255)
    UNIQUE_PURPLE = (102, 102, 255, 255)
    UNIQUE_PINK = (255, 0, 153, 255)
    LIGHT_YELLOW = (255, 255, 204, 255)
    OCEAN = (0, 204, 204, 255)
    DARK_BLUE = (51, 0, 153, 255)
    GRAY2 = (120, 144, 120, 255)
    BANANA2 = (240, 216, 160, 255)
    GREEN2 = (0, 180, 0, 255)
    PURPLE2 = (200, 36, 120, 255)

    @classmethod
    def get_all(cls):
        return [c for c in Color]

    @classmethod
    def get_basic_colors(cls):
        return [
            cls.BLACK,
            cls.GRAY,
            cls.WHITE,
            cls.RED,
            cls.GREEN,
            cls.BLUE,
            cls.ORANGE,
            cls.YELLOW,
            cls.PURPLE,
            cls.BROWN,
            cls.LIGHT_BLUE,
            cls.PINK,
            cls.PEACH,
            cls.YELLOW_LIME,
        ]

    def __str__(self):
        return self.name
