import pymunk
from elements.element import Element


class Boundary(Element):
    def __init__(
            self,
            position: tuple[float, float]=(0,0),
            size: tuple[float, float]=(30, 30),
            color: tuple[int, int, int, int] = (144, 144, 120, 100),
            group: int=1
    ):
        super().__init__(
            position=position,
            size=size,
            body_type=pymunk.Body.STATIC,
            group=group,
            color=color
        )