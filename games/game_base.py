import json
import os
import time
from abc import ABC
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
        """
        Game Base Class

        This class serves as the foundation for creating and managing game instances.

        Attributes:
            :param name: str
                The name of the game.
            :param n: int, optional
                The game number. Defaults to -1, which corresponds to the last saved game number
                in the `games_data` folder with the same game name.
            :param recording: bool, optional
                Enables game recording. If set to `True`, the game will be recorded as it runs.
            :param upload: bool, optional
                Enables automatic uploading to social media. If set to `True`, the game recording
                will be uploaded automatically to social media platforms at the end of the game.

        Note:
            - Ensure proper setup for game recording and social media integration before enabling the respective flags.
            - Game recordings will be stored locally and managed within the project directory.
        """
        self._name = name
        snake_name = self._name.lower().replace(' ', '_')
        self._n = n if n != -1 else len(
            [file for file in os.listdir(self.GAME_DATA_DIR) if file.startswith(snake_name)]) - 1
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
        self._uploader = ReelUploader(self._name, self._n,
                                      players_color=self._get_players_color()) if recording and upload else None

    def run(self):
        """
        Run the game loop.

        This method starts the main game loop, handling game logic, user interactions,
        and rendering. It ensures that the game runs continuously until the user exits
        or the game ends.

        :Responsibilities:
            - Initialize the game environment and resources.
            - Process user inputs during the game.
            - Update the game state (e.g., positions, scores, events).
            - Render the game visuals on the screen.
            - Record the game if the `recording` flag is enabled.
            - Upload the game recording to social media if the `upload` flag is enabled and the game has ended.

        Notes:
            - The game loop runs at a fixed frame rate to ensure smooth game play.
            - If `recording` is enabled, the game recording starts when the game begins and stops when it ends.
            - If `upload` is enabled, ensure the proper authentication setup for social media integration.

        Example:
            game = SomeGame(name="MyGame", recording=True, upload=True)
            game.run()
        """
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
        if self._uploader:
            self._uploader.upload()
        else:
            time.sleep(1)
        pygame.quit()

    def _get_players_color(self) -> list[tuple]:
        """
        Retrieve a list of colors for players based on an external mapping.

        This method fetches the colors associated with each player from an external mapping.
        The colors are used for rendering elements like text annotations or overlays in the
        game's recorded video, particularly when uploading the game to social media.

        Returns:
            :return: list[tuple]: A list of colors, where each color is represented as a tuple
            (e.g., RGB values or hex codes). The order of the colors corresponds to
            the player order in the game.

            Example: [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

        Usage:
            - These colors can be applied to text, player indicators, or other visual
              elements in the video recording.
            - Ensures consistent player representation across the game's visuals.
        """
        pass

    def _events_handler(self) -> dict[int, Callable[[], None]]:
        """
        Map event types to their handler functions.

        :return dict[int, Callable[[], None]]:
            A dictionary where keys are event type identifiers
            (int), and values are functions that handle those events. Each function takes
            no arguments and performs the required actions.
        """
        return {
            pygame.QUIT: self._quit_handler
        }

    def _finish_game_handler(self) -> list[bool]:
        """
        Check conditions for finishing the game.

        :return list[bool]:
            A list of boolean values, where each element represents whether
            a specific condition for finishing the game is met. The game is considered
            finished if all values in the list are True.
        """
        pass

    def _quit_handler(self):
        self._running = False

    def _draw_logo(self):
        font = pygame.font.SysFont("Agency FB", 20)
        text = font.render("@ grr.sim.games", True, Color.BLACK.value)
        text_rect = text.get_rect(center=self._logo_position)
        self._screen.blit(text, text_rect)
