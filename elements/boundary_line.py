import  pymunk
from elements.element import Element

class BoundaryLine(Element):
    _default_values = {
        "color": (0, 0, 0, 0),
        "body_type": pymunk.Body.STATIC,
        "radius": 1
    }
    def __init__(
            self,
            a: tuple[float, float] = (0, 0),
            b: tuple[float, float] = (0, 0),
            group: int = 1,
    ):
        super().__init__(
            a=a,
            b=b,
            group=group,
            **self._default_values
        )

