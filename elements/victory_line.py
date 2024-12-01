import  pymunk
from elements.element import Element
from utils.colors import Color


class VictoryLine(Element):

    def __init__(
            self,
            a: tuple[float, float] = (0, 0),
            b: tuple[float, float] = (0, 0),
            radius: float = 5,
            group: int = 3,
    ):
        super().__init__(
            a=a,
            b=b,
            radius=radius,
            group=group,
            collision_type=group,
            body_type=pymunk.Body.KINEMATIC,
            color=Color.RED.value,
        )

