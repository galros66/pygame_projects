import json
import os

import pygame

from utils.colors import Color


class GameGeneratorBase:
    DIR = r"C:\ws\pygame_projects\utils\games_data"
    control_height = 100

    def __init__(self, game_name: str):
        self.game_name = game_name

        self.screen = None
        self.screen_size = self.width, self.height = 400, 600
        self.screen_color: tuple[int, int, int, int] = Color.GRAY.value

        self.clock_fps = 60

        self.space_gravity = 0, 0
        self.space_step = 60.0
        self.data = dict()

    def generate(self):
        ans = input("Starting generate game. If You want the default game parameters tab - D: ")
        if ans.upper() != "D":
            try:
                self.screen_size = self.width, self.height = int(input("Width: ")), int(input("height: "))
            except:
                print(f"Invalid input. Screen size set by default to be {self.screen_size}.")
        self._add_general_data()
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height + self.control_height))
        pygame.display.set_caption(f"Interactive Game {self.game_name} Setup with Control Panel")

    def _add_general_data(self):
        self.data |= {
            "screen": {"size": self.screen_size, "color": self.screen_color},
            "clock": {"fps": self.clock_fps},
            "space": {"gravity": self.space_gravity, "step": self.space_step}
        }

    def _save_data(self):
        snack_name = self.game_name.lower().replace(' ', '_')
        n = len([f for f in os.listdir(self.DIR) if f.startswith(snack_name)])
        file = f"{snack_name}_game_data_{n}.json"
        with open(os.path.join(self.DIR, file), "w") as f:
            json.dump(self.data, f, indent=4)
        print(f"{self.game_name} Game data saved successfully!")
