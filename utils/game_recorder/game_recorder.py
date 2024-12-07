import os
import shutil
import time

import pyautogui

from utils.private_parms import USER_NAME_FOLDER

_WAITING_TIME = 0.5


class GameRecorder:
    """
    Handles recording and saving of game recordings.

    This class provides functionality to record game sessions, save them to a local directory,
    and optionally manage them for upload or playback.
    """

    _SAVED_DIR = r"C:\Users\{user_name}\Videos\Captures".format(user_name=USER_NAME_FOLDER)
    _DIR = r"C:\ws\pygame_projects\utils\game_recorder\game_recordings"

    def __init__(self, game_name: str, game_number: int):
        """
        Initialize a GameRecorder instance.

        Args:
            :param game_name (str): The name of the game.
            :param game_number (int): The unique game number associated with this recording session.
        """
        self.game_name = f"{game_name} {game_number}"

    def start(self):
        """
        Start the game recording process.

        This method initializes the recording mechanism.
        """

        pyautogui.hotkey('win', 'alt', 'g')
        time.sleep(_WAITING_TIME)
        pyautogui.hotkey('win', 'alt', 'r')
        print(f"Start Recording - {self.game_name}")
        time.sleep(_WAITING_TIME * 2)

    def stop(self):
        """
        Stop the game recording process.

        This method stops the recording, finalizes the saved file, and ensures all captured data
        is properly written to disk. It cleans up any resources related to the recording process.

        The recording will be saved to the designated directory using the initialized game name and number.
        """

        time.sleep(_WAITING_TIME * 2)
        pyautogui.hotkey('win', 'alt', 'r')
        time.sleep(_WAITING_TIME)
        pyautogui.hotkey('win', 'alt', 'g')
        print(f"Stop Recording = {self.game_name}")
        self._move_file_to_target_dir()

    def _move_file_to_target_dir(self):
        files = [f for f in os.listdir(self._SAVED_DIR) if f.startswith(self.game_name) and f.endswith("mp4")]

        if len(files) == 0:
            print(f"Record of {self.game_name} Not Saved.")
            return

        file = max(files)
        saved_path = os.path.join(self._SAVED_DIR, file)
        shutil.move(saved_path, self._DIR)
        print(f"Record of {self.game_name} Saved.")
