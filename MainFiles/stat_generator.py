from typing import Dict, Any


class StatGenerator:
    """
    Class to generate and track various statistics to compare the different subset search algorithms.
    """

    def __init__(self, grid_size: int):
        """
        Initialize the StatGenerator with the size of the grid.

        :param grid_size: The size of the Minesweeper grid.
        """
        self.grid_size: int = grid_size
        self.knowledge_base_total_size: int = 0
        self.knowledge_base_max_size: int = 0
        self.knowledge_base_count: int = 0
        self.inferences_total: int = 0
        self.inferences_max: int = 0
        self.subset_comparisons_total: int = 0
        self.subset_comparisons_max: int = 0
        self.subset_comparisons_count: int = 0
        self.iterations_total: int = 0  # Total iterations over all loops
        self.iterations_max: int = 0  # Max iterations in a single loop
        self.iterations_count: int = 0  # Count of loops
        self.duplicate_inferences_total: int = 0  # Tracking duplicate non-empty inferences

    def reset_current_stats(self) -> None:
        """
        Reset counters that are specific to the current operation.
        Increments the knowledge base count.
        """
        self.knowledge_base_count += 1

    def update_knowledge_base_size(self, size: int) -> None:
        """
        Update the knowledge base size statistics.

        :param size: The current size of the knowledge base.
        """
        self.knowledge_base_total_size += size
        if size > self.knowledge_base_max_size:
            self.knowledge_base_max_size = size

    def update_inferences(self, inferences: int) -> None:
        """
        Update the total and maximum number of inferences made.

        :param inferences: The number of inferences made in the current operation.
        """
        self.inferences_total += inferences
        if inferences > self.inferences_max:
            self.inferences_max = inferences

    def update_total_subset_comparisons(self, comparisons: int) -> None:
        """
        Update the total number of subset comparisons.

        :param comparisons: The number of subset comparisons made in the current operation.
        """
        self.subset_comparisons_total += comparisons
        self.subset_comparisons_count += 1

    def update_subset_comparisons(self, comparisons: int) -> None:
        """
        Update the maximum and total number of subset comparisons.

        :param comparisons: The number of subset comparisons made in the current operation.
        """
        if comparisons > self.subset_comparisons_max:
            self.subset_comparisons_max = comparisons
        self.update_total_subset_comparisons(comparisons)

    def update_iterations(self, iterations: int) -> None:
        """
        Update the total and maximum number of iterations in loops.

        :param iterations: The number of iterations made in the current operation.
        """
        self.iterations_total += iterations
        if iterations > self.iterations_max:
            self.iterations_max = iterations
        self.iterations_count += 1

    def update_duplicate_inferences(self, duplicates: int) -> None:
        """
        Update the total number of duplicate inferences.

        :param duplicates: The number of duplicate inferences made in the current operation.
        """
        self.duplicate_inferences_total += duplicates

    def get_inference_to_comparison_ratio(self) -> float:
        """
        Calculate the ratio of inferences to subset comparisons.

        :return: The ratio of inferences to subset comparisons, or 0 if no comparisons were made.
        """
        if self.subset_comparisons_total == 0:
            return 0.0
        return self.inferences_total / self.subset_comparisons_total

    def get_avg_iterations(self) -> float:
        """
        Calculate the average number of iterations per loop.

        :return: The average number of iterations, or 0 if no iterations were counted.
        """
        if self.iterations_count == 0:
            return 0.0
        return self.iterations_total / self.iterations_count

    def get_performance_stats_summary(self) -> Dict[str, Any]:
        """
        Generate a summary of the performance statistics.

        :return: A dictionary containing the summary of performance statistics.
        """
        stats_summary = {
            "knowledge_base_avg_size": self.knowledge_base_total_size / self.knowledge_base_count if self.knowledge_base_count > 0 else 0,
            "knowledge_base_max_size": self.knowledge_base_max_size,
            "inferences_total": self.inferences_total,
            "subset_comparisons_avg": self.subset_comparisons_total / self.subset_comparisons_count if self.subset_comparisons_count > 0 else 0,
            "subset_comparisons_max": self.subset_comparisons_max,
            "subset_comparisons_total": self.subset_comparisons_total,
            "inference_to_comparison_ratio": self.get_inference_to_comparison_ratio(),
            "iterations_avg": self.get_avg_iterations(),
            "iterations_max": self.iterations_max,
            "iterations_total": self.iterations_total,
            "duplicate_inferences_total": self.duplicate_inferences_total
        }
        return stats_summary

    def reset_stats(self) -> None:
        """
        Reset all statistics to their initial values.
        """
        self.knowledge_base_total_size = 0
        self.knowledge_base_max_size = 0
        self.knowledge_base_count = 0
        self.inferences_total = 0
        self.inferences_max = 0
        self.subset_comparisons_total = 0
        self.subset_comparisons_max = 0
        self.subset_comparisons_count = 0
        self.iterations_total = 0
        self.iterations_max = 0
        self.iterations_count = 0
        self.duplicate_inferences_total = 0
