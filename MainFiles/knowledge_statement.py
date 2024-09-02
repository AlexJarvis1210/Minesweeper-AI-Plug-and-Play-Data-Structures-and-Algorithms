from typing import Set, Tuple


class KnowledgeStatement:
    """
    Logical statement about a Minesweeper game.
    A knowledge statement consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cell_positions: Set[Tuple[int, int]], mine_count: int):
        """
        Initialise a knowledge statement with given cells and count.

        :param cell_positions: Set of cell coordinates.
        :param mine_count: Number of mines in the set of cells.
        """
        self.cell_positions: Set[Tuple[int, int]] = set(cell_positions)
        self.mine_count: int = mine_count

    def __eq__(self, other: object) -> bool:
        """
        Check equality between two KnowledgeStatement objects.

        :param other: Object to compare against.
        :return: True if objects are equal, False otherwise.
        """
        if isinstance(other, KnowledgeStatement):
            return self.cell_positions == other.cell_positions and self.mine_count == other.mine_count
        return False

    def __hash__(self) -> int:
        """
        Generate a hash value for the KnowledgeStatement.

        :return: Hash value as an integer.
        """
        return hash((frozenset(self.cell_positions), self.mine_count))

    def __lt__(self, other: object) -> bool:
        """
        Less-than comparison based on the number of cells and mine count.

        :param other: KnowledgeStatement to compare against.
        :return: True if self is less than other, False otherwise.
        """
        if isinstance(other, KnowledgeStatement):
            return (len(self.cell_positions), self.mine_count) < (len(other.cell_positions), other.mine_count)
        return NotImplemented

    def __str__(self) -> str:
        """
        String representation of the KnowledgeStatement.

        :return: String describing the set of cell positions and mine count.
        """
        return f"{self.cell_positions} = {self.mine_count}"

    def known_mines(self) -> Set[Tuple[int, int]]:
        """
        Return the set of all cells known to be mines.

        :return: Set of cell coordinates known to be mines.
        """
        if len(self.cell_positions) == self.mine_count:
            return self.cell_positions
        return set()

    def known_safes(self) -> Set[Tuple[int, int]]:
        """
        Return the set of all cells in self.cell_positions known to be safe.

        :return: Set of cell coordinates known to be safe.
        """
        if self.mine_count == 0:
            return self.cell_positions
        return set()

    def mark_cell_as_mine(self, cell: Tuple[int, int]) -> None:
        """
        Update internal knowledge representation given that
        a cell is known to be a mine.

        :param cell: Tuple representing the cell coordinates.
        """
        if cell in self.cell_positions:
            self.cell_positions.remove(cell)
            self.mine_count -= 1

    def mark_cell_as_safe(self, cell: Tuple[int, int]) -> None:
        """
        Update internal knowledge representation given that
        a cell is known to be safe.

        :param cell: Tuple representing the cell coordinates.
        """
        if cell in self.cell_positions:
            self.cell_positions.remove(cell)

    def get_mine_count(self) -> int:
        """
        Get the number of mines in the knowledge statement.

        :return: Integer count of mines.
        """
        return self.mine_count

    def get_cell_positions(self) -> Set[Tuple[int, int]]:
        """
        Get the set of cell positions in the knowledge statement.

        :return: Set of tuples representing cell positions.
        """
        return self.cell_positions
