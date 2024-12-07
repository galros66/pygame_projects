from typing import Any

from utils.colors import Color
from utils.games_generator.control_elements.button import Button


class ColorButton(Button):
    _SMALL_BUTTON_SIZE = 10
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
        super().__init__(screen, top_left, size, color)
        self.colors_buttons = []
        self.reset_n_colors(n_colors=n_colors, color=color)

    def set_value(self, mouse_position: tuple[float, float] = None, value: Color = None):
        if mouse_position is None: return
        for button in self.colors_buttons:
            if button.rect.collidepoint(mouse_position):
                if button not in self._waiting:
                    button._box = True
                    self._waiting.append(button)
                else:
                    self._waiting.remove(button)
                    button._box = False

    @classmethod
    def set_waiting(cls, value: Color):
        if value is not None and cls._waiting:
            button = cls._waiting.pop(0)
            button._box = False
            button.color = value

    def get_value(self, mouse_position: tuple[float, float] = None):
        if mouse_position is None: return self.colors_buttons[0].color
        for button in self.colors_buttons:
            if button.rect.collidepoint(mouse_position):
                return button.color
        return None

    def reset_n_colors(self, n_colors: int, color: Color = None):
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

    def draw(self):
        super().draw()
        for button in self.colors_buttons: button.draw()
