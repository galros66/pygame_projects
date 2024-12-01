import random

from utils.colors import Color
from utils.games_generator.game_generator_base import GameGeneratorBase
import pygame


class SquareRaceGameGenerator(GameGeneratorBase):
    MODE_BORDER = "border"
    MODE_START = "start"
    MODE_END = "end"
    MODE_LOGO = "logo"

    BOUNDARIES_ELEMENTS = "boundaries"
    BOUNDARIES_LINES_ELEMENTS = "boundaries_lines"
    VICTORY_LINE_ELEMENTS = "victory_line"
    BRICKS_ELEMENTS = "bricks"

    GROUPS = {
        BOUNDARIES_ELEMENTS: 1,
        BOUNDARIES_LINES_ELEMENTS: 1,
        VICTORY_LINE_ELEMENTS: 2,
        BRICKS_ELEMENTS: 3
    }

    SIZES = {
        BRICKS_ELEMENTS: (15, 15),
    }
    def __init__(self, game_name: str = "Square Race"):
        super().__init__(game_name)
        self.boundaries = []
        self.boundaries_lines = []
        self.start_victory_line, self.end_victory_line = None, None
        self.start_position = None
        self.logo_position = None

    def generate(self):
        super().generate()
        # Grid of tiles
        tile_size = 50
        tiles = [
            [pygame.Rect(x, y, tile_size, tile_size)
             for x in range(0, self.width, tile_size)]
            for y in range(0, self.height, tile_size)
        ]

        # Game objects
        borders = []  # List of border tiles
        borders_lines = [
            [(0, 0), (self.width, 0)],
            [(0, 0), (0, self.height)],
            [(self.width, 0), (self.width, self.height)],
            [(0, self.height), (self.width, self.height)]
        ]

        modes = [self.MODE_LOGO, self.MODE_END, self.MODE_START, self.MODE_BORDER]
        mode = modes.pop()
        # Buttons
        button = pygame.Rect(self.width//2 -75 , self.height + 20, 150, 50)

        # Main loop
        running = True
        while running:
            self.screen.fill(Color.WHITE.value)
            # Draw grid
            for row in tiles:
                for tile in row:
                    color = Color.GRAY.value if tile not in borders else Color.BLUE.value
                    pygame.draw.rect(self.screen, color, tile, 0)
                    pygame.draw.rect(self.screen, Color.WHITE.value, tile, 1)

            # Draw start point
            if self.start_position:
                pygame.draw.circle(self.screen, Color.GREEN.value, self.start_position, 5)  # Draws a small green circle

            # Draw end line
            if self.end_victory_line and self.start_victory_line:
                pygame.draw.line(self.screen, Color.RED.value, self.start_victory_line, self.end_victory_line, 4)

            for line in borders_lines:
                pygame.draw.line(self.screen, Color.BLACK.value, line[0], line[1], 4)

            self._draw_logo()
            # Draw control panel
            pygame.draw.rect(self.screen, Color.WHITE.value, (0, self.height, self.width, self.control_height))
            pygame.draw.line(self.screen, Color.BLACK.value, (0, self.height), (self.width, self.height),
                             2)
            self._draw_button(button, mode)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if a button is clicked
                    if button.collidepoint(mouse_pos):
                        if mode == self.MODE_BORDER:
                            self._add_borders_lines(borders_lines, tiles, borders)
                            self._add_boundaries_data(borders, borders_lines)
                            mode = modes.pop()
                        elif mode == self.MODE_START:
                            if self.start_position:
                                self._add_bricks_data()
                                mode = modes.pop()
                        elif mode == self.MODE_END:
                            if self.end_victory_line and self.start_victory_line:
                                self._add_victory_line_data()
                                mode = modes.pop()
                        elif mode == self.MODE_LOGO:
                            self.data["logo"] = {'position': self.logo_position}
                            running = False

                    # Handle tile selection based on mode
                    if mouse_pos[1] < self.height:
                        if mode == self.MODE_BORDER:
                            for row in tiles:
                                for tile in row:
                                    if tile.collidepoint(mouse_pos):
                                        if tile in borders: borders.remove(tile)
                                        else: borders.append(tile)

                        elif mode == self.MODE_START:
                            self.start_position = mouse_pos

                        elif mode == self.MODE_END:
                            if not self.start_victory_line:
                                self.start_victory_line = mouse_pos
                            else:
                                if self.end_victory_line: self.start_victory_line = self.end_victory_line
                                a0, b0 = self.start_victory_line
                                self.end_victory_line = (a0 , mouse_pos[1]) if abs(a0 - mouse_pos[0]) < abs(b0 - mouse_pos[1]) \
                                    else (mouse_pos[0], b0)

                        elif mode == self.MODE_LOGO:
                            self.logo_position = mouse_pos


            # Update display
            pygame.display.flip()

        self._save_data()
        # Quit pygame
        pygame.quit()

    def _draw_button(self, button: pygame.Rect, mode: str):
        """Draws the buttons in the control panel."""
        # Font
        font = pygame.font.SysFont("Arial Nova", 20)

        pygame.draw.rect(self.screen, Color.GRAY.value, button)
        pygame.draw.rect(self.screen, Color.BLACK.value, button, 2)
        text = font.render(mode.capitalize(), True, Color.BLACK.value)
        text_rect = text.get_rect(center=button.center)
        self.screen.blit(text, text_rect)

    def _draw_logo(self):
        if self.logo_position:
            font = pygame.font.SysFont("Agency FB", 20)
            text = font.render("@ grr.sim.games", True, Color.BLACK.value)
            text_rect = text.get_rect(center=self.logo_position)
            self.screen.blit(text, text_rect)

    @classmethod
    def _add_borders_lines(cls, borders_lines: list[list], tiles: list[list[pygame.Rect]], borders: list[pygame.Rect]):
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                if tiles[i][j] in borders:
                    border = tiles[i][j]
                    if j + 1 < len(tiles[i]) and tiles[i][j + 1] not in borders:
                        borders_lines.append([(border.x + border.size[0], border.y),
                         (border.x + border.size[0], border.y + border.size[1])])
                    if j > 0 and tiles[i][j - 1] not in borders:
                        borders_lines.append([(border.x, border.y), (border.x, border.y + border.size[1])])
                    if i + 1 < len(tiles) and tiles[i + 1][j] not in borders:
                        borders_lines.append([(border.x, border.y + border.size[1]),
                         (border.x + border.size[0], border.y + border.size[1])])
                    if i > 0 and tiles[i - 1][j] not in borders:
                        borders_lines.append([(border.x, border.y), (border.x + border.size[0], border.y)])

    def _add_boundaries_data(self, borders: list[pygame.Rect], borders_lines: list[list]):
        for c in Color.get_all(): print(c)
        try:
            color = getattr(Color, input("Choose color: ").upper()).value
        except:
            print("Color name not found the color chosen randomly.")
            color = random.choice(Color.get_all()).value
        self.data[self.BOUNDARIES_ELEMENTS] = [
            {
                "position": (border.x + border.size[0]/2,  border.y + border.size[1]/2),
                "size": border.size,
                "group": self.GROUPS[self.BOUNDARIES_ELEMENTS],
                "color": color
            } for border in borders
        ]
        self.data[self.BOUNDARIES_LINES_ELEMENTS] = [
            {
                "a": a,
                "b": b,
                "group": self.GROUPS[self.BOUNDARIES_LINES_ELEMENTS],
            } for [a , b] in borders_lines
        ]

    @classmethod
    def _get_random_velocity(cls) -> tuple[float, float]:
        v = [i for i in range(-10, 10)]
        v.remove(0)
        vx, vy = random.choice(v), random.choice(v)
        norm = 50 / float((vx ** 2 + vy ** 2) ** 0.5)
        return vx * norm, vy * norm

    def _add_bricks_data(self):
        try:
            n_bricks = int(input("Please write the number of the playing bricks: "))
        except:
            n_bricks = 2
        colors = []
        for i in range(n_bricks):
            for c in Color.get_basic_colors(): print(c)
            try:
                colors.append(getattr(Color, input(f"Please Choose color for brick number {i + 1}").upper()).value)
            except:
                print("Color name not found the color chosen randomly.")
                colors.append(random.choice(Color.get_basic_colors()).value)
        self.data[self.BRICKS_ELEMENTS] = [
            {
                "position": self.start_position,
                "size": self.SIZES[self.BRICKS_ELEMENTS],
                "velocity": self._get_random_velocity(),
                "group": self.GROUPS[self.BRICKS_ELEMENTS] + i,
                "color": colors[i]
            } for i in range(n_bricks)
        ]


    def _add_victory_line_data(self):
        self.data[self.VICTORY_LINE_ELEMENTS] = {
            "a": self.start_victory_line,
            "b": self.end_victory_line,
            "group": self.GROUPS[self.VICTORY_LINE_ELEMENTS]
        }


if __name__ == '__main__':
    game_generator = SquareRaceGameGenerator()
    game_generator.generate()