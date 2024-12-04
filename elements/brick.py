import pymunk

from elements.element import Element


class Brick(Element):
    _default_values = {
        "mass": 1,
        "moment": float('inf'),
        "body_type": pymunk.Body.DYNAMIC,
    }

    def __init__(
            self,
            position: tuple[float, float] = (0, 0),
            size: tuple[float, float] = (15, 15),
            velocity: tuple[float, float] = (0, 0),
            group: int = 2,
            color: tuple[int, int, int, int] = (255, 0, 0, 255),
    ):
        super().__init__(
            position=position,
            velocity=velocity,
            size=size,
            group=group,
            color=color,
            collision_type=group,
            **self._default_values
        )
