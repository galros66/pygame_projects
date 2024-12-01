import time
from abc import ABC
import os
import json
from typing import Callable

import pygame
import pymunk
import pymunk.pygame_util

from utils.colors import Color
from utils.game_recorder.game_recorder import GameRecorder
from utils.media_uploaders.reel_uploader import ReelUploader


class GameBase(ABC):
    GAME_DATA_DIR = r"C:\ws\pygame_projects\utils\games_data"
    SCREEN_STR, CLOCK_STR, SPACE_STR, LOGO_STR = "screen", "clock", "space", "logo"
    SIZE_STR, COLOR_STR, FPS_STR, GRAVITY_STR, STEP_STR, POSITION_STR = "size", "color", "fps", "gravity", "step", "position"

    def __init__(self, name: str, n: int = -1, recording: bool = True, upload: bool = True):
        self._name = name
        snake_name = self._name.lower().replace(' ', '_')
        self._n = n if n != -1 else len([file for file in os.listdir(self.GAME_DATA_DIR) if file.startswith(snake_name)]) - 1
        file = f"{snake_name}_data_{self._n}.json"
        with open(os.path.join(self.GAME_DATA_DIR, file), "r") as f:
            self._game_data = json.load(f)

        # Initialize pygame
        pygame.init()
        pygame.mixer.init()

        # Screen dimensions and setup
        self._screen = pygame.display.set_mode(self._game_data[self.SCREEN_STR][self.SIZE_STR])
        self._screen_color = self._game_data[self.SCREEN_STR][self.COLOR_STR]
        pygame.display.set_caption(f"{self._name} {self._n}")

        # Clock for controlling frame rate
        self._clock = pygame.time.Clock()
        self._fps = self._game_data[self.CLOCK_STR][self.FPS_STR]

        # Pymunk space setup
        self._space = pymunk.Space()
        self._space.gravity = self._game_data[self.SPACE_STR][self.GRAVITY_STR]
        self._step = float(self._game_data[self.SPACE_STR][self.STEP_STR])

        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        self._logo_position = self._game_data[self.LOGO_STR][self.POSITION_STR]
        self._running = True
        self._recorder = GameRecorder(self._name, self._n) if recording else None
        self._uploader = ReelUploader(self._name, self._n, players_color=self._get_players_color()) if recording and upload else None



    def run(self):
        self._screen.fill(self._screen_color)  # Clear the screen
        if self._recorder: self._recorder.start()
        events_handler = self._events_handler()
        while self._running:
            self._screen.fill(self._screen_color)  # Clear the screen
            self._draw_logo()

            self._running = not any(self._finish_game_handler())

            for event in pygame.event.get():
                if event.type in events_handler:
                    events_handler[event.type]()

            # Step the physics simulation
            self._space.step(1 / self._step)

            # Draw everything
            self._space.debug_draw(self._draw_options)

            # Update the display
            pygame.display.flip()
            self._clock.tick(self._fps)  # Limit frame rate to 60 FPS

        # Quit the game
        if self._recorder: self._recorder.stop()
        # time.sleep(5)
        if self._uploader:
            time.sleep(30)
            self._uploader.upload()
        pygame.quit()

    def _get_players_color(self) -> list[tuple]:
        pass

    def _events_handler(self) -> dict[int, Callable[[], None]]:
        return {
            pygame.QUIT: self._quit_handler
        }

    def _finish_game_handler(self) -> list[bool]:
        pass

    def _quit_handler(self):
        self._running = False

    def _draw_logo(self):
        font = pygame.font.SysFont("Agency FB", 20)
        text = font.render("@ grr.sim.games", True, Color.BLACK.value)
        text_rect = text.get_rect(center=self._logo_position)
        self._screen.blit(text, text_rect)