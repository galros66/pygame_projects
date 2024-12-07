from typing import Any

import pygame

from utils.colors import Color
from utils.games_generator.control_elements.button import Button


class TilesButton(Button):
    """
    TilesButton is responsible for creating and managing a grid of tiles on a button interface.
    It keeps track of both the boundaries and the areas of the individual tiles within the defined region.
    """

    def __init__(
            self,
            screen: Any,
            top_left: tuple[float, float],
            size: tuple[float, float],
            step: int = 50,
            tile_color: Color = Color.GRAY,
            border_color: Color = Color.BLUE
    ):
        """
        Initialize a TilesButton.

        :param screen (Any): The Pygame screen or rendering surface on which this button will be drawn.
        :param top_left (tuple[float, float]): The top-left corner coordinates of the area this button covers.
        :param size (tuple[float, float]): The width and height (dimensions) of the entire tiles grid region.
        :param step (int): The size of each individual tile (distance between each tile's boundaries). Default is 50.
        :param tile_color (Color): The default color of each tile in the grid. Default is gray.
        :param border_color (Color): The color used for tile borders. Default is blue.
        """
        super().__init__(screen=screen, top_left=top_left, size=size)
        self.tile_color = tile_color
        self.border_color = border_color
        self._step = step
        self.tiles = None
        self.border = list()
        self.border_lines = list()
        self.reset_size(top_left, size)

    def draw(self):
        for tile in self.tiles: tile.draw()
        for line in self.border_lines: pygame.draw.line(self._screen, Color.BLACK.value, line[0], line[1], 4)

    def reset_size(self, top_left: tuple[float, float], size: tuple[float, float]):
        w, h = size
        x0, y0 = top_left
        self.tiles = [
            Button(screen=self._screen, top_left=(x, y), size=(self._step, self._step), color=self.tile_color, box=True)
            for x in range(int(x0), int(x0 + w), self._step) for y in range(int(y0), int(y0 + h), self._step)
        ]
        self.border = list()
        self.border_lines = [
            [(x0, y0), (x0 + w, y0)],
            [(x0, y0), (x0, y0 + h)],
            [(x0 + w, y0), (x0 + w, y0 + h)],
            [(x0, y0 + h), (x0 + w, y0 + h)]
        ]

    def reset_color(self, tile_color: Color = None, border_color: Color = None):
        if tile_color is None and border_color is None: return
        if border_color is not None: self.border_color = border_color
        if tile_color is not None: self.tile_color = tile_color
        for tile in self.tiles:
            if tile in self.border:
                tile.color = self.border_color
            else:
                tile.color = self.tile_color

    def set_value(self, mouse_position: tuple[float, float] = None, value: Any = None):
        """
        Updates the tile boundaries or grid properties based on mouse interaction or specified value.

        If the mouse_position is provided and is within the clickable area, the tile boundaries are updated accordingly.
        Alternatively.

        :param mouse_position: The current mouse cursor position for interactive adjustments.
        :param value: A specific value used to redefine or adjust the tile boundaries.
        """
        for tile in self.tiles:
            if tile.click(mouse_position):
                if tile in self.border:
                    self.border.remove(tile)
                    tile.color = self.tile_color
                else:
                    self.border.append(tile)
                    tile.color = self.border_color
                x0, y0 = tile.rect.topleft
                w, h = tile.rect.size
                for line in [
                    [(x0, y0), (x0, y0 + h)],
                    [(x0, y0), (x0 + w, y0)],
                    [(x0 + w, y0), (x0 + w, y0 + h)],
                    [(x0, y0 + h), (x0 + w, y0 + h)]
                ]:
                    if line in self.border_lines:
                        self.border_lines.remove(line)
                    else:
                        self.border_lines.append(line)
