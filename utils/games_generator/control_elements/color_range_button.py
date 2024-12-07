from typing import Any

from utils.colors import Color
from utils.games_generator.control_elements.button import Button


class ColorRangeButton(Button):
    _all_colors = Color.get_all()

    def __init__(
            self,
            screen: Any,
            top_left: tuple[float, float],
            size: tuple[float, float],
    ):
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

    def get_value(self, mouse_position: tuple[float, float] = None):
        if mouse_position is None: return None
        for button in self._colors_buttons:
            if button.rect.collidepoint(mouse_position):
                return button.color
        return None
