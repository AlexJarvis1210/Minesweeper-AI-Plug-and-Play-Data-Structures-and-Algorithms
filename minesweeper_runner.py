import pygame
import sys
import time
from typing import Tuple, Optional, List
from MainFiles.minesweeper_game import MinesweeperGame
from MainFiles.minesweeper_ai import MinesweeperAI
from MainFiles.minesweeper_ui import MinesweeperUI


class MinesweeperRunner:
    """
    Manages the overall running of the Minesweeper game, integrating the game logic, AI, and UI.
    """

    def __init__(self, initial_game: MinesweeperGame) -> None:
        """
        Initialises the Minesweeper game with a MinesweeperGame object.

        :param initial_game: An instance of the MinesweeperGame class containing the complete game state and logic.
        """
        self.current_game = initial_game
        self.user_interface = MinesweeperUI(self.current_game)

        selected_algorithm_name = self.user_interface.search_algorithms[self.user_interface.current_algorithm_index].strip()
        selected_safe_cell_strategy = self.user_interface.safe_cell_strategies[self.user_interface.current_safe_cell_strategy_index].strip()

        self.ai_controller = MinesweeperAI(
            grid_size=self.current_game.get_grid_size(),
            search_algorithm_name=selected_algorithm_name,
            safe_cell_strategy=selected_safe_cell_strategy
        )

        self.is_ai_playing: bool = False
        self.opened_via_options_button: bool = False
        self.manual_move_mode: bool = False  # Click per turn boolean flag.
        self.saved_board_layout: Optional[List[List[bool]]] = None  # Store the saved board layout

        # Track the last corner and edge for reuse when board state is "Existing"
        self.last_corner: Optional[Tuple[int, int]] = None
        self.last_edge: Optional[Tuple[int, int]] = None

    # ---------- Game Initialisation Methods ----------

    def initialise_new_game(self) -> None:
        """
        Generates a new board and starts a fresh game.
        """
        try:
            board_size_text = self.user_interface.board_size_input['box'].get_text_content()
            mine_percentage_text = self.user_interface.mines_input['box'].get_text_content()

            if not board_size_text.isdigit() or not mine_percentage_text.isdigit():
                self.user_interface.error_message = \
                    "Please enter valid positive integers for board size and percentage of mines."
                return

            board_size: int = int(board_size_text)
            mine_percentage: int = int(mine_percentage_text)

            if board_size <= 0 or mine_percentage < 0 or mine_percentage > 100:
                self.user_interface.error_message = \
                    "Board size must be greater than zero and percentage of mines must be between 0 and 100."
                return

            total_cells = board_size * board_size
            mine_count = (mine_percentage * total_cells) // 100

            if mine_count <= 0:
                self.user_interface.error_message = "The calculated number of mines must be greater than zero."
                return

            speed_mapping = {'Click per turn': 0.5, 'Normal': 0.4, 'Fastest': 0.0001}
            selected_speed = self.user_interface.speed_options[self.user_interface.current_speed_index]
            ai_move_speed: float = speed_mapping[selected_speed]

            selected_algorithm = self.user_interface.search_algorithms[self.user_interface.current_algorithm_index]
            selected_safe_cell_strategy = self.user_interface.safe_cell_strategies[self.user_interface.current_safe_cell_strategy_index].strip()

            start_position_mapping = {
                'First cell': 'corner',
                'Centre cell': 'centre',
                'Last cell': 'last',
                'Random cell': 'random'
            }

            start_position_type_ui = self.user_interface.start_position_options[self.user_interface.current_start_position_index]
            start_position_type = start_position_mapping.get(start_position_type_ui, 'random')

            # Clear the previous saved board layout
            self.saved_board_layout = None

            self.current_game = MinesweeperGame(grid_size=board_size, mine_count=mine_count,
                                                ai_move_speed=ai_move_speed,
                                                start_position_type=start_position_type,
                                                )

            self.saved_board_layout = self.current_game.save_board_layout()

            self.ai_controller = MinesweeperAI(
                grid_size=board_size,
                search_algorithm_name=selected_algorithm,
                safe_cell_strategy=selected_safe_cell_strategy
            )
            self.user_interface.options_menu_open = False

            self.update_manual_move_mode()
            self.user_interface.game.get_screen().fill(self.user_interface.get_background_colour())

        except ValueError:
            self.user_interface.error_message = "An unexpected error occurred. Please try again."

    def initialise_existing_game(self) -> None:
        """
        Uses the previously saved board layout to start the game.
        """
        if self.saved_board_layout is None:
            self.user_interface.error_message = "No previous board layout found. Please generate a new board first."
            return

        try:
            board_size = len(self.saved_board_layout)
            speed_mapping = {'Click per turn': 0.5, 'Normal': 0.4, 'Fastest': 0.0001}
            selected_speed = self.user_interface.speed_options[self.user_interface.current_speed_index]
            ai_move_speed: float = speed_mapping[selected_speed]

            selected_algorithm = self.user_interface.search_algorithms[self.user_interface.current_algorithm_index]
            selected_safe_cell_strategy = self.user_interface.safe_cell_strategies[self.user_interface.current_safe_cell_strategy_index].strip()

            start_position_mapping = {
                'First cell': 'first',
                'Centre cell': 'centre',
                'Last cell': 'last',
                'Random cell': 'random'
            }

            start_position_type_ui = self.user_interface.start_position_options[self.user_interface.current_start_position_index]
            start_position_type = start_position_mapping.get(start_position_type_ui, 'random')

            self.current_game = MinesweeperGame(grid_size=board_size, mine_count=self.current_game.get_mine_count(),
                                                ai_move_speed=ai_move_speed,
                                                existing_board=self.saved_board_layout,
                                                start_position_type=start_position_type,
                                                )

            self.ai_controller = MinesweeperAI(
                grid_size=board_size,
                search_algorithm_name=selected_algorithm,
                safe_cell_strategy=selected_safe_cell_strategy
            )
            self.user_interface.options_menu_open = False

            self.update_manual_move_mode()
            self.user_interface.game.get_screen().fill(self.user_interface.get_background_colour())

        except ValueError:
            self.user_interface.error_message = "An unexpected error occurred. Please try again."

    # ---------- Game Control Methods ----------

    def reset_with_new_board(self) -> None:
        """
        Resets the game with a newly generated board.
        """
        self.initialise_new_game()
        self.is_ai_playing = False

    def reset_with_existing_board(self) -> None:
        """
        Resets the game using the saved board layout.
        """
        self.initialise_existing_game()
        self.is_ai_playing = False

    def process_move(self, cell_position: Tuple[int, int]) -> None:
        """
        Makes a move on the game board and updates the game state accordingly.

        :param cell_position: A tuple representing the cell coordinates for the move.
        """
        if self.current_game.is_first_move:
            # Force the first move to be at the starting position
            cell_position = self.current_game.starting_position
            self.current_game.is_first_move = False

        if cell_position:
            if self.current_game.contains_mine(cell_position):
                self.current_game.flagged_mine_positions.add(cell_position)
                self.ai_controller.mark_cell_as_mine(cell_position)
                self.current_game.flagged_mine_positions.add(cell_position)
                self.current_game.game_over = True
            else:
                adjacent_mines_count = self.current_game.count_adjacent_mines(cell_position)
                self.current_game.revealed_positions.add(cell_position)
                self.ai_controller.add_knowledge(cell_position, adjacent_mines_count)
                self.update_flagged_positions_from_ai()

    def refresh_screen(self) -> None:
        """
        Updates the screen to reflect the current game state.
        """
        self.current_game.refresh_game_screen()
        self.user_interface.draw_game_control_buttons()
        pygame.display.flip()

    def update_flagged_positions_from_ai(self) -> None:
        """
        Updates the flagged cells on the board based on the AI's knowledge of mines.
        """
        for mine_position in self.ai_controller.identified_mines:
            if mine_position not in self.current_game.flagged_mine_positions:
                self.current_game.flagged_mine_positions.add(mine_position)

    def display_options_menu(self) -> None:
        """
        Opens the options menu to allow the user to modify game settings.
        """
        self.user_interface.options_menu_open = True

        # Update the board state if the options menu was opened via the Options button
        if self.opened_via_options_button:
            # If there is a saved board layout, default to "Existing", otherwise "New"
            if self.saved_board_layout:
                self.user_interface.current_board_state = "Existing"
            else:
                self.user_interface.current_board_state = "New"

            # Update the button text accordingly
            self.user_interface.board_state_button['text'] = self.user_interface.load_font('ui_font', 28).render(
                self.user_interface.current_board_state, True, self.user_interface.get_text_colour_1()
            )
            self.user_interface.board_state_button['text_rect'] = self.user_interface.board_state_button[
                'text'].get_rect(
                center=self.user_interface.board_state_button['rect'].center
            )
        else:
            # Ensure board state is "New" when first initialized
            self.user_interface.current_board_state = "New"

        self.refresh_screen()

    def update_manual_move_mode(self) -> None:
        """
        Updates the manual_move_mode flag based on the current speed option.
        """
        selected_speed = self.user_interface.speed_options[self.user_interface.current_speed_index]
        self.manual_move_mode = (selected_speed == 'Click per turn')

    def get_game_stats(self) -> dict:
        """
        Retrieves current game statistics.

        :return: A dictionary containing the game statistics.
        """
        safe_moves_set = set(self.ai_controller.identified_safe_cells)

        return {
            "Board size": f"{self.current_game.get_grid_size()}x{self.current_game.get_grid_size()}",
            "Mines remaining": self.current_game.get_mine_count() - len(self.current_game.flagged_mine_positions),
            "Known mines": len(self.ai_controller.identified_mines),
            "Safe moves": len(safe_moves_set - self.ai_controller.moves_made)
        }

    # ---------- Main Game Loop ----------

    def execute(self) -> None:
        """
        Runs the main game loop.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.user_interface.board_size_input['box'].handle_event(event,
                                                                         self.user_interface.update_board_state_to_new)
                self.user_interface.mines_input['box'].handle_event(event,
                                                                    self.user_interface.update_board_state_to_new)

            if self.user_interface.options_menu_open:
                self.user_interface.handle_speed_button_click()
                self.user_interface.handle_search_algorithm_button_click()
                self.user_interface.handle_safe_cell_strategy_button_click()
                self.user_interface.handle_start_position_button_click()
                self.user_interface.handle_performance_stats_button_click()
                self.user_interface.handle_inference_logic_button_click()
                self.user_interface.handle_board_state_button_click()

                if self.user_interface.handle_button_click(self.user_interface.play_button):
                    if self.user_interface.get_current_board_state() == "New":
                        self.initialise_new_game()
                    else:
                        self.initialise_existing_game()
                    pygame.time.wait(200)
                    pygame.event.clear(pygame.MOUSEBUTTONDOWN)
                else:
                    self.user_interface.display_options_menu()
                continue

            board_cells = self.current_game.draw_game_board()
            restart_button_rect, ai_button_rect, options_button_rect = self.user_interface.draw_game_control_buttons()

            selected_move, ai_active, restart_requested = \
                self.user_interface.board_size_input['box'].process_user_interactions(
                    board_cells, ai_button_rect, restart_button_rect, self.current_game, self.is_ai_playing
                )

            self.is_ai_playing = ai_active

            if restart_requested or self.user_interface.handle_button_click(self.user_interface.reset_button):
                if self.saved_board_layout:
                    self.reset_with_existing_board()
                else:
                    self.reset_with_new_board()
                continue

            if self.user_interface.handle_button_click(self.user_interface.options_button):
                self.opened_via_options_button = True
                self.display_options_menu()
                continue

            if self.manual_move_mode and self.user_interface.handle_button_click(self.user_interface.start_button):
                selected_move = self.ai_controller.make_safe_move() or self.ai_controller.make_random_move()

            if self.is_ai_playing and not self.current_game.game_over:
                if not self.manual_move_mode:
                    selected_move = self.ai_controller.make_safe_move() or self.ai_controller.make_random_move()

                if not selected_move:
                    self.current_game.flagged_mine_positions = self.ai_controller.identified_mines.copy()
                    self.is_ai_playing = False

                if selected_move:
                    self.process_move(selected_move)
                    time.sleep(self.current_game.get_ai_move_speed())

            if self.user_interface.display_performance_stats:
                performance_stats = self.ai_controller.stat_generator.get_performance_stats_summary()
                game_stats = self.get_game_stats()
                self.user_interface.draw_performance_stats_panel(performance_stats, game_stats)

            if self.current_game.is_game_won():
                self.is_ai_playing = False

            pygame.display.flip()


if __name__ == "__main__":
    game_instance = MinesweeperGame()
    game_runner = MinesweeperRunner(game_instance)
    game_runner.execute()
