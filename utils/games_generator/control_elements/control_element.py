from typing import Any

from utils.colors import Color
from utils.games_generator.control_elements.button import Button
from utils.games_generator.control_elements.color_button import ColorButton
from utils.games_generator.control_elements.range_button import RangeButton
from utils.games_generator.control_elements.select_point_button import SelectPointButton


class ControlElement(Button):
    """
    ControlElement represents a customizable, interactive UI element with specific behavior
    based on its parameters (e.g., `value_range`, `step`, `n_colors`, etc.).

    This class represents different control types (like buttons/sliders) depending on
    the attributes passed during initialization.
    """
    _ELEMENT_WIDTH = 100
    control_elements = dict()  # all the elements that created

    def __init__(self, screen: Any, element: str, top_left: tuple[float, float], size: tuple[float, float],
                 color: Color = Color.WHITE, n_colors: int = None, area_top_left: tuple[float, float] = None,
                 area_size: tuple[float, float] = None, value: Any = None,
                 value_range: tuple[int, int] = None, step: int = None, box: bool = False, font: Any = None):
        """
        Initializes a ControlElement button with various customizable properties.

        :param screen (Any): The Pygame screen or rendering surface where the button will be displayed.
        :param element (str): The name or type of the control element, used for identifying its purpose.
        :param top_left (tuple[float, float]): Coordinates (x, y) defining the top-left position of the button.
        :param size (tuple[float, float]): Width and height of the button, specified as a tuple (width, height).
        :param color (Color, optional): The button's default color (default is white).
        :param n_colors (int, optional): Number of colors to handle for the button's behavior.
        :param area_top_left (tuple[float, float], optional): Top-left coordinates of the clickable area for this control.
        :param area_size (tuple[float, float], optional): Size of the clickable area.
        :param value (Any, optional): The initial value or state the button will maintain.
        :param value_range (tuple[int, int], optional): The range of values allowed for this control element.
        :param step (int, optional): The step size to adjust the value by when interacting with the button.
        :param box (bool, optional): Whether this control is part of a visual "box" interface.
        :param font (Any, optional): The font used for displaying text on this button.
        """
        super().__init__(screen, top_left, size, color, value, box, font)
        x, y = top_left
        w, h = size

        if n_colors is not None:
            self.button = ColorButton(screen=screen, top_left=(x + self._ELEMENT_WIDTH, y),
                                      size=(w - self._ELEMENT_WIDTH, h), color=color, n_colors=n_colors)

        elif isinstance(value, int) and isinstance(value_range, tuple) and isinstance(step, int):
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
