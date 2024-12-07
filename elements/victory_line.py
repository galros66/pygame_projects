import pymunk

from elements.element import Element
from utils.colors import Color


class VictoryLine(Element):

    def __init__(
            self,
            position: tuple[float, float] = (0, 0),
            size: tuple[float, float] = (10, 10),
            color: tuple[int, int, int, int] = Color.BLACK.value,
            group: int = 3,
    ):
        super().__init__(
            position=position,
            size=size,
            group=group,
            collision_type=group,
            body_type=pymunk.Body.KINEMATIC,
            color=color,
        )
