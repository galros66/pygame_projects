import random

import pygame

from utils.colors import Color
from utils.games_generator.control_elements.button import Button
from utils.games_generator.control_elements.color_button import ColorButton
from utils.games_generator.control_elements.control_element import ControlElement
from utils.games_generator.control_elements.select_point_button import SelectPointButton
from utils.games_generator.control_elements.tiles import TileButton
from utils.games_generator.game_generator_base import GameGeneratorBase


class SquareRaceGameGenerator(GameGeneratorBase):
    BOUNDARIES_ELEMENTS = "boundaries"
    BOUNDARIES_LINES_ELEMENTS = "boundaries_lines"
    VICTORY_LINE_ELEMENTS = "victory_line"
    BRICKS_ELEMENTS = "bricks"

    GROUPS = {
        BOUNDARIES_ELEMENTS: 1,
        BOUNDARIES_LINES_ELEMENTS: 1,
        VICTORY_LINE_ELEMENTS: 2,
        BRICKS_ELEMENTS: 3
    }

    SIZES = {
        BRICKS_ELEMENTS: (15, 15),
    }

    def __init__(self, game_name: str = "Square Race"):
        super().__init__(game_name)

    def _draw(self):
        super()._draw()
        bricks_position_button = ControlElement.control_elements["bricks position"]
        victory_line_a_button = ControlElement.control_elements["victory_line a"]
        victory_line_b_button = ControlElement.control_elements["victory_line b"]

        # Draw start point
        if bricks_position_button.value is not None:
            pygame.draw.circle(self.screen, Color.GREEN.value, bricks_position_button.value,
                               5)  # Draws a small green circle

        # Draw end line
        if victory_line_a_button.value and victory_line_b_button.value:
            pygame.draw.line(self.screen, Color.RED.value, victory_line_a_button.value, victory_line_b_button.value, 4)

    def _get_control_elements(self) -> list[Button]:
        x, y = self._control_x, self._control_y
        w, h = self._control_w, self._control_h
        self._control_idx += 4
        return [
            *super()._get_control_elements(),
            ControlElement(self.screen, "bricks number", (x, y + self._control_idx * h), (w, h), value=2,
                           value_range=(2, 5), step=1),
            ControlElement(self.screen, "bricks colors", (x, y + (1 + self._control_idx) * h), (w, h), n_colors=2),
            ControlElement(self.screen, "bricks position", (x, y + (2 + self._control_idx) * h), (w, h),
                           area_top_left=(0, 0), area_size=(self.width, self.height)),
            ControlElement(self.screen, "boundaries color", (x, y + (3 + self._control_idx) * h), (w, h), n_colors=1,
                           color=Color.BLUE),
            ControlElement(self.screen, "victory_line a", (x, y + (4 + self._control_idx) * h), (w, h),
                           area_top_left=(0, 0), area_size=(self.width, self.height)),
            ControlElement(self.screen, "victory_line b", (x, y + (5 + self._control_idx) * h), (w, h),
                           area_top_left=(0, 0), area_size=(self.width, self.height)),
        ]

    def _get_buttons(self) -> dict[str, Button]:
        return dict(
            **super()._get_buttons(),
            **{"tiles": TileButton(self.screen, (0, 0), (self.width, self.height))}
        )

    def _add_data(self):
        super()._add_data()
        self._add_boundaries_data()
        self._add_bricks_data()
        self._add_victory_line_data()

    def _add_boundaries_data(self):
        color = ControlElement.control_elements["boundaries color"].get_value().value
        borders = self._buttons["tiles"].border
        borders_lines = self._buttons["tiles"].border_lines
        self.data[self.BOUNDARIES_ELEMENTS] = [
            {
                "position": (border.rect.x + border.rect.size[0] / 2, border.rect.y + border.rect.size[1] / 2),
                "size": border.rect.size,
                "group": self.GROUPS[self.BOUNDARIES_ELEMENTS],
                "color": color
            } for border in borders
        ]
        self.data[self.BOUNDARIES_LINES_ELEMENTS] = [
            {
                "a": a,
                "b": b,
                "group": self.GROUPS[self.BOUNDARIES_LINES_ELEMENTS],
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
        bricks_colors_buttons = ControlElement.control_elements["bricks colors"].colors_buttons
        start_position = ControlElement.control_elements["bricks position"].value
        colors = [button.color.value for button in bricks_colors_buttons]
        self.data[self.BRICKS_ELEMENTS] = [
            {
                "position": start_position,
                "size": self.SIZES[self.BRICKS_ELEMENTS],
                "velocity": self._get_random_velocity(),
                "group": self.GROUPS[self.BRICKS_ELEMENTS] + i,
                "color": colors[i]
            } for i in range(len(colors))
        ]

    def _add_victory_line_data(self):
        victory_line_a = ControlElement.control_elements["victory_line a"].value
        victory_line_b = ControlElement.control_elements["victory_line b"].value
        dx, dy = abs(victory_line_a[0] - victory_line_b[0]), abs(victory_line_a[1] - victory_line_b[1])
        a, b = min(victory_line_a[0], victory_line_b[0]), min(victory_line_a[1], victory_line_b[1])
        box_size = 6
        x_pos, y_pos = (
        [a - box_size // 2, a + box_size // 2], [b + y for y in range(0, dy, box_size)]) if dx == 0 else (
            [a + x for x in range(0, dx, box_size)], [b - box_size // 2, b + box_size // 2])

        self.data[self.VICTORY_LINE_ELEMENTS] = [{
            "position": (x, y),
            "size": (box_size, box_size),
            "color": Color.BLACK.value if (x_pos.index(x) + y_pos.index(y)) % 2 == 0 else Color.WHITE.value,
            "group": self.GROUPS[self.VICTORY_LINE_ELEMENTS]

        } for x in x_pos for y in y_pos]

    def _mouse_button_down_handler(self, mouse_position: tuple[float, float]):
        color_range_button = self._buttons["color range"]
        tiles_button = self._buttons["tiles"]
        done_button = self._buttons["done"]
        screen_color_button = ControlElement.control_elements["screen color"]
        boundaries_color_button = ControlElement.control_elements["boundaries color"]
        bricks_number_button = ControlElement.control_elements["bricks number"]
        bricks_colors_button = ControlElement.control_elements["bricks colors"]
        victory_line_a_button = ControlElement.control_elements["victory_line a"]
        victory_line_b_button = ControlElement.control_elements["victory_line b"]

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
