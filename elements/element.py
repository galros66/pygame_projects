from typing import Literal, Union, Optional

import pymunk
from pymunk import Transform

VEC2 = Union[tuple[float, float], list[float, float]]
class Element:
    items = []

    def __init__(
            self,
            mass: float = 1.0,
            moment: float = 0.0,
            body_type: Literal[pymunk.Body.STATIC, pymunk.Body.KINEMATIC, pymunk.Body.DYNAMIC] = pymunk.Body.STATIC,
            position: VEC2 = (0.0, 0.0),
            velocity: VEC2 = (0.0, 0.0),
            force: Optional[VEC2] = (0.0, 0.0),
            angle: Optional[float] = 0.0,
            radius: Optional[float] = 0.0,
            vertices: Optional[list[VEC2]] = None,
            transform: Optional[Transform] = None,
            size: Optional[VEC2] = None,
            a: Optional[VEC2] = None,
            b: Optional[VEC2] = None,
            friction: Optional[float] = 0.0,
            elasticity: float = 1.0,
            sensor: Optional[bool] = False,
            collision_type: int = 0,
            color: tuple[int, int, int, int] = (0, 0, 0, 0),
            group: int = 0,
    ):
        self.body = pymunk.Body(mass=mass, moment=moment, body_type=body_type)
        self.body.position = position
        self.body.velocity = velocity
        self.body.force = force
        self.body.angle = angle

        if a and b:
            self.shape = pymunk.Segment(body=self.body, a=a, b=b, radius=radius)
        elif size:
            self.shape = pymunk.Poly.create_box(body=self.body, size=size, radius=radius)
        elif vertices:
            self.shape = pymunk.Poly(body=self.body, vertices=vertices, transform=transform, radius=radius)
        else:
            self.shape = pymunk.Circle(body=self.body, radius=radius)

        self.shape.friction = friction
        self.shape.elasticity = elasticity
        self.shape.sensor = sensor
        self.shape.collision_type = collision_type
        self.shape.color = color
        self.shape.filter = pymunk.ShapeFilter(group=group)

        self.items += [self.body, self.shape]

