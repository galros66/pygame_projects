import os
import shutil
import time

import pyautogui

from utils.private_parms import USER_NAME_FOLDER

_WAITING_TIME = 0.5


class GameRecorder:
    _SAVED_DIR = r"C:\Users\{user_name}\Videos\Captures".format(user_name=USER_NAME_FOLDER)
    _DIR = r"C:\ws\pygame_projects\utils\game_recorder\game_recordings"

    def __init__(self, game_name: str, game_number: int):
        self.game_name = f"{game_name} {game_number}"

    def start(self):
        pyautogui.hotkey('win', 'alt', 'g')
        time.sleep(_WAITING_TIME)
        pyautogui.hotkey('win', 'alt', 'r')
        print(f"Start Recording - {self.game_name}")
        time.sleep(_WAITING_TIME * 2)

    def stop(self):
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
