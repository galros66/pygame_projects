from elements.boundary import Boundary
from elements.boundary_line import BoundaryLine
from elements.brick import Brick
from elements.element import Element
from elements.victory_line import VictoryLine
from games.game_base import GameBase
from utils.sounds import Sound


class SquareRaceGame(GameBase):
    GAME_NAME = "Square Race Game"
    VICTORY_LINE_STR, BOUNDARIES_STR, BOUNDARIES_LINES_STR, BRICKS_STR = "victory_line", "boundaries", "boundaries_lines", "bricks"

    def __init__(self, n: int = -1, recording: bool = True, upload: bool = True):
        """
        Initialize a SquareRaceGame instance.

        SquareRaceGame is a fast-paced racing game where players navigate
        through a square-based track, competing to reach the finish line
        while avoiding obstacles. The game supports recording gameplay
        and uploading recordings to social media platforms.

        Args:
            :param n (int, optional):
                Game number. Defaults to -1, which loads the last saved game with the same name from the
                `games_data` folder.
            :param recording (bool, optional):
                Whether to enable game recording. Defaults to True.
            :param upload (bool, optional):
                Whether to enable automatic upload to social media after the game ends. Defaults to True.
        """
        super().__init__(self.GAME_NAME, n, recording, upload)
        self._victory_line = [VictoryLine(**victory_line_data) for victory_line_data in
                              self._game_data[self.VICTORY_LINE_STR]]
        self._boundaries = [Boundary(**boundary_data) for boundary_data in self._game_data[self.BOUNDARIES_STR]]
        self._boundaries_lines = [BoundaryLine(**boundary_line_data) for boundary_line_data in
                                  self._game_data[self.BOUNDARIES_LINES_STR]]
        self._bricks = [Brick(**brick_data) for brick_data in self._game_data[self.BRICKS_STR]]
        self._space.add(*Element.items)
        self._add_victory_line_collision_handler()
        self._add_brick_collision_handler()

    def _get_players_color(self) -> list[tuple]:
        return [brick_data[self.COLOR_STR] for brick_data in self._game_data[self.BRICKS_STR]]

    def _finish_game_handler(self) -> list[bool]:
        return [brick.body.velocity == (0, 0) for brick in self._bricks]

    def _stop_game(self):
        for body in self._space.bodies: body.velocity = (0, 0)

    def _add_victory_line_collision_handler(self):
        def victory_line_collision_handler(arbiter, space, data):
            Sound.WIN.value.play()
            for body in space.bodies:
                vx, vy = body.velocity
                body.velocity = int(vx / 40.0), int(vy / 40.0)
            return False

        for brick in self._bricks:
            for victory_line_element in self._victory_line:
                handler = self._space.add_collision_handler(victory_line_element.shape.collision_type,
                                                            brick.shape.collision_type)
                handler.begin = victory_line_collision_handler

    def _add_brick_collision_handler(self):

        def brick_collision_handler(arbiter, space, data):
            Sound.HIT.value.play()
            return True

        for brick in self._bricks:
            for victory_line_element in self._victory_line:
                for shape in self._space.shapes:
                    if shape.collision_type == brick.shape.collision_type or shape.collision_type == victory_line_element.shape.collision_type: continue
                    handler = self._space.add_collision_handler(brick.shape.collision_type, shape.collision_type)
                    handler.begin = brick_collision_handler


if __name__ == '__main__':
    num = -1
    game = SquareRaceGame(n=num, recording=False, upload=False)
    game.run()
