import json
import os

import pygame

from utils.colors import Color
from utils.games_generator.control_elements.button import Button
from utils.games_generator.control_elements.color_range_button import ColorRangeButton
from utils.games_generator.control_elements.control_element import ControlElement
from utils.private_parms import ACCOUNT_USER_NAME


class GameGeneratorBase:
    DIR = r"C:\ws\pygame_projects\utils\games_data"

    _COLOR_STR = "color"
    _POSITION_STR = "position"
    _SIZE_STR = "size"
    _WIDTH_STR = "width"
    _HEIGHT_STR = "height"
    _FPS_STR = "fps"

    _GROUP_STR = "group"
    _GRAVITY_STR = "gravity"
    _STEP_STR = "step"
    _COLOR_RANGE_STR = "color range"
    _DONE_STR = "done"
    _X_CHR = "x"
    _Y_CHR = "y"

    _SCREEN_ELEMENT = "screen"
    _CLOCK_ELEMENT = "clock"
    _SPACE_ELEMENT = "space"
    _LOGO_ELEMENT = "logo"

    _SCREEN_COLOR_ELEMENT = f"{_SCREEN_ELEMENT} {_COLOR_STR}"
    _SCREEN_WIDTH_ELEMENT = f"{_SCREEN_ELEMENT} {_WIDTH_STR}"
    _SCREEN_HEIGHT_ELEMENT = f"{_SCREEN_ELEMENT} {_HEIGHT_STR}"
    _CLOCK_FPS_ELEMENT = f"{_CLOCK_ELEMENT} {_FPS_STR}"
    _SPACE_GRAVITY_X_ELEMENT = f"{_SPACE_ELEMENT} {_GRAVITY_STR}_{_X_CHR}"
    _SPACE_GRAVITY_Y_ELEMENT = f"{_SPACE_ELEMENT} {_GRAVITY_STR}_{_Y_CHR}"
    _SPACE_STEP_ELEMENT = f"{_SPACE_ELEMENT} {_STEP_STR}"
    _LOGO_POSITION_ELEMENT = f"{_LOGO_ELEMENT} {_POSITION_STR}"

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
        screen_size = ControlElement.control_elements[self._SCREEN_WIDTH_ELEMENT].value, \
                      ControlElement.control_elements[self._SCREEN_HEIGHT_ELEMENT].value
        screen_color = ControlElement.control_elements[self._SCREEN_COLOR_ELEMENT].get_value().value
        clock_fps = ControlElement.control_elements[self._CLOCK_FPS_ELEMENT].value
        space_gravity = ControlElement.control_elements[self._SPACE_GRAVITY_X_ELEMENT].value, \
                        ControlElement.control_elements[self._SPACE_GRAVITY_Y_ELEMENT].value
        space_step = ControlElement.control_elements[self._SPACE_STEP_ELEMENT].value
        logo_position = ControlElement.control_elements[self._LOGO_POSITION_ELEMENT].value

        self.data |= {
            self._SCREEN_ELEMENT: {self._SIZE_STR: screen_size, self._COLOR_STR: screen_color},
            self._CLOCK_ELEMENT: {self._FPS_STR: clock_fps},
            self._SPACE_ELEMENT: {self._GRAVITY_STR: space_gravity, self._STEP_STR: space_step},
            self._LOGO_ELEMENT: {self._POSITION_STR: logo_position},
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
        logo_position_button = ControlElement.control_elements[self._LOGO_POSITION_ELEMENT]

        self.screen.fill(ControlElement.control_elements[self._SCREEN_COLOR_ELEMENT].get_value().value)

        for e in self._control_elements: e.draw()
        for b in self._buttons.values(): b.draw()

        if logo_position_button.value is not None:
            font = pygame.font.SysFont("Agency FB", 20)
            text = font.render(f"@ {ACCOUNT_USER_NAME}", True, Color.BLACK.value)
            text_rect = text.get_rect(center=logo_position_button.value)
            self.screen.blit(text, text_rect)

    def _get_control_elements(self) -> list[ControlElement]:
        x, y = self._control_x, self._control_y
        w, h = self._control_w, self._control_h
        self._control_idx = 8
        return [
            Button(self.screen, (self.width, 0), (self._CONTROL_WIDTH, self.height), color=Color.WHITE),
            ControlElement(self.screen, self._SCREEN_WIDTH_ELEMENT, (x, y), (w, h), value=400, value_range=(400, 400),
                           step=50),
            ControlElement(self.screen, self._SCREEN_HEIGHT_ELEMENT, (x, y + h), (w, h), value=600,
                           value_range=(600, 600), step=50),
            ControlElement(self.screen, self._SCREEN_COLOR_ELEMENT, (x, y + 2 * h), (w, h), color=Color.GRAY,
                           n_colors=1),
            ControlElement(self.screen, self._CLOCK_FPS_ELEMENT, (x, y + 3 * h), (w, h), value=60,
                           value_range=(10, 360), step=10),
            ControlElement(self.screen, self._SPACE_GRAVITY_X_ELEMENT, (x, y + 4 * h), (w, h), value=0,
                           value_range=(-900, 900), step=100),
            ControlElement(self.screen, self._SPACE_GRAVITY_Y_ELEMENT, (x, y + 5 * h), (w, h), value=0,
                           value_range=(-900, 900),
                           step=100),
            ControlElement(self.screen, self._SPACE_STEP_ELEMENT, (x, y + 6 * h), (w, h), value=60,
                           value_range=(10, 180), step=10),
            ControlElement(self.screen, self._LOGO_POSITION_ELEMENT, (x, y + 7 * h), (w, h),
                           area_top_left=(0, 0), area_size=(self.width, self.height)),
        ]

    def _get_buttons(self) -> dict[str, Button]:
        return {
            self._COLOR_RANGE_STR: ColorRangeButton(
                self.screen, (0, self.height), (self._CONTROL_WIDTH + self.width, self._CONTROL_HEIGHT)),
            self._DONE_STR: Button(
                self.screen, (self._control_x, self._control_y + (20 * self._control_h)),
                (self._control_w, self._control_h), value=self._DONE_STR.upper(), color=Color.GRAY, box=True),
        }
