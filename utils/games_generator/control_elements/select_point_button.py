from typing import Any

from utils.games_generator.control_elements.button import Button


class SelectPointButton(Button):
    """
    A button class that allows selecting a point within a defined area by clicking on it.

    This button enables the selection of points within a rectangular area and manages click
    events for tracking the selected points. Selected points are stored in the `_waiting` list.

    Attributes:
        :param _waiting (list): A list to store points selected by user interaction within the area.
    """
    _waiting = []

    def __init__(
            self,
            screen: Any,
            top_left: tuple[float, float],
            size: tuple[float, float],
            area_top_left: tuple[float, float],
            area_size: tuple[float, float],
    ):
        """
        Initialize a SelectPointButton.

        :param screen (Any): The Pygame screen or rendering surface on which this button will be drawn.
        :param top_left (tuple[float, float]): Coordinates (x, y) representing the top-left corner of this button's position.
        :param size (tuple[float, float]): Dimensions of the button (width, height).
        :param area_top_left (tuple[float, float]): The top-left corner of the rectangular area to select points from.
        :param area_size (tuple[float, float]): The size (width, height) of the area where points can be selected.
        """
        super().__init__(screen, top_left, size)
        self.area = Button(screen, area_top_left, area_size)

    def set_value(self, mouse_position: tuple[float, float] = None, value: tuple[float, float] = None):
        """
        Handles mouse clicks to add/remove/update points in the waiting list.

        - If a specific value is provided, it will replace any existing value at that position in the list.
        - If a mouse click occurs within the designated area, the mouse's position is added to or updated in the waiting list.

        :param mouse_position: The position of the mouse click.
        :param value: A specific coordinate value to set in the waiting list.
        """
        if isinstance(value, tuple) and len(value) == 2:
            self.value = value
            return

        if mouse_position is None: return
        if self.click(mouse_position):
            if self in self._waiting:
                self._box = False
                self._waiting.remove(self)
            else:
                self._box = True
                self._waiting.append(self)

    @classmethod
    def set_waiting(cls, mouse_position: tuple[float, float]):
        """
        Updates the first value in the waiting list to the mouse click position if it is within the defined clickable area.

        :param mouse_position: The mouse click position to check and potentially update.
        """
        for button in cls._waiting:
            if button.area.click(mouse_position):
                cls._waiting.remove(button)
                button.value = mouse_position
                button._box = False

    @classmethod
    def is_select_mode(cls) -> bool:
        return len(cls._waiting) > 0
