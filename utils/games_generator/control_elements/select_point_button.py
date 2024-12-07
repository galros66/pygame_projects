from typing import Any

from utils.games_generator.control_elements.button import Button


class SelectPointButton(Button):
    _waiting = []

    def __init__(
            self,
            screen: Any,
            top_left: tuple[float, float],
            size: tuple[float, float],
            area_top_left: tuple[float, float],
            area_size: tuple[float, float],
    ):
        super().__init__(screen, top_left, size)
        self.area = Button(screen, area_top_left, area_size)

    def set_value(self, mouse_position: tuple[float, float] = None, value: tuple[float, float] = None):
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
        for button in cls._waiting:
            if button.area.click(mouse_position):
                cls._waiting.remove(button)
                button.value = mouse_position
                button._box = False

    @classmethod
    def is_select_mode(cls):
        return len(cls._waiting) > 0
