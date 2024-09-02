import pygame
from typing import List, Tuple
from .user_input_handler import UserInputHandler


class MinesweeperUI:
    """
    Handles the user interface elements of the Minesweeper game, including buttons, labels, and input boxes.
    """

    def __init__(self, game) -> None:
        """
        Initialises the UI with the given game instance.

        :param game: The game instance to interact with.
        """

        self.game = game
        self.error_message: str = ""
        self.options_menu_open: bool = True
        self.current_board_state = 'New'  # Default state

        self.fonts = {
            "main_font": "MainFiles/assets/fonts/junegull/junegull rg.otf",
            "ui_font": "MainFiles/assets/fonts/Cronus_Round.otf"
        }

        # Colours
        self._background_colour: Tuple[int, int, int] = (34, 86, 117)
        self._text_colour_1: Tuple[int, int, int] = (255, 255, 255)
        self._button_colour: Tuple[int, int, int] = (230, 135, 60)  # orange

        # Button dimensions
        button_width = 350
        button_height = 50
        vertical_spacing = 10

        # Calculate x position to center buttons and align input boxes
        center_x = (self.game.get_screen_width() // 2) - (button_width // 2)

        # Add the game control buttons (Restart, AI Move, Options)
        top_right_x: int = self.game.get_screen_width() - 430
        top_right_y: int = 20

        self.reset_button = self.create_button(
            'Reset',
            top_right_x,
            top_right_y,
            'ui_font',
            28,
            self._text_colour_1,
            150
        )

        self.start_button = self.create_button(
            'Start',
            top_right_x + 160,
            top_right_y,
            'ui_font',
            28,
            self._text_colour_1,
            150
        )

        self.options_button = self.create_button(
            'Options',
            top_right_x - 160,
            top_right_y,
            'ui_font',
            28,
            self._text_colour_1,
            150
        )

        # Input boxes
        input_box_width = 250
        input_box_height = button_height

        # Align the input boxes to the right-hand side of the buttons
        input_box_start_y = 240

        self.board_size_input = self.create_input_box(
            input_box_start_y,
            'Board Size:',
            text=str(self.game.get_grid_size()),
            default=50,
            width=input_box_width,
            height=input_box_height,
            font_name='ui_font',
            font_size=20,
            font_colour=self._text_colour_1
        )

        self.mines_input = self.create_input_box(
            input_box_start_y + input_box_height + vertical_spacing,
            'Percentage of Mines (%):',
            text='20',
            default=15,
            width=input_box_width,
            height=input_box_height,
            font_name='ui_font',
            font_size=20,
            font_colour=self._text_colour_1
        )

        # Game speed button
        self.speed_button = self.create_button(
            'Fastest',
            center_x,
            input_box_start_y + 2 * (input_box_height + vertical_spacing),
            'ui_font',
            28,
            self._text_colour_1
        )
        self.speed_options: List[str] = ['Click per turn', 'Normal', 'Fastest']
        self.current_speed_index: int = 2  # Default to max speed

        # Search algorithm button
        self.search_algorithm_button = self.create_button(
            'Brute Force',
            center_x,
            input_box_start_y + 3 * (input_box_height + vertical_spacing),
            'ui_font',
            28,
            self._text_colour_1
        )
        self.safe_cell_strategy_button = self.create_button(
            'First In, First Out',  # Default strategy
            center_x,
            input_box_start_y + 4 * (input_box_height + vertical_spacing),
            'ui_font',
            28,
            self._text_colour_1
        )

        self.safe_cell_strategies: List[str] = ['First In, First Out', 'Last In, First Out', 'Sorted by position', 'Random']
        self.current_safe_cell_strategy_index: int = 0  # Default to FIFO
        self.start_position_options = ['Random cell', 'First cell', 'Centre cell', 'Last cell']
        self.current_start_position_index: int = 0  # Default to Random

        # Create the Start Position button
        self.start_position_button = self.create_button(
            self.start_position_options[self.current_start_position_index],
            center_x,
            input_box_start_y + 8 * (input_box_height + vertical_spacing),  # Position below other options
            'ui_font',
            28,
            self._text_colour_1
        )
        # Performance stats button
        self.performance_stats_button = self.create_button(
            'On',
            center_x,
            input_box_start_y + 4 * (input_box_height + vertical_spacing),
            'ui_font',
            28,
            self._text_colour_1
        )

        # Inference logic button
        self.inference_logic_button = self.create_button(
            'Off',
            center_x,
            input_box_start_y + 5 * (input_box_height + vertical_spacing),
            'ui_font',
            28,
            self._text_colour_1
        )

        self.game_stats_button = self.create_button(
            'On',  # Default state is "On"
            center_x,
            input_box_start_y + 4 * (input_box_height + vertical_spacing),  # Position appropriately
            'ui_font',
            28,
            self._text_colour_1
        )

        # Board state toggle button (New/Existing)
        self.board_state_button = self.create_button(
            'New',
            center_x,
            input_box_start_y + 6 * (input_box_height + vertical_spacing),
            'ui_font',
            28,
            self._text_colour_1
        )

        # Play game button
        self.play_button = self.create_button(
            'Play Game',
            center_x,
            input_box_start_y + 7 * (input_box_height + vertical_spacing),
            'ui_font',
            28,
            self._text_colour_1,
        )

        # Adjust the error message label position to be below the Play Game button and centered
        play_button_rect = self.play_button['rect']
        error_label_y_position = play_button_rect.bottom + 20

        self.error_message_label = self.create_label(
            "",
            error_label_y_position,
            'ui_font',
            28,
            self._text_colour_1
        )

        self.error_message_label[1].centerx = self.game.get_screen_width() // 2

        # Default settings for stats and logic options
        self.display_game_stats = True
        self.display_performance_stats = True
        self.display_inference_logic = False

        # Search algorithm information
        self.search_algorithms = ['divide_and_conquer', 'dynamic_programming', 'brute_force',
                                  'greedy_algorithm_size', 'greedy_algorithm_minecount', 'bfs', 'dfs']
        # Default to Brute Force
        self.current_algorithm_index = 2
        self.current_search_algorithm_name: str = self.search_algorithms[self.current_algorithm_index]

        self.search_algorithm_display_names = {
            'divide_and_conquer': 'Divide and Conquer',
            'dynamic_programming': 'Dynamic Programming',
            'brute_force': 'Brute Force',
            'greedy_algorithm_size': 'Greedy by Size',
            'greedy_algorithm_minecount': 'Greedy by Mine count',
            'bfs': 'BFS',
            'dfs': 'DFS'
        }

        self.safe_cell_strategy_display_names = {
            'First In, First Out': 'FIFO',
            'Last In, First Out': 'LIFO',
            'Sorted by position': 'Sorted',
            'Random': 'Random'
        }

        self.start_position_display_names = {
            'First cell': 'corner',
            'Centre cell': 'centre',
            'Last cell': 'last',
            'Random cell': 'random'
        }

    def force_redraw_buttons(self) -> None:
        """
        Forces redraw of the text on buttons.
        Fixes a bug where the button text is misaligned on startup
        """
        buttons = [
            self.speed_button,
            self.search_algorithm_button,
            self.safe_cell_strategy_button,
            self.performance_stats_button,
            self.start_position_button,
            self.inference_logic_button,
            self.board_state_button,
            self.play_button
        ]
        for button in buttons:
            button['text_rect'] = button['text'].get_rect(center=button['rect'].center)
            self.draw_button(button)

    def load_font(self, font_name: str, font_size: int) -> pygame.font.Font:
        """
        Loads a font with the specified name and size.
        :param font_name: The key to identify the font path.
        :param font_size: The size of the font to load.
        :return: A pygame Font object.
        """
        font_path = self.fonts.get(font_name, self.fonts['main_font'])
        return pygame.font.Font(font_path, font_size)

    def create_button(self, text: str, x_position: int, y_position: int, font_name: str, font_size: int,
                      font_colour: Tuple[int, int, int], width: int = 250, height: int = 50,
                      button_colour: Tuple[int, int, int] = (55, 55, 55)) -> dict:
        """
        Creates a button with the specified parameters.
        :param text: The text displayed on the button.
        :param x_position: The X coordinate of the button's position.
        :param y_position: The Y coordinate of the button's position.
        :param font_name: The name of the font to use.
        :param font_size: The size of the font.
        :param font_colour: The color of the font.
        :param width: The width of the button.
        :param height: The height of the button.
        :param button_colour: The background color of the button.
        :return: A dictionary representing the button's properties.
        """
        button_rect = pygame.Rect(x_position, y_position, width, height)
        button_text = self.load_font(font_name, font_size).render(text, True, font_colour)

        # Calculate text_rect to ensure it is centered within the button_rect
        button_text_rect = button_text.get_rect(center=button_rect.center)

        return {
            "rect": button_rect,
            "text": button_text,
            "text_rect": button_text_rect,
            "button_colour": button_colour,
            "state": text,  # Store the initial state (text) of the button here
            "action": None  # Placeholder for future button action if needed
        }

    def create_label(self, text: str, y_position: int, font_name: str, font_size: int,
                     font_colour: Tuple[int, int, int], input_box_height: int = None) -> Tuple[
        pygame.Surface, pygame.Rect]:
        """
        Creates a label with the specified parameters.
        :param text: The text displayed on the label.
        :param y_position: The Y coordinate of the label's position.
        :param font_name: The name of the font to use.
        :param font_size: The size of the font.
        :param font_colour: The color of the font.
        :param input_box_height: The height of the input box to align the label with (optional).
        :return: A tuple containing the label surface and its rect.
        """
        font = self.load_font(font_name, font_size)
        label = font.render(text, True, font_colour)
        label_rect = label.get_rect()

        if input_box_height is not None:
            # Align the label's center vertically with the middle of the input box
            label_rect.centery = y_position + (input_box_height // 2)
        else:
            # Position the label based on the provided y_position
            label_rect.topleft = ((self.game.get_screen_width() // 2) - 150, y_position)

        return label, label_rect

    def create_input_box(self, y_position: int, label_text: str = '', text: str = '', default: int = 0,
                         width: int = 140, height: int = 32, font_name: str = 'ui_font', font_size: int = 20,
                         font_colour: Tuple[int, int, int] = (255, 255, 255)) -> dict:
        """
        Creates an input box with the specified parameters.
        :param y_position: The Y coordinate of the input box's position.
        :param label_text: The text displayed next to the input box.
        :param text: The default text inside the input box.
        :param default: The default value for the input box.
        :param width: The width of the input box (default is 140).
        :param height: The height of the input box (default is 32).
        :param font_name: The name of the font to use for the label.
        :param font_size: The font size for the label.
        :param font_colour: The font color for the label.
        :return: A dictionary representing the input box and its label.
        """
        # Positioning label to the left of the input box
        label_x_position = (
                                       self.game.get_screen_width() // 2) - width - 50  # Adjust to position the label relative to the input box
        label, label_rect = self.create_label(
            label_text, y_position, font_name, font_size, font_colour
        )
        label_rect.x = label_x_position  # Set label x position

        # Positioning the input box right next to the label
        input_x_position: int = label_rect.right + 10  # Adjust as necessary to position it next to the label
        input_box = UserInputHandler(input_x_position, y_position, width, height, text)

        return {
            "label": label,
            "label_rect": label_rect,
            "box": input_box
        }

    def draw_button(self, button: dict) -> None:
        """
        Draws a button on the screen.

        :param button: The dictionary representing the button's properties.
        """
        self.draw_rounded_rect(self.game.get_screen(), self._button_colour, button['rect'], radius=0.3)
        self.game.get_screen().blit(button['text'], button['text_rect'])

    def draw_rounded_rect(self, surface, color, rect, radius=0.4):
        """
        Draw a rectangle with rounded corners.
        :param surface: The surface to draw the rectangle on.
        :param color: The color of the rectangle.
        :param rect: The rectangle (pygame.Rect or tuple).
        :param radius: The radius of the corners as a float or an int.
        :return: The rounded rectangle surface.
        """
        rect = pygame.Rect(rect)
        corner_radius = min(rect.width, rect.height) * radius  # Adjust the corner radius

        # Create the rectangle with rounded corners
        rounded_rect_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(rounded_rect_surface, color, rounded_rect_surface.get_rect(), border_radius=int(corner_radius))

        # Blit the rounded rectangle onto the target surface
        surface.blit(rounded_rect_surface, rect.topleft)

    def draw_game_control_buttons(self) -> Tuple[pygame.Rect, pygame.Rect, pygame.Rect]:
        """
        Draws the game control buttons (AI Move, Options, Restart) on the screen.

        :return: A tuple of pygame.Rect objects for each button's rect.
        """
        self.draw_button(self.reset_button)
        self.draw_button(self.start_button)
        self.draw_button(self.options_button)

        return self.reset_button['rect'], self.start_button['rect'], self.options_button['rect']

    def draw_label(self, label: pygame.Surface, label_rect: pygame.Rect) -> None:
        """
        Draws a label on the screen.

        :param label: The label surface to draw.
        :param label_rect: The rect specifying the label's position.
        """
        self.game.get_screen().blit(label, label_rect)

    def draw_input_box_with_label(self, input_box: dict) -> None:
        """
        Draws an input box with its label on the screen.

        :param input_box: The dictionary representing the input box and its label.
        """
        self.draw_label(input_box['label'], input_box['label_rect'])
        input_box['box'].draw_input_box(self.game.get_screen())  # Updated method name

    def handle_button_click(self, button: dict) -> bool:
        """
        Handles the button click event.

        :param button: The dictionary representing the button's properties.
        :return: True if the button is clicked, False otherwise.
        """
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse_position = pygame.mouse.get_pos()
            if button['rect'].collidepoint(mouse_position):
                return True
        return False

    def handle_search_algorithm_button_click(self) -> None:
        """
                Handles the click event for the 'Search Algorithm' button.

                Cycles through the available search algorithm options.
                """
        if self.handle_button_click(self.search_algorithm_button):
            # Update the current algorithm index and name
            self.current_algorithm_index = (self.current_algorithm_index + 1) % len(self.search_algorithms)
            self.current_search_algorithm_name = self.search_algorithms[self.current_algorithm_index]

            # Debugging print statement
            print(f"Algorithm changed to: {self.current_search_algorithm_name} (Index: {self.current_algorithm_index})")

            # Update the button text to display the new algorithm name
            self.search_algorithm_button['text'] = self.load_font('ui_font', 28).render(
                self.search_algorithm_display_names[self.search_algorithms[self.current_algorithm_index]], True,
                self._text_colour_1
            )
            self.search_algorithm_button['text_rect'] = self.search_algorithm_button['text'].get_rect(
                center=self.search_algorithm_button['rect'].center
            )
            pygame.time.wait(200)  # Add a delay to avoid rapid cycling

    def handle_start_position_button_click(self) -> None:
        """
        Handles the click event for the 'Start Position' button.

        Cycles through the available start position options.
        """
        if self.handle_button_click(self.start_position_button):
            # Cycle through the start position options
            self.current_start_position_index = (self.current_start_position_index + 1) % len(
                self.start_position_options)
            current_position_name = self.start_position_options[self.current_start_position_index]

            # Update the button text to display the new start position name
            self.start_position_button['text'] = self.load_font('ui_font', 28).render(
                current_position_name, True, self._text_colour_1
            )
            self.start_position_button['text_rect'] = self.start_position_button['text'].get_rect(
                center=self.start_position_button['rect'].center
            )
            pygame.time.wait(200)  # Add a delay to avoid rapid cycling

    def build_2_col_table(self, start_x: int, start_y: int, rows: List[Tuple[str, any]],
                          col_widths: Tuple[int, int], row_height: int = 30, font_size: int = 20) -> List[dict]:
        """
        Builds a 2-column table at the specified location with the given rows and column widths.

        :param start_x: The starting X coordinate for the table.
        :param start_y: The starting Y coordinate for the table.
        :param rows: A list of tuples where each tuple contains (description, value) pairs. Value can be a string or a Pygame surface.
        :param col_widths: A tuple specifying the width of the first column (description) and the second column (value).
        :param row_height: The height of each row in the table.
        :param font_size: The font size to be used in the table.
        :return: A list of dictionaries where each dictionary contains the surfaces and rects for a table row.
        """
        table_rows = []
        font = self.load_font('ui_font', font_size)

        for index, (description, value) in enumerate(rows):
            y_position = start_y + index * row_height

            description_surf = font.render(description, True, self._text_colour_1)
            description_rect = pygame.Rect(start_x + 10, y_position, col_widths[0], row_height)
            description_rect.centery = y_position + (row_height // 2)

            # Handle different types of values
            if isinstance(value, pygame.Surface):
                value_surf = value
                value_rect = value.get_rect(midleft=(start_x + col_widths[0] + 10, y_position + (row_height // 2)))
            else:
                value_surf = font.render(str(value), True, self._text_colour_1)
                value_rect = pygame.Rect(start_x + col_widths[0], y_position, col_widths[1], row_height)
                value_rect.centery = y_position + (row_height // 2)

            table_rows.append({
                "description_surf": description_surf,
                "description_rect": description_rect,
                "value_surf": value_surf,
                "value_rect": value_rect
            })

        return table_rows

    def build_3_col_table(self, start_x: int, start_y: int, rows: List[Tuple[str, str, str]],
                          col_widths: Tuple[int, int, int], row_height: int = 30, font_size: int = 20) -> List[dict]:
        """
        Builds a 3-column table at the specified location with the given rows and column widths.

        :param start_x: The starting X coordinate for the table.
        :param start_y: The starting Y coordinate for the table.
        :param rows: A list of tuples where each tuple contains (description, value, third_value) triples.
        :param col_widths: A tuple specifying the width of the columns in order: first column (description),
                           second column (value), third column (third_value).
        :param row_height: The height of each row in the table.
        :param font_size: The font size to be used in the table.
        :return: A list of dictionaries where each dictionary contains the surfaces and rects for a table row.
        """
        table_rows = []
        font = self.load_font('ui_font', font_size)

        for index, (description, value, third_value) in enumerate(rows):
            y_position = start_y + index * row_height

            # First column
            description_surf = font.render(description, True, self._text_colour_1)
            description_rect = pygame.Rect(start_x + 10, y_position, col_widths[0], row_height)
            description_rect.centery = y_position + (row_height // 2)

            # Second column
            value_surf = font.render(value, True, self._text_colour_1)
            value_rect = pygame.Rect(start_x + col_widths[0], y_position, col_widths[1], row_height)
            value_rect.centery = y_position + (row_height // 2)

            # Third column
            third_value_surf = font.render(third_value, True, self._text_colour_1)
            third_value_rect = pygame.Rect(start_x + col_widths[0] + col_widths[1], y_position, col_widths[2],
                                           row_height)
            third_value_rect.centery = y_position + (row_height // 2)

            table_rows.append({
                "description_surf": description_surf,
                "description_rect": description_rect,
                "value_surf": value_surf,
                "value_rect": value_rect,
                "third_value_surf": third_value_surf,
                "third_value_rect": third_value_rect
            })

        return table_rows

    def draw_table(self, table_rows: List[dict]) -> None:
        """
        Draws a previously built table on the screen.

        :param table_rows: A list of dictionaries where each dictionary contains the surfaces and rects for a table row.
        """
        for row in table_rows:
            self.game.get_screen().blit(row["description_surf"], row["description_rect"])
            self.game.get_screen().blit(row["value_surf"], row["value_rect"])

    def draw_performance_stats_panel(self, performance_stats: dict, game_stats: dict) -> None:
        """

        :param performance_stats:
        :param game_stats:
        :return:
        """
        if self.display_performance_stats:
            start_x = self.options_button['rect'].left
            start_y = self.options_button['rect'].bottom + 50

            rows = [
                ("Board size:", game_stats["Board size"]),
                ("Hidden mines remaining:", str(game_stats["Mines remaining"])),
                ("Number of known mine positions:", str(game_stats["Known mines"])),
                ("Known safe moves remaining: ", str(game_stats["Safe moves"])),
                ("Search Algorithm:", self.search_algorithm_display_names[self.current_search_algorithm_name]),
                ("Safe Cell Strategy:", self.safe_cell_strategy_display_names[
                    self.safe_cell_strategies[self.current_safe_cell_strategy_index]]),
                ("Knowledge Base (Average Size):", f"{performance_stats['knowledge_base_avg_size']:.2f}"),
                ("Knowledge Base (Maximum Size):", str(performance_stats["knowledge_base_max_size"])),
                ("Total Inferences Made:", str(performance_stats["inferences_total"])),
                ("Subset Comparisons (Average):", f"{performance_stats['subset_comparisons_avg']:.2f}"),
                ("Subset Comparisons (Maximum):", str(performance_stats["subset_comparisons_max"])),
                ("Total Subset Comparisons:", str(performance_stats["subset_comparisons_total"])),
                ("Inference to Comparison Ratio:", f"{performance_stats['inference_to_comparison_ratio']:.3f}"),
                ("AI Decision Loop (Average Iterations):", f"{performance_stats['iterations_avg']:.2f}"),
                ("AI Decision Loop (Max Iterations):", str(performance_stats["iterations_max"])),
                ("Total AI Decision Loops:", str(performance_stats["iterations_total"])),
                ("Duplicate Non-Empty Inferences (Total):", str(performance_stats["duplicate_inferences_total"]))
            ]

            col_widths = (330, 120)
            self.update_table(start_x=start_x, start_y=start_y, rows=rows, col_widths=col_widths, font_size=22)

    def update_table(self, start_x: int, start_y: int, rows: List[Tuple[str, str]],
                     col_widths: Tuple[int, int], row_height: int = 30, font_size: int = 20) -> None:
        """
        Updates and redraws a table at the specified location with the given rows and column widths.

        :param start_x: The starting X coordinate for the table.
        :param start_y: The starting Y coordinate for the table.
        :param rows: A list of tuples where each tuple contains (description, value) pairs.
        :param col_widths: A tuple specifying the width of the first column (description) and the second column (value).
        :param row_height: The height of each row in the table.
        :param font_size: The font size to be used in the table.
        """
        # Clear the area where the table will be drawn
        table_height = len(rows) * row_height
        table_width = sum(col_widths)

        pygame.draw.rect(
            self.game.get_screen(),
            self._background_colour,
            (start_x, start_y, table_width, table_height)
        )
        # Build and draw the table with the latest stats
        table = self.build_2_col_table(start_x, start_y, rows, col_widths, row_height, font_size)
        self.draw_table(table)

    def handle_speed_button_click(self) -> None:
        """
        Handles the click event for the speed button, cycling through the speed options.
        """
        if self.handle_button_click(self.speed_button):
            self.current_speed_index = (self.current_speed_index + 1) % len(self.speed_options)
            self.speed_button['text'] = self.load_font('ui_font', 28).render(
                self.speed_options[self.current_speed_index], True, self._text_colour_1
            )
            self.speed_button['text_rect'] = self.speed_button['text'].get_rect(center=self.speed_button['rect'].center)
            pygame.time.wait(200)  # Add a delay to avoid rapid cycling

    def handle_board_state_button_click(self) -> None:
        """
        Handles the click event for the 'Board State' button.

        Toggles the state between 'New' and 'Existing'.
        """
        if self.handle_button_click(self.board_state_button):
            # Toggle the state
            self.current_board_state = 'Existing' if self.current_board_state == 'New' else 'New'

            # Update the button text
            self.board_state_button['text'] = self.load_font('ui_font', 28).render(
                self.current_board_state, True, self._text_colour_1
            )
            self.board_state_button['text_rect'] = self.board_state_button['text'].get_rect(
                center=self.board_state_button['rect'].center
            )
            pygame.time.wait(200)  # Add a delay to avoid rapid toggling

    def display_options_menu(self) -> None:
        """
        Displays the Options Menu on the screen using a table layout.
        """
        self.game.get_screen().fill(self._background_colour)

        # Draw the first line of the title ("Minesweeper") and center it
        minesweeper_label, minesweeper_rect = self.create_label("MinesweeperAI", 50, 'main_font', 100,
                                                                self._text_colour_1)
        minesweeper_rect.centerx = self.game.get_screen_width() // 2  # Center the label horizontally
        self.draw_label(minesweeper_label, minesweeper_rect)

        # Draw the second line of the title ("Plug and play data structures and algorithms") and center it
        subtitle_label, subtitle_rect = self.create_label(
            "Plug and play data structures and algorithms",
            minesweeper_rect.bottom - 20,  # Position it below the first line
            'ui_font', 60,  # Use the UI font and a smaller size
            self._text_colour_1
        )
        subtitle_rect.centerx = self.game.get_screen_width() // 2  # Center the label horizontally
        self.draw_label(subtitle_label, subtitle_rect)

        # Define the starting coordinates for the table
        start_x = (self.game.get_screen_width() // 2) - 300  # Adjust to center the table
        start_y = subtitle_rect.bottom + 50
        col_widths = (250, 200)

        # Define the table rows
        rows = [
            ("Board Size", self.board_size_input['box']),
            ("Percentage of Mines (%)", self.mines_input['box']),
            ("Game Speed", self.speed_button),
            ("Search Algorithm", self.search_algorithm_button),
            ("Safe Cell Strategy", self.safe_cell_strategy_button),
            ("Start Position", self.start_position_button),
            ("Performance Stats", self.performance_stats_button),
            ("Inference Logic", self.inference_logic_button),
            ("Board State", self.board_state_button),
        ]

        # Draw the table rows
        for i, (description, widget) in enumerate(rows):
            y_position = start_y + i * 70  # Adjust spacing as needed
            description_label, description_rect = self.create_label(description, y_position, 'ui_font', 28,
                                                                    self._text_colour_1)
            description_rect.x = start_x + 10
            description_rect.centery = y_position + 30

            # Draw the description label
            self.draw_label(description_label, description_rect)

            if isinstance(widget, UserInputHandler):
                # If the widget is an input box
                widget.input_box_rect.x = start_x + col_widths[0] + 10
                widget.input_box_rect.y = y_position
                widget.draw_input_box(self.game.get_screen())
            else:
                # If the widget is a button
                widget_rect = widget['rect']
                widget_rect.x = start_x + col_widths[0] + 10
                widget_rect.centery = y_position + 30
                self.draw_button(widget)

        # Draw Play Game button across the bottom
        self.play_button['rect'].y = start_y + len(rows) * 70 + 50  # Adjust Y position to be below the table
        self.play_button['text_rect'] = self.play_button['text'].get_rect(center=self.play_button['rect'].center)
        self.draw_button(self.play_button)

        self.force_redraw_buttons()

        # Display error message if any
        if self.error_message:
            error_label_y_position = self.play_button['rect'].bottom + 20
            error_label, error_rect = self.create_label(self.error_message,
                                                        error_label_y_position,
                                                        'main_font',
                                                        20,
                                                        self._text_colour_1)
            error_rect.centerx = self.game.get_screen_width() // 2  # Center the label horizontally
            self.draw_label(error_label, error_rect)

        pygame.display.flip()

    def handle_safe_cell_strategy_button_click(self) -> None:
        """
        Handles the click event for the 'Safe Cell Strategy'
        Cycles through all available safe cell data structure options.
        Updates the button text to reflect the current state.
        """
        if self.handle_button_click(self.safe_cell_strategy_button):
            # Update the current safe cell strategy index and name
            self.current_safe_cell_strategy_index = (self.current_safe_cell_strategy_index + 1) % len(
                self.safe_cell_strategies)
            current_strategy_name = self.safe_cell_strategies[self.current_safe_cell_strategy_index]

            # Update the button text to display the new safe cell strategy name
            self.safe_cell_strategy_button['text'] = self.load_font('ui_font', 28).render(
                current_strategy_name, True, self._text_colour_1
            )
            self.safe_cell_strategy_button['text_rect'] = self.safe_cell_strategy_button['text'].get_rect(
                center=self.safe_cell_strategy_button['rect'].center
            )
            pygame.time.wait(200)  # Add a delay to avoid rapid cycling

    def handle_performance_stats_button_click(self) -> None:
        """
        Handles the click event for the 'Underlying Stats' button.

        Toggles the display state of the underlying statistics between 'On' and 'Off'.
        Updates the button text to reflect the current state.
        """
        self.display_performance_stats = self.toggle_button(
            self.performance_stats_button,
            self.display_performance_stats,
            'On',
            'Off'
        )

    def handle_inference_logic_button_click(self) -> None:
        """
        Handles the click event for the 'Inference Logic' button.

        Toggles the display state of the inference logic between 'On' and 'Off'.
        Updates the button text to reflect the current state.
        """
        self.display_inference_logic = self.toggle_button(
            self.inference_logic_button,
            self.display_inference_logic,
            'Inference Logic: On',
            'Inference Logic: Off'
        )

    def toggle_button(self, button: dict, display_flag: bool, label_on: str, label_off: str) -> bool:
        """
          Toggles the state of a button and updates its text.
          This method checks if the button was clicked, then toggles the display flag and updates
          the button's text accordingly. A small delay is introduced after toggling to ensure smooth UI interaction.

          :param button: A dictionary representing the button to toggle. It should contain keys such as
                        'text' and 'rect' for updating the button's display properties.
          :param display_flag: A boolean indicating the current state of the display.
                               If True, the button is considered "on".
          :param label_on: The text to display on the button when the display flag is True.
          :param label_off: The text to display on the button when the display flag is False.

          :return: A boolean representing the new state of the display flag after toggling.
          """
        if self.handle_button_click(button):
            display_flag = not display_flag
            new_text = label_on if display_flag else label_off
            button['text'] = self.load_font('ui_font', 28).render(new_text, True, self._text_colour_1)
            button['text_rect'] = button['text'].get_rect(center=button['rect'].center)
            pygame.time.wait(200)
        return display_flag

    def update_board_state_to_new(self) -> None:
        """
        Updates the board state to 'New' and refreshes the button text.
        """
        self.current_board_state = "New"
        self.board_state_button['text'] = self.load_font('ui_font', 28).render(
            "New", True, self._text_colour_1
        )
        self.board_state_button['text_rect'] = self.board_state_button['text'].get_rect(
            center=self.board_state_button['rect'].center
        )

    def get_background_colour(self) -> Tuple[int, int, int]:
        """
        Returns the current background colour used in the UI.

        :return: A tuple representing the RGB values of the background colour.
        """
        return self._background_colour

    def get_text_colour_1(self) -> Tuple[int, int, int]:
        """
        Returns the primary text colour used in the UI.

        :return: A tuple representing the RGB values of the primary text colour.
        """
        return self._text_colour_1

    def get_current_board_state(self) -> str:
        """
        Returns the current state of the board.

        :return: A string representing the current board state, e.g., 'New'.
        """
        return self.current_board_state
