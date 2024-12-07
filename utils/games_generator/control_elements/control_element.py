from typing import Any

from utils.colors import Color
from utils.games_generator.control_elements.button import Button
from utils.games_generator.control_elements.color_button import ColorButton
from utils.games_generator.control_elements.range_button import RangeButton
from utils.games_generator.control_elements.select_point_button import SelectPointButton


class ControlElement(Button):
    _ELEMENT_WIDTH = 100
    control_elements = dict()

    def __init__(self, screen: Any, element: str, top_left: tuple[float, float], size: tuple[float, float],
                 color: Color = Color.WHITE, n_colors: int = None, area_top_left: tuple[float, float] = None,
                 area_size: tuple[float, float] = None, value: Any = None,
                 value_range: tuple[int, int] = None, step: int = None, box: bool = False, font: Any = None):
        super().__init__(screen, top_left, size, color, value, box, font)
        x, y = top_left
        w, h = size
        self._is_range_button = isinstance(value, int) and isinstance(value_range, tuple) and isinstance(step, int)
        self._is_color_button = n_colors is not None

        if self._is_color_button:
            self.button = ColorButton(screen=screen, top_left=(x + self._ELEMENT_WIDTH, y),
                                      size=(w - self._ELEMENT_WIDTH, h), color=color, n_colors=n_colors)

        elif self._is_range_button:
            self.button = RangeButton(screen=screen, top_left=(x + self._ELEMENT_WIDTH, y),
                                      size=(w - self._ELEMENT_WIDTH, h), color=color,
                                      value=value, value_range=value_range, step=step, box=box, font=font
                                      )
        elif area_size and area_top_left:
            self.button = SelectPointButton(screen=screen, top_left=(x + self._ELEMENT_WIDTH, y),
                                            size=(w - self._ELEMENT_WIDTH, h), area_top_left=area_top_left,
                                            area_size=area_size)
        else:
            self.button = Button(
                screen=screen, top_left=(x + self._ELEMENT_WIDTH, y), size=(w - self._ELEMENT_WIDTH, h), color=color,
                value=value, box=box, font=font
            )

        self.element = Button(screen, (x, y), (self._ELEMENT_WIDTH, h), value=element)
        self.control_elements[element] = self.button

    def draw(self):
        self.element.draw()
        self.button.draw()

    def set_value(self, mouse_position: tuple[float, float] = None, value: Color = None):
        self.button.set_value(mouse_position, value)

    @classmethod
    def get_control_element_value(cls, element: str) -> Any:
        return cls.control_elements[element].get_value()

    @classmethod
    def set_control_element_value(cls, element: str, value: Any) -> Any:
        cls.control_elements[element].value = value
