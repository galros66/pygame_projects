from typing import Any

from utils.colors import Color
from utils.games_generator.control_elements.button import Button


class ColorRangeButton(Button):
    """
    A specialized button for selecting a range of colors.
    Inherits from the base `Button` class.

    This button maintains a range of selectable colors and interacts
    with input events to allow users to select multiple colors from a range.
    """
    _all_colors = Color.get_all()

    def __init__(
            self,
            screen: Any,
            top_left: tuple[float, float],
            size: tuple[float, float],
    ):
        """
        Initialize a ColorRangeButton instance.

        Sets up the button's position, size, and initializes the parent Button class.

        :param screen: The rendering surface to draw on.
        :param top_left: The screen coordinates for the top-left corner of the button.
        :param size: Dimensions of the button (width, height).
        """
        super().__init__(screen=screen, top_left=top_left, size=size)
        x, y = top_left
        w, h = size
        w = w // len(self._all_colors)
        self._colors_buttons = [
            Button(screen, (x + i * w, y), (w, h), color=self._all_colors[i]) for i in range(len(self._all_colors))
        ]

    def draw(self):
        super().draw()
        for button in self._colors_buttons: button.draw()

    def get_value(self, mouse_position: tuple[float, float] = None) -> Any:
        """
        Determines which color the user clicked on within the button range.

        :param mouse_position: The current position of the mouse as (x, y) coordinates.
        :return: The color that was clicked on or `None` if no specific click was detected.
        """
        if mouse_position is None: return None
        for button in self._colors_buttons:
            if button.rect.collidepoint(mouse_position):
                return button.color
        return None
