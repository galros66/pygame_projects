from typing import Any

import pygame

from utils.colors import Color


class Button:
    """
    Represents an interactive button element within the Game Generator interface.

    The Button class is used to define clickable elements in the game generator's UI,
    allowing users to trigger specific game generation options, settings, or actions.
    """

    def __init__(
            self,
            screen: Any,
            top_left: tuple[float, float],
            size: tuple[float, float],
            color: Color = Color.WHITE,
            value: Any = None,
            box: bool = False,
            font: Any = None
    ):
        """
        Initialize a Button instance for the Game Generator UI.

        Args:
            :param screen (Any): The rendering surface where the button will appear and respond to clicks.
            :param top_left (tuple[float, float]): Coordinates (x, y) of the button's top-left corner.
            :param size (tuple[float, float]): Dimensions (width, height) that define the button's size.
            :param color (Color, optional): The button's default color. Defaults to `Color.WHITE`.
            :param value (Any, optional): The text, action, or identifier the button represents. Defaults to `None`.
            :param box (bool, optional): Whether to visually include a surrounding box around the button. Defaults to `False`.
            :param font (Any, optional): Font style to render the text value on the button. Defaults to `None`.
        """
        self.rect = pygame.Rect(top_left, size)
        self.color = color
        self.value = value
        self._screen = screen
        self._box = box
        self._font = font

    def draw(self):
        if not self._font: self._font = pygame.font.SysFont("Agency FB", 18)
        pygame.draw.rect(self._screen, self.color.value, self.rect)
        if self._box: pygame.draw.rect(self._screen, Color.BLACK.value, self.rect, 1)
        if self.value is not None:
            text = self._font.render(str(self.value), True, Color.BLACK.value)
            text_rect = text.get_rect(center=self.rect.center)
            self._screen.blit(text, text_rect)

    def click(self, mouse_position: tuple[float, float]) -> bool:
        return self.rect.collidepoint(mouse_position)

    def set_value(self, mouse_position: tuple[float, float] = None, value: Any = None):
        if value is not None: self.value = value

    def get_value(self, mouse_position: tuple[float, float] = None) -> Any:
        return self.value
