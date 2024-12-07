from typing import Any

from utils.colors import Color
from utils.games_generator.control_elements.button import Button


class RangeButton(Button):
    """
    A specialized button for selecting or manipulating number within a range of values.
    """
    _SMALL_BUTTON_SIZE = 10

    def __init__(
            self,
            screen: Any,
            top_left: tuple[float, float],
            size: tuple[float, float],
            color: Color = Color.WHITE,
            value: int = 0,
            value_range: tuple[int, int] = (0, 900),
            step: int = 50,
            box: bool = False,
            font: Any = None
    ):
        """
        Initializes the `ColorButton` object with specified rendering properties and behavior.

        :param screen (Any): The Pygame screen or rendering surface on which this button will be drawn.
        :param top_left (tuple[float, float]): Coordinates (x, y) representing the top-left corner of this button's position.
        :param size (tuple[float, float]): The dimensions of the button (width, height).
        :param color (Color): The default color of the button. Defaults to `Color.WHITE`.
        :param value (int): The initial value of the button's state representing the color intensity/index. Defaults to 0.
        :param value_range (tuple[int, int]): Defines the valid range of color indices (e.g., 0 to 900). Defaults to (0, 900).
        :param step (int): Defines how much each click adjusts the value by. Defaults to 50.
        :param box (bool): Whether the button should visually render as a box. Defaults to False.
        :param font (Any): An optional font for rendering text on the button. Defaults to None.
        """
        x, y = top_left
        w, h = size
        self._button_minus = Button(
            screen, (x, y + 5),
            (self._SMALL_BUTTON_SIZE, self._SMALL_BUTTON_SIZE),
            Color.GRAY,
            "-",
            True
        )
        self._button_plus = Button(
            screen, (x + w - self._SMALL_BUTTON_SIZE, y + 5),
            (self._SMALL_BUTTON_SIZE, self._SMALL_BUTTON_SIZE),
            Color.GRAY,
            "+",
            True
        )
        super().__init__(screen, (x + self._SMALL_BUTTON_SIZE, y), (w - 2 * self._SMALL_BUTTON_SIZE, h), color, value,
                         box, font)
        self._step = step
        self._min_value, self._max_value = value_range

    def set_value(self, mouse_position: tuple[float, float] = None, value: Any = None):
        """
        Handles changes to the value by clicking on the "+" or "-" buttons.

        :param value: The new value to set. If None, determine based on the mouse click logic.
        :param mouse_position: The current mouse position.
        """
        if self._button_minus.rect.collidepoint(mouse_position):
            self.value = max(self.value - self._step, self._min_value)
        if self._button_plus.rect.collidepoint(mouse_position):
            self.value = min(self.value + self._step, self._max_value)

    def click(self, mouse_position: tuple[float, float]) -> bool:
        return self._button_minus.rect.collidepoint(mouse_position) or self._button_plus.rect.collidepoint(
            mouse_position)

    def draw(self):
        super().draw()
        self._button_plus.draw()
        self._button_minus.draw()
