import pygame
import random
from typing import Set, Tuple, List, Optional


class MinesweeperGame:
    def __init__(self, grid_size: int = 50, mine_count: int = 15, ai_move_speed: float = 0.005,
                 existing_board: Optional[List[List[bool]]] = None, start_position_type: str = 'centre',
                 ) -> None:
        """
        Initialise the game with the given parameters.

        :param grid_size: The size of the game grid (default is 50x50).
        :param mine_count: The number of mines on the board (default is 15).
        :param ai_move_speed: The speed of the AI moves and reveal animations (default is 0.005).
        :param existing_board: An optional existing board layout to use instead of generating a new one.
        :param start_position_type: The type of starting position ('first', 'centre', 'last', 'random').

        """
        pygame.init()
        pygame.font.init()
        self._grid_size: int = grid_size
        self._mine_count: int = mine_count
        self._ai_move_speed: float = ai_move_speed
        self.is_first_move: bool = True
        self.start_position_type = start_position_type

        self.board: List[List[bool]] = existing_board if existing_board else \
            [[False for _ in range(self._grid_size)] for _ in range(self._grid_size)]
        self.mine_positions: Set[Tuple[int, int]] = set()
        self.revealed_positions: Set[Tuple[int, int]] = set()
        self.starting_position = self._determine_starting_position()
        self.revealed_positions.add(self.starting_position)

        self.flagged_mine_positions: Set[Tuple[int, int]] = set()
        self.game_over: bool = False

        if not existing_board:
            self._randomly_place_mines()
        else:
            self._load_existing_mines()

        # Colours
        self._font_colour: Tuple[int, int, int] = (255, 255, 255)  # white
        self._cell_colour: Tuple[int, int, int] = (34, 86, 117)
        self._border_colour: Tuple[int, int, int] = (230, 135, 60)
        self._background_colour: Tuple[int, int, int] = (34, 86, 117)

        # Board font:
        font_path: str = "MainFiles/assets/fonts/Cronus_Round.otf"
        self._small_font: pygame.font.Font = pygame.font.Font(font_path, 20)
        self._medium_font: pygame.font.Font = pygame.font.Font(font_path, 28)
        self._large_font: pygame.font.Font = pygame.font.Font(font_path, 40)

        # Pygame setup
        self._screen_size = self._screen_width, self._screen_height = 1920, 1080
        self._screen: pygame.Surface = pygame.display.set_mode(self._screen_size)

        # Compute game box size (2/3 of screen width, full height)
        self._game_box_width: int = int(self._screen_width * 2 / 3)
        self._game_box_height: int = self._screen_height

        # Compute board size and positioning
        self._calculate_board_dimensions()

        # Load images
        self._load_and_scale_images()

    def _randomly_place_mines(self) -> None:
        """Randomly places mines on the board. Will not place a mine at the starting cell position"""
        while len(self.mine_positions) < self._mine_count:
            row: int = random.randrange(self._grid_size)
            col: int = random.randrange(self._grid_size)
            if (row, col) != self.starting_position and not self.board[row][col]:
                self.mine_positions.add((row, col))
                self.board[row][col] = True

    def _load_existing_mines(self) -> None:
        """Loads mine positions from the existing board layout."""
        for row in range(self._grid_size):
            for col in range(self._grid_size):
                if self.board[row][col]:
                    self.mine_positions.add((row, col))

    def save_board_layout(self) -> List[List[bool]]:
        """
        Save the current board layout.

        :return: A 2D list representing the board layout with mines.
        """
        return [row.copy() for row in self.board]

    def _determine_starting_position(self) -> Tuple[int, int]:
        """Determine the starting position based on the selected type."""
        if self.start_position_type.lower() == 'first':
            return 0, 0

        if self.start_position_type.lower() == 'centre':
            return self._grid_size // 2, self._grid_size // 2

        if self.start_position_type.lower() == 'last':
            return self._grid_size - 1, self._grid_size - 1

        return self._get_random_safe_position()

    def _get_random_safe_position(self) -> Tuple[int, int]:
        """Find a random position on the board that is not a mine."""
        while True:
            row = random.randrange(self._grid_size)
            col = random.randrange(self._grid_size)
            if not self.board[row][col]:
                return row, col

    def contains_mine(self, cell_position: Tuple[int, int]) -> bool:
        """
        Determine if the given cell contains a mine.

        :param cell_position: Tuple representing the cell coordinates.
        :return: True if the cell contains a mine, False otherwise.
        """
        row, col = cell_position
        return self.board[row][col]

    def count_adjacent_mines(self, cell_position: Tuple[int, int]) -> int:
        """
        Count the number of mines adjacent to the given cell.

        :param cell_position: Tuple representing the cell coordinates.
        :return: The number of adjacent mines.
        """
        adjacent_mines: int = 0
        for row in range(max(0, cell_position[0] - 1), min(self._grid_size, cell_position[0] + 2)):
            for col in range(max(0, cell_position[1] - 1), min(self._grid_size, cell_position[1] + 2)):
                if (row, col) != cell_position and self.board[row][col]:
                    adjacent_mines += 1
        return adjacent_mines

    def is_game_won(self) -> bool:
        """Check if the game is won."""
        all_safe_cells_revealed = len(self.revealed_positions) == (self._grid_size * self._grid_size - self._mine_count)
        return self.flagged_mine_positions == self.mine_positions and all_safe_cells_revealed

    def _calculate_board_dimensions(self) -> None:
        """Compute the size of the cells and their positions on the screen."""
        self._board_padding: int = 20
        board_width: int = self._game_box_width - (self._board_padding * 2)
        board_height: int = self._game_box_height - (self._board_padding * 2)

        self._cell_size: int = int(min(board_width / self._grid_size, board_height / self._grid_size))

        self._board_origin_x: int = (self._game_box_width - (self._cell_size * self._grid_size)) // 2
        self._board_origin_y: int = (self._game_box_height - (self._cell_size * self._grid_size)) // 2
        # Dynamic font size based on cell size
        font_size: int = max(12, int(self._cell_size * 0.8))
        self._small_font: pygame.font.Font = pygame.font.Font("MainFiles/assets/fonts/Cronus_Round.otf", font_size)

    def _load_and_scale_images(self) -> None:
        """Load and scale the images for flags and mines."""
        self._flag_image: pygame.Surface = pygame.image.load("MainFiles/assets/images/flag.png")
        self._flag_image = pygame.transform.scale(self._flag_image, (self._cell_size // 2, self._cell_size // 2))
        self._mine_image: pygame.Surface = pygame.image.load("MainFiles/assets/images/mine.png")
        self._mine_image = pygame.transform.scale(self._mine_image, (self._cell_size // 2, self._cell_size // 2))

    def draw_game_board(self) -> List[List[pygame.Rect]]:
        """
        Draw the game board on the screen.

        :return: A 2D list of pygame.Rect objects representing the cells.
        """
        cell_rectangles: List[List[pygame.Rect]] = []
        for row in range(self._grid_size):
            row_rects: List[pygame.Rect] = []
            for col in range(self._grid_size):
                cell_rect = pygame.Rect(
                    self._board_origin_x + col * self._cell_size,
                    self._board_origin_y + row * self._cell_size,
                    self._cell_size, self._cell_size
                )
                pygame.draw.rect(self._screen, self._cell_colour, cell_rect)
                pygame.draw.rect(self._screen, self._border_colour, cell_rect, 3)

                image_x: int = cell_rect.x + (self._cell_size - self._flag_image.get_width()) // 2
                image_y: int = cell_rect.y + (self._cell_size - self._flag_image.get_height()) // 2

                if self.contains_mine((row, col)) and self.game_over:
                    self._screen.blit(self._mine_image, (image_x, image_y))
                elif (row, col) in self.flagged_mine_positions:
                    self._screen.blit(self._flag_image, (image_x, image_y))
                elif (row, col) in self.revealed_positions:
                    adjacent_mines_text = self._small_font.render(
                        str(self.count_adjacent_mines((row, col))),
                        True, self._font_colour
                    )
                    text_rect = adjacent_mines_text.get_rect()
                    text_rect.center = cell_rect.center
                    self._screen.blit(adjacent_mines_text, text_rect)

                row_rects.append(cell_rect)
            cell_rectangles.append(row_rects)
        return cell_rectangles

    def refresh_game_screen(self) -> None:
        """Fill the screen with the background colour and redraw the board."""
        self._screen.fill(self._background_colour)
        self.draw_game_board()
        pygame.display.flip()

    # Getter methods
    def get_grid_size(self) -> int:
        """Return the grid size of the game."""
        return self._grid_size

    def get_mine_count(self) -> int:
        """Return the number of mines on the board."""
        return self._mine_count

    def get_ai_move_speed(self) -> float:
        """Return the AI move speed."""
        return self._ai_move_speed

    def get_screen(self) -> pygame.Surface:
        """Return the Pygame screen surface."""
        return self._screen

    def get_screen_width(self) -> int:
        """Return the width of the screen."""
        return self._screen_width
