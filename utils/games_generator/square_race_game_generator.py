import random

import pygame

from utils.colors import Color
from utils.games_generator.control_elements.button import Button
from utils.games_generator.control_elements.color_button import ColorButton
from utils.games_generator.control_elements.control_element import ControlElement
from utils.games_generator.control_elements.select_point_button import SelectPointButton
from utils.games_generator.control_elements.tiles import TilesButton
from utils.games_generator.game_generator_base import GameGeneratorBase


class SquareRaceGameGenerator(GameGeneratorBase):
    _NUMBER_STR = "number"
    _COLORS_STR = "colors"
    _TILES_STR = "tiles"
    _VELOCITY_STR = "velocity"
    _A_CHR = "a"
    _B_CHR = "b"

    _BOUNDARIES_ELEMENTS = "boundaries"
    _BOUNDARIES_LINES_ELEMENTS = "boundaries_lines"
    _VICTORY_LINE_ELEMENTS = "victory_line"
    _BRICKS_ELEMENTS = "bricks"

    _BOUNDARIES_COLOR_ELEMENT = f"{_BOUNDARIES_ELEMENTS} {GameGeneratorBase._COLOR_STR}"
    _VICTORY_LINE_A_ELEMENT = f"{_VICTORY_LINE_ELEMENTS} {_A_CHR}"
    _VICTORY_LINE_B_ELEMENT = f"{_VICTORY_LINE_ELEMENTS} {_B_CHR}"
    _BRICKS_NUMBER_ELEMENT = f"{_BRICKS_ELEMENTS} {_NUMBER_STR}"
    _BRICKS_COLORS_ELEMENT = f"{_BRICKS_ELEMENTS} {_COLORS_STR}"
    _BRICKS_POSITION_ELEMENT = f"{_BRICKS_ELEMENTS} {GameGeneratorBase._POSITION_STR}"

    _GAME_NAME = "Square Race"

    GROUPS = {
        _BOUNDARIES_ELEMENTS: 1,
        _BOUNDARIES_LINES_ELEMENTS: 1,
        _VICTORY_LINE_ELEMENTS: 2,
        _BRICKS_ELEMENTS: 3
    }

    SIZES = {
        _BRICKS_ELEMENTS: (15, 15),
    }

    def __init__(self):
        super().__init__(self._GAME_NAME)

    def _draw(self):
        super()._draw()
        bricks_position_button = ControlElement.control_elements[self._BRICKS_POSITION_ELEMENT]
        victory_line_a_button = ControlElement.control_elements[self._VICTORY_LINE_A_ELEMENT]
        victory_line_b_button = ControlElement.control_elements[self._VICTORY_LINE_B_ELEMENT]

        # Draw start point
        if bricks_position_button.value is not None:
            # Draws a small green circle
            pygame.draw.circle(self.screen, Color.GREEN.value, bricks_position_button.value, 5)

            # Draw end line
        if victory_line_a_button.value and victory_line_b_button.value:
            pygame.draw.line(self.screen, Color.RED.value, victory_line_a_button.value, victory_line_b_button.value, 4)

    def _get_control_elements(self) -> list[Button]:
        x, y = self._control_x, self._control_y
        w, h = self._control_w, self._control_h
        self._control_idx += 4
        return [
            *super()._get_control_elements(),
            ControlElement(self.screen, self._BRICKS_NUMBER_ELEMENT, (x, y + self._control_idx * h), (w, h), value=2,
                           value_range=(2, 5), step=1),
            ControlElement(self.screen, self._BRICKS_COLORS_ELEMENT, (x, y + (1 + self._control_idx) * h), (w, h),
                           n_colors=2),
            ControlElement(self.screen, self._BRICKS_POSITION_ELEMENT, (x, y + (2 + self._control_idx) * h), (w, h),
                           area_top_left=(0, 0), area_size=(self.width, self.height)),
            ControlElement(self.screen, self._BOUNDARIES_COLOR_ELEMENT, (x, y + (3 + self._control_idx) * h), (w, h),
                           n_colors=1, color=Color.BLUE),
            ControlElement(self.screen, self._VICTORY_LINE_A_ELEMENT, (x, y + (4 + self._control_idx) * h), (w, h),
                           area_top_left=(0, 0), area_size=(self.width, self.height)),
            ControlElement(self.screen, self._VICTORY_LINE_B_ELEMENT, (x, y + (5 + self._control_idx) * h), (w, h),
                           area_top_left=(0, 0), area_size=(self.width, self.height)),
        ]

    def _get_buttons(self) -> dict[str, Button]:
        return dict(
            **super()._get_buttons(),
            **{self._TILES_STR: TilesButton(self.screen, (0, 0), (self.width, self.height))}
        )

    def _add_data(self):
        super()._add_data()
        self._add_boundaries_data()
        self._add_bricks_data()
        self._add_victory_line_data()

    def _add_boundaries_data(self):
        color = ControlElement.control_elements[self._BOUNDARIES_COLOR_ELEMENT].get_value().value
        borders = self._buttons[self._TILES_STR].border
        borders_lines = self._buttons[self._TILES_STR].border_lines
        self.data[self._BOUNDARIES_ELEMENTS] = [
            {
                self._POSITION_STR: (border.rect.x + border.rect.size[0] / 2, border.rect.y + border.rect.size[1] / 2),
                self._SIZE_STR: border.rect.size,
                self._GROUP_STR: self.GROUPS[self._BOUNDARIES_ELEMENTS],
                self._COLOR_STR: color
            } for border in borders
        ]
        self.data[self._BOUNDARIES_LINES_ELEMENTS] = [
            {
                self._A_CHR: a,
                self._B_CHR: b,
                self._GROUP_STR: self.GROUPS[self._BOUNDARIES_LINES_ELEMENTS],
            } for [a, b] in borders_lines
        ]

    @classmethod
    def _get_random_velocity(cls) -> tuple[float, float]:
        v = [i for i in range(-10, 10)]
        v.remove(0)
        vx, vy = random.choice(v), random.choice(v)
        norm = 50 / float((vx ** 2 + vy ** 2) ** 0.5)
        return vx * norm, vy * norm

    def _add_bricks_data(self):
        bricks_colors_buttons = ControlElement.control_elements[self._BRICKS_COLORS_ELEMENT].colors_buttons
        start_position = ControlElement.control_elements[self._BRICKS_POSITION_ELEMENT].value
        colors = [button.color.value for button in bricks_colors_buttons]
        self.data[self._BRICKS_ELEMENTS] = [
            {
                self._POSITION_STR: start_position,
                self._SIZE_STR: self.SIZES[self._BRICKS_ELEMENTS],
                self._VELOCITY_STR: self._get_random_velocity(),
                self._GROUP_STR: self.GROUPS[self._BRICKS_ELEMENTS] + i,
                self._COLOR_STR: colors[i]
            } for i in range(len(colors))
        ]

    def _add_victory_line_data(self):
        victory_line_a = ControlElement.control_elements[self._VICTORY_LINE_A_ELEMENT].value
        victory_line_b = ControlElement.control_elements[self._VICTORY_LINE_B_ELEMENT].value
        dx, dy = abs(victory_line_a[0] - victory_line_b[0]), abs(victory_line_a[1] - victory_line_b[1])
        a, b = min(victory_line_a[0], victory_line_b[0]), min(victory_line_a[1], victory_line_b[1])
        box_size = 6
        x_pos, y_pos = (
            [a - box_size // 2, a + box_size // 2], [b + y for y in range(0, dy, box_size)]) if dx == 0 else (
            [a + x for x in range(0, dx, box_size)], [b - box_size // 2, b + box_size // 2])

        self.data[self._VICTORY_LINE_ELEMENTS] = [{
            self._POSITION_STR: (x, y),
            self._SIZE_STR: (box_size, box_size),
            self._COLOR_STR: Color.BLACK.value if (x_pos.index(x) + y_pos.index(y)) % 2 == 0 else Color.WHITE.value,
            self._GROUP_STR: self.GROUPS[self._VICTORY_LINE_ELEMENTS]

        } for x in x_pos for y in y_pos]

    def _mouse_button_down_handler(self, mouse_position: tuple[float, float]):
        color_range_button = self._buttons[self._COLOR_RANGE_STR]
        tiles_button = self._buttons[self._TILES_STR]
        done_button = self._buttons[self._DONE_STR]
        screen_color_button = ControlElement.control_elements[self._SCREEN_COLOR_ELEMENT]
        boundaries_color_button = ControlElement.control_elements[self._BOUNDARIES_COLOR_ELEMENT]
        bricks_number_button = ControlElement.control_elements[self._BRICKS_NUMBER_ELEMENT]
        bricks_colors_button = ControlElement.control_elements[self._BRICKS_COLORS_ELEMENT]
        victory_line_a_button = ControlElement.control_elements[self._VICTORY_LINE_A_ELEMENT]
        victory_line_b_button = ControlElement.control_elements[self._VICTORY_LINE_B_ELEMENT]

        if not SelectPointButton.is_select_mode(): tiles_button.set_value(mouse_position)

        SelectPointButton.set_waiting(mouse_position)
        for b in ControlElement.control_elements.values():
            if b != bricks_number_button: b.set_value(mouse_position)

        if color_range_button.click(mouse_position):
            ColorButton.set_waiting(color_range_button.get_value(mouse_position))
            tiles_button.reset_color(screen_color_button.get_value(), boundaries_color_button.get_value())

        if bricks_number_button.click(mouse_position):
            bricks_number_button.set_value(mouse_position)
            bricks_colors_button.reset_n_colors(bricks_number_button.value)

        if victory_line_a_button.value and victory_line_b_button.value:
            dx = abs(victory_line_a_button.value[0] - victory_line_b_button.value[0])
            dy = abs(victory_line_a_button.value[1] - victory_line_b_button.value[1])
            if dx != 0 and dx < dy:
                victory_line_b_button.set_value(value=(victory_line_a_button.value[0], victory_line_b_button.value[1]))
            elif dy != 0 and dy < dx:
                victory_line_b_button.set_value(value=(victory_line_b_button.value[0], victory_line_a_button.value[1]))

        if done_button.click(mouse_position):
            if all([
                button.value is not None
                for button in ControlElement.control_elements.values() if isinstance(button, SelectPointButton)
            ]): self._running = False


if __name__ == '__main__':
    game_generator = SquareRaceGameGenerator()
    game_generator.generate()
