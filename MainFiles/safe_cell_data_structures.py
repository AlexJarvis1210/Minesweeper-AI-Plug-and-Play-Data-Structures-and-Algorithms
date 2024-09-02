from typing import Tuple, Deque, Union
import random

class SafeCellDataStructures:
    """
    Provides strategies for selecting safe cells from a list of identified safe cells.
    """

    def __init__(self):
        """
        Initialise the strategy dictionary.
        """
        self.strategies = {
            "First In, First Out": self.select_fifo,
            "Last In, First Out": self.select_lifo,
            "Sorted by position": self.select_sorted,
            "Random": self.select_random
        }

    def select_strategy(self, strategy_name: str):
        """
        Select and return the strategy method based on the provided strategy name.

        :param strategy_name: The name of the strategy to use (e.g., "FIFO", "LIFO", "Sorted", "Random").
        :return: The strategy method corresponding to the strategy name.
        """
        strategy = self.strategies.get(strategy_name)
        if strategy:
            return strategy
        print(f"ERROR: Strategy '{strategy_name}' not found, defaulting to FIFO")
        return self.select_fifo

    def select_fifo(self, identified_safe_cells: Deque[Tuple[int, int]]) -> Union[Tuple[int, int], None]:
        """
        Select a cell using the FIFO (First-In-First-Out) strategy.

        :param identified_safe_cells: Deque of identified safe cells.
        :return: The selected cell or None if no cells are available.
        """
        if identified_safe_cells:
            return identified_safe_cells.popleft()
        return None

    def select_lifo(self, identified_safe_cells: Deque[Tuple[int, int]]) -> Union[Tuple[int, int], None]:
        """
        Select a cell using the LIFO (Last-In-First-Out) strategy.

        :param identified_safe_cells: Deque of identified safe cells.
        :return: The selected cell or None if no cells are available.
        """
        if identified_safe_cells:
            return identified_safe_cells.pop()
        return None

    def select_sorted(self, identified_safe_cells: Deque[Tuple[int, int]]) -> Union[Tuple[int, int], None]:
        """
        Select a cell by sorting based on proximity to the top-left corner.

        :param identified_safe_cells: Deque of identified safe cells.
        :return: The selected cell or None if no cells are available.
        """
        if identified_safe_cells:
            sorted_cells = sorted(identified_safe_cells, key=lambda x: (x[0], x[1]))
            selected_cell = sorted_cells[0]
            identified_safe_cells.remove(selected_cell)
            return selected_cell
        return None

    def select_random(self, identified_safe_cells: Deque[Tuple[int, int]]) -> Union[Tuple[int, int], None]:
        """
        Select a cell randomly from the identified safe cells.

        :param identified_safe_cells: Deque of identified safe cells.
        :return: The selected cell or None if no cells are available.
        """
        if identified_safe_cells:
            selected_cell = random.choice(identified_safe_cells)
            identified_safe_cells.remove(selected_cell)
            return selected_cell
        return None
