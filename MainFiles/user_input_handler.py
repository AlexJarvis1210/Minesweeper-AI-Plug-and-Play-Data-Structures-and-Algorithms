import pygame
import time
from typing import Tuple, List, Optional


class UserInputHandler:
    """
    Handles user input for the Minesweeper game, including text input fields and interaction with UI elements.
    """

    def __init__(self, x_position: int, y_position: int, width: int, height: int, initial_text: str = '',
                 default: Optional[int] = None) -> None:
        """
        Initialise the UserInputHandler class with a text input field.

        :param x_position: The X coordinate of the input box.
        :param y_position: The Y coordinate of the input box.
        :param width: The width of the input box.
        :param height: The height of the input box.
        :param initial_text: The initial text to display in the input box.
        :param default: An optional default value for the input box.
        """
        self.input_box_rect: pygame.Rect = pygame.Rect(x_position, y_position, width, height)
        self.box_colour: pygame.Color = pygame.Color('white')

        self.text_content: str = str(default) if default is not None else initial_text

        self.input_font: pygame.font.Font = pygame.font.Font(None, 36)
        self.rendered_text_surface: pygame.Surface = self.input_font.render(self.text_content, True, self.box_colour)
        self.is_active: bool = False

    def handle_event(self, event: pygame.event.Event, update_board_state_func: Optional[callable] = None) -> None:
        """
        Handle input events for the text box, including mouse clicks and key presses.

        :param event: The event to handle.
        :param update_board_state_func: Optional callable to update board state in the UI.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event)
        elif event.type == pygame.KEYDOWN and self.is_active:
            self._handle_key_press(event, update_board_state_func)

    def _handle_mouse_click(self, event: pygame.event.Event) -> None:
        """
        Handle mouse click events for activating/deactivating the input box.

        :param event: The mouse event to handle.
        """
        if self.input_box_rect.collidepoint(event.pos):
            self.is_active = not self.is_active
        else:
            self.is_active = False
        self.box_colour = pygame.Color((230, 135, 60)) if self.is_active else pygame.Color('white')

    def _handle_key_press(self, event: pygame.event.Event, update_board_state_func: Optional[callable]) -> None:
        """
        Handle key press events for text input.

        :param event: The key event to handle.
        :param update_board_state_func: Optional callable to update board state in the UI.
        """
        if event.key == pygame.K_RETURN:
            self.is_active = False
            self.box_colour = pygame.Color('white')
        elif event.key == pygame.K_BACKSPACE:
            self.text_content = self.text_content[:-1]
        else:
            self.text_content += event.unicode
        self.rendered_text_surface = self.input_font.render(self.text_content, True, self.box_colour)

        if update_board_state_func:
            update_board_state_func()

    def draw_input_box(self, screen: pygame.Surface) -> None:
        """
        Draw the input box and the text on the screen.

        :param screen: The screen surface to draw on.
        """
        text_rect = self.rendered_text_surface.get_rect(center=self.input_box_rect.center)
        screen.blit(self.rendered_text_surface, text_rect)
        pygame.draw.rect(screen, self.box_colour, self.input_box_rect, 2)

    def get_text_content(self) -> str:
        """
        Return the current text in the input box.

        :return: The current text.
        """
        return self.text_content

    def process_user_interactions(
        self,
        game_board_cells: List[List[pygame.Rect]],
        ai_button_rect: pygame.Rect,
        reset_button_rect: pygame.Rect,
        game_instance,
        is_ai_active: bool
    ) -> Tuple[Optional[Tuple[int, int]], bool, bool]:
        """
        Handle user interactions with the game board and UI buttons.

        :param game_board_cells: A 2D list of rects representing the game board cells.
        :param ai_button_rect: The rect for the AI move button.
        :param reset_button_rect: The rect for the reset button.
        :param game_instance: The game instance to interact with.
        :param is_ai_active: Whether the AI is currently playing.
        :return: A tuple containing the user's move, the updated AI playing status, and whether a reset was requested.
        """
        selected_cell: Optional[Tuple[int, int]] = None
        reset_requested: bool = False
        left_click, _, _ = pygame.mouse.get_pressed()

        if left_click == 1:
            mouse_position = pygame.mouse.get_pos()
            selected_cell, is_ai_active, reset_requested = self._handle_mouse_interaction(
                mouse_position, game_board_cells, ai_button_rect, reset_button_rect, game_instance, is_ai_active
            )

        return selected_cell, is_ai_active, reset_requested

    def _handle_mouse_interaction(
        self,
        mouse_position: Tuple[int, int],
        game_board_cells: List[List[pygame.Rect]],
        ai_button_rect: pygame.Rect,
        reset_button_rect: pygame.Rect,
        game_instance,
        is_ai_active: bool
    ) -> Tuple[Optional[Tuple[int, int]], bool, bool]:
        """
        Handle mouse interactions on the game board and buttons.

        :param mouse_position: The current mouse position.
        :param game_board_cells: A 2D list of rects representing the game board cells.
        :param ai_button_rect: The rect for the AI move button.
        :param reset_button_rect: The rect for the reset button.
        :param game_instance: The game instance to interact with.
        :param is_ai_active: Whether the AI is currently playing.
        :return: A tuple containing the user's move, the updated AI playing status, and whether a reset was requested.
        """
        selected_cell: Optional[Tuple[int, int]] = None
        reset_requested: bool = False

        if ai_button_rect.collidepoint(mouse_position) and not game_instance.game_over:
            time.sleep(0.5)
            is_ai_active = True  # Start AI play-through mode

        elif reset_button_rect.collidepoint(mouse_position):
            reset_requested = True

        elif not game_instance.game_over:
            for row_index in range(game_instance.get_grid_size()):
                for col_index in range(game_instance.get_grid_size()):
                    cell = (row_index, col_index)
                    if (
                        game_board_cells[row_index][col_index].collidepoint(mouse_position) and
                        cell not in game_instance.flagged_mine_positions and
                        cell not in game_instance.revealed_positions
                    ):
                        selected_cell = cell

        return selected_cell, is_ai_active, reset_requested
