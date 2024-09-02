from collections import deque
from typing import List, Set, Tuple, Union, Deque
import random
from .knowledge_statement import KnowledgeStatement
from .stat_generator import StatGenerator
from .subset_search_algorithms import SubsetSearchAlgorithms
from .safe_cell_data_structures import SafeCellDataStructures


class MinesweeperAI:
    """
    Minesweeper game player AI.
    """

    def __init__(self, grid_size: int = 16, search_algorithm_name: str = "BFS", safe_cell_strategy: str = "Random") -> None:
        """
        Initialise the MinesweeperAI with a grid size, search algorithm, and safe cell strategy.

        :param grid_size: Size of the Minesweeper grid.
        :param search_algorithm_name: Name of the search algorithm to use.
        :param safe_cell_strategy: Strategy to use for selecting safe cells.
        """
        self.grid_size: int = grid_size
        self.moves_made: Set[Tuple[int, int]] = set()
        self.identified_mines: Set[Tuple[int, int]] = set()
        self.identified_safe_cells: Set[Tuple[int, int]] = set()
        self.safe_cell_queue: Deque[Tuple[int, int]] = deque()
        self.knowledge_base: List[KnowledgeStatement] = []
        self.stat_generator = StatGenerator(self.grid_size)
        self.low_risk_cache: Set[Tuple[int, int]] = set()

        self.search_algorithm_name: str = search_algorithm_name
        self.search_data_structures = SubsetSearchAlgorithms(self.stat_generator)
        self.search_algorithm_method = self.search_data_structures.select_algorithm(search_algorithm_name)

        self.safe_cell_data_structures = SafeCellDataStructures()
        self.safe_cell_selection_strategy = self.safe_cell_data_structures.select_strategy(safe_cell_strategy)

    def mark_cell_as_mine(self, cell: Tuple[int, int]) -> None:
        """
        Mark a cell as a mine and update the knowledge base accordingly.

        :param cell: Tuple representing the cell coordinates.
        """
        self.identified_mines.add(cell)
        for statement in self.knowledge_base:
            statement.mark_cell_as_mine(cell)

    def mark_cell_as_safe(self, cell: Tuple[int, int]) -> None:
        """
        Mark a cell as safe and update the knowledge base accordingly.

        :param cell: Tuple representing the cell coordinates.
        """
        if cell not in self.identified_safe_cells:
            self.identified_safe_cells.add(cell)
            self.safe_cell_queue.append(cell)
        for statement in self.knowledge_base:
            statement.mark_cell_as_safe(cell)

    def remove_empty_and_duplicate_statements(self) -> None:
        """
        Remove empty and duplicate knowledge statements from the knowledge base.
        """
        original_set = set(self.knowledge_base)
        cleaned_knowledge_base = []
        duplicate_count = 0

        for statement in self.knowledge_base:
            if statement.get_cell_positions():
                if statement not in original_set:
                    duplicate_count += 1
                else:
                    cleaned_knowledge_base.append(statement)
                    original_set.remove(statement)

        self.knowledge_base = cleaned_knowledge_base
        cleaned_size = len(self.knowledge_base)

        self.stat_generator.update_knowledge_base_size(cleaned_size)
        self.stat_generator.update_duplicate_inferences(duplicate_count)

    def add_knowledge(self, cell: Tuple[int, int], surrounding_mines_count: int) -> None:
        """
        Add knowledge based on the identified cell and its surrounding mine count.

        :param cell: Tuple representing the cell coordinates.
        :param surrounding_mines_count: Number of mines surrounding the cell.
        """
        self.stat_generator.reset_current_stats()

        self.moves_made.add(cell)
        self.mark_cell_as_safe(cell)

        surrounding_cells: Set[Tuple[int, int]] = set(
            (i, j)
            for i in range(cell[0] - 1, cell[0] + 2)
            for j in range(cell[1] - 1, cell[1] + 2)
            if (i, j) != cell and 0 <= i < self.grid_size and 0 <= j < self.grid_size
        )

        surrounding_cells.difference_update(self.identified_safe_cells)
        for mine in self.identified_mines:
            if mine in surrounding_cells:
                surrounding_mines_count -= 1
                surrounding_cells.remove(mine)

        if surrounding_cells:
            new_statement = KnowledgeStatement(surrounding_cells, surrounding_mines_count)
            self.knowledge_base.append(new_statement)


        knowledge_changed = True
        loop_iterations = 0
        inferred_set = set(self.knowledge_base)

        while knowledge_changed:
            loop_iterations += 1
            knowledge_changed = False

            cells_to_mark_safe: Set[Tuple[int, int]] = set()
            cells_to_mark_as_mine: Set[Tuple[int, int]] = set()

            for statement in self.knowledge_base.copy():
                safe_cells = statement.known_safes()
                mine_cells = statement.known_mines()

                cells_to_mark_safe.update(safe_cells)
                cells_to_mark_as_mine.update(mine_cells)

            if cells_to_mark_safe or cells_to_mark_as_mine:
                knowledge_changed = True

            for safe_cell in cells_to_mark_safe:
                self.mark_cell_as_safe(safe_cell)
            for mine_cell in cells_to_mark_as_mine:
                self.mark_cell_as_mine(mine_cell)

            self.remove_empty_and_duplicate_statements()

            #  The knowledge base is sent to the user selected search algorithm and processed
            inferred_statements = self.search_algorithm_method(self.knowledge_base)

            new_inferences = [inf for inf in inferred_statements if inf not in inferred_set]
            if new_inferences:
                inferred_set.update(new_inferences)
                self.knowledge_base.extend(new_inferences)
                knowledge_changed = True

        self.stat_generator.update_iterations(loop_iterations)

    def make_safe_move(self) -> Union[Tuple[int, int], None]:
        """
        Make a move by selecting a known safe cell using the chosen data structure.

        :return: Tuple representing the cell coordinates, or None if no safe move is possible.
        """
        if self.safe_cell_queue:
            return self.safe_cell_selection_strategy(self.safe_cell_queue)
        return None

    def make_random_move(self) -> Union[Tuple[int, int], None]:
        """
        Make a random move by selecting an unmarked cell.

        :return: Tuple representing the cell coordinates, or None if no move is possible.
        """
        all_possible_moves: List[Tuple[int, int]] = [
            (i, j) for i in range(self.grid_size) for j in range(self.grid_size)
        ]
        move_found: bool = False

        while not move_found and all_possible_moves:
            random_cell_index: int = random.randrange(len(all_possible_moves))
            selected_cell: Tuple[int, int] = all_possible_moves.pop(random_cell_index)
            if selected_cell not in self.moves_made and selected_cell not in self.identified_mines:
                return selected_cell
        return None
