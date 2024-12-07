from typing import Any

import pygame

from utils.colors import Color


class Button:
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

    def get_value(self, mouse_position: tuple[float, float] = None):
        return self.value
