from typing import Any

from utils.colors import Color
from utils.games_generator.control_elements.button import Button


class ColorButton(Button):
    """
    Represents a color selection button in the Game Generator UI.

    This button allows the user to select or interact with colors dynamically,
    enabling visual selection for player colors, interface changes, or other game settings.

    Attributes:
        :param _all_colors (list): List of all available colors generated by the `Color.get_all()` method.
        :param _waiting (list): List used for deferred processing while handling multiple color selections.
    """
    _all_colors = Color.get_all()
    _waiting = []

    def __init__(
            self,
            screen: Any,
            top_left: tuple[float, float],
            size: tuple[float, float],
            n_colors: int = 1,
            color: Color = Color.WHITE,
    ):
        """
        Initialize a ColorButton instance for interactive color selection.

        Args:
            :param screen (Any): The rendering surface (e.g., Pygame's surface) where the button will appear.
            :param top_left (tuple[float, float]): Coordinates (x, y) of the button's top-left corner on the screen.
            :param size (tuple[float, float]): Dimensions (width, height) of the button's clickable area.
            :param n_colors (int, optional): Number of colors this button will represent. Defaults to 1.
            :param color (Color, optional): Default color of the button. Defaults to Color.WHITE.
        """
        super().__init__(screen, top_left, size, color)
        self.colors_buttons = []
        self.reset_n_colors(n_colors=n_colors, color=color)

    @classmethod
    def set_waiting(cls, value: Color):
        """
        Updates the button's color to the first color in the waiting queue, if any exist.
        """
        if value is not None and cls._waiting:
            button = cls._waiting.pop(0)
            button._box = False
            button.color = value

    def reset_n_colors(self, n_colors: int, color: Color = None):
        """
        Resize and reset the buttons colors list to the specified number of colors (`n_colors`).
        If the new size is larger, it fills the new slots with the provided `color` or from `_all_colors`.
        If smaller, it truncates the list to keep only the first n_colors.

        :param n_colors: Desired number of colors in the waiting queue.
        :param color: Default color to fill if n_colors are increased.
        """
        assert n_colors <= len(self._all_colors)
        x, y = self.rect.topleft
        w, h = self.rect.size
        w = w // n_colors
        if n_colors == 1 and color:
            self._all_colors = [color]
        self.colors_buttons = [
            Button(
                self._screen, (x + w * i, y),
                (w, h),
                self.colors_buttons[i].color if i < len(self.colors_buttons) else self._all_colors[i],
            ) for i in range(n_colors)
        ]

    def set_value(self, mouse_position: tuple[float, float] = None, value: Color = None):
        """
        Adds a color to the waiting queue if it's not already there, or removes it if it's already in the queue.

        :param mouse_position: The position of the mouse cursor, if relevant.
        :param value: The color to add or remove from the waiting queue.
        """
        if mouse_position is None: return
        for button in self.colors_buttons:
            if button.rect.collidepoint(mouse_position):
                if button not in self._waiting:
                    button._box = True
                    self._waiting.append(button)
                else:
                    self._waiting.remove(button)
                    button._box = False

    def get_value(self, mouse_position: tuple[float, float] = None) -> Any:
        """
        Returns the color that was clicked if the mouse position corresponds to one in the waiting list.
        If no specific color was clicked, returns the first color in the list.

        :param mouse_position: The position of the mouse cursor for detecting clicks.
        :return: The selected color or the first color in the waiting queue if none was clicked.
        """
        if mouse_position is None: return self.colors_buttons[0].color
        for button in self.colors_buttons:
            if button.rect.collidepoint(mouse_position):
                return button.color
        return None

    def draw(self):
        super().draw()
        for button in self.colors_buttons: button.draw()
