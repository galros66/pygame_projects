from pathlib import Path

from instagrapi import Client
import  os

from utils.colors import Color
from utils.media_uploaders.emojis import color_emoji_mapping

VIDEO_DIR = r"C:\ws\pygame_projects\utils\game_recorder\game_recordings"
USER_NAME = "grr.sim.games"
PASSWORD = "GRR663355"


class ReelUploader:
    def __init__(self, game_name: str, game_number: int = -1, text: str = None, players_color: list[tuple] = None):
        self.client = Client()
        self.client.login(USER_NAME, PASSWORD)
        self.file_prefix = game_name if game_number == -1 else f"{game_name} {game_number}"
        self.game_name = game_name
        self._title = f"🎮 {game_name.title()} 🏁"
        self._hash_tags = " #".join([
            "#game",
            f"{game_name.lower().replace(' ', '')}",
            *game_name.lower().split(' '),
            "reel",
            "animation",
            "art",
            "mathematics",
            "satisfying",
        ])
        self._text = text
        self._colors = players_color

    def upload(self):
        video_file = max([file for file in os.listdir(VIDEO_DIR) if file.startswith(self.file_prefix) and file.endswith("mp4")])
        media = self.client.clip_upload(
            Path(fr"{VIDEO_DIR}\\{video_file}"),
            self._get_caption()
        )
        print(f"Reel uploaded successfully: {media.dict()}")

    def _get_caption(self) -> str:
        texts = [self._title]
        if self._text: texts.append(self._text)
        if self._colors:
            texts[0] += "\n" + "🆚".join([emoji for color, emoji in color_emoji_mapping.items() if list(color.value) in self._colors])
        texts.append(self._hash_tags)
        return "\n".join(texts)

if __name__ == '__main__':
    uploader = ReelUploader("Square Race", players_color=[Color.PINK.value, Color.YELLOW.value])
    uploader.upload()