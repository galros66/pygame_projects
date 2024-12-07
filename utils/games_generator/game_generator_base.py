import json
import os

import pygame

from utils.colors import Color
from utils.games_generator.control_elements.button import Button
from utils.games_generator.control_elements.color_range_button import ColorRangeButton
from utils.games_generator.control_elements.control_element import ControlElement


class GameGeneratorBase:
    DIR = r"C:\ws\pygame_projects\utils\games_data"
    _CONTROL_HEIGHT = 100
    _CONTROL_WIDTH = 200

    def __init__(self, game_name: str):
        self.game_name = game_name

        self.screen = None
        self.width, self.height = 400, 600
        self.data = dict()
        self._control_elements = None
        self._buttons = None

        self._control_idx = 0
        self._control_x, self._control_y = self.width + 10, 5
        self._control_w, self._control_h = self._CONTROL_WIDTH - 20, 25

        self._running = True

    def generate(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width + self._CONTROL_WIDTH, self.height + self._CONTROL_HEIGHT))
        pygame.display.set_caption(f"Interactive Game {self.game_name} Setup with Control Panel")
        self._control_elements = self._get_control_elements()
        self._buttons = self._get_buttons()
        print(self._buttons)
        while self._running:
            self._draw()
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._mouse_button_down_handler(mouse_pos)
            pygame.display.flip()

        self._save_data()
        pygame.quit()

    def _mouse_button_down_handler(self, mouse_position: tuple[float, float]):
        pass

    def _add_data(self):
        screen_size = ControlElement.control_elements["screen width"].value, ControlElement.control_elements[
            "screen height"].value
        screen_color = ControlElement.control_elements["screen color"].get_value().value
        clock_fps = ControlElement.control_elements["clock fpc"].value
        space_gravity = ControlElement.control_elements["space gravity_x"].value, ControlElement.control_elements[
            "space gravity_y"].value
        space_step = ControlElement.control_elements["space step"].value
        logo_position = ControlElement.control_elements["logo position"].value
        self.data |= {
            "screen": {"size": screen_size, "color": screen_color},
            "clock": {"fps": clock_fps},
            "space": {"gravity": space_gravity, "step": space_step},
            "logo": {"position": logo_position},
        }

    def _save_data(self):
        self._add_data()
        snack_name = self.game_name.lower().replace(' ', '_')
        n = len([f for f in os.listdir(self.DIR) if f.startswith(snack_name)])
        file = f"{snack_name}_game_data_{n}.json"
        with open(os.path.join(self.DIR, file), "w") as f:
            json.dump(self.data, f, indent=4)
        print(f"{self.game_name} Game data saved successfully!")

    def _draw(self):
        logo_position_button = ControlElement.control_elements["logo position"]

        self.screen.fill(ControlElement.get_control_element_value("screen color").value)

        for e in self._control_elements: e.draw()
        for b in self._buttons.values(): b.draw()

        if logo_position_button.value is not None:
            font = pygame.font.SysFont("Agency FB", 20)
            text = font.render("@ grr.sim.games", True, Color.BLACK.value)
            text_rect = text.get_rect(center=logo_position_button.value)
            self.screen.blit(text, text_rect)

    def _get_control_elements(self) -> list[ControlElement]:
        x, y = self._control_x, self._control_y
        w, h = self._control_w, self._control_h
        self._control_idx = 8
        return [
            Button(self.screen, (self.width, 0), (self._CONTROL_WIDTH, self.height), color=Color.WHITE),
            ControlElement(self.screen, "screen width", (x, y), (w, h), value=400, value_range=(400, 400), step=50),
            ControlElement(self.screen, "screen height", (x, y + h), (w, h), value=600, value_range=(600, 600),
                           step=50),
            ControlElement(self.screen, "screen color", (x, y + 2 * h), (w, h), color=Color.GRAY, n_colors=1),
            ControlElement(self.screen, "clock fpc", (x, y + 3 * h), (w, h), value=60, value_range=(10, 360), step=10),
            ControlElement(self.screen, "space gravity_x", (x, y + 4 * h), (w, h), value=0, value_range=(-900, 900),
                           step=100),
            ControlElement(self.screen, "space gravity_y", (x, y + 5 * h), (w, h), value=0, value_range=(-900, 900),
                           step=100),
            ControlElement(self.screen, "space step", (x, y + 6 * h), (w, h), value=60, value_range=(10, 180), step=10),
            ControlElement(self.screen, "logo position", (x, y + 7 * h), (w, h),
                           area_top_left=(0, 0), area_size=(self.width, self.height)),
        ]

    def _get_buttons(self) -> dict[str, Button]:
        return {
            "color range": ColorRangeButton(self.screen, (0, self.height),
                                            (self._CONTROL_WIDTH + self.width, self._CONTROL_HEIGHT)),
            "done": Button(self.screen, (self._control_x, self._control_y + (20 * self._control_h)),
                           (self._control_w, self._control_h), value="DONE", color=Color.GRAY, box=True),
        }
