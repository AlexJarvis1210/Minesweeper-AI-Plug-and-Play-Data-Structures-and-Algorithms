from collections import deque
from typing import List, Optional
from .knowledge_statement import KnowledgeStatement
from .stat_generator import StatGenerator


class TreeNode:
    """
    Represents a node in a tree structure used in BFS and DFS search algorithms.
    """

    def __init__(self, knowledge_base: List[KnowledgeStatement], parent: Optional['TreeNode'] = None):
        """
        Initialize a TreeNode.

        :param knowledge_base: The knowledge base (a list of KnowledgeStatement objects) at this node.
        :param parent: The parent node in the tree.
        """
        self.knowledge_base: List[KnowledgeStatement] = knowledge_base
        self.parent: Optional[TreeNode] = parent
        self.children: List[TreeNode] = []
        self.inferences: List[KnowledgeStatement] = []

    def add_child(self, child_node: 'TreeNode') -> None:
        """
        Add a child node to this node.

        :param child_node: The TreeNode to add as a child.
        """
        self.children.append(child_node)


class SubsetSearchAlgorithms:
    """
    Contains various subset search algorithms for inferring new KnowledgeStatements from an existing knowledge base.
    """

    def __init__(self, stat_generator: StatGenerator):
        """
        Initialize SubsetSearchAlgorithms with a StatGenerator for tracking performance metrics.

        :param stat_generator: The StatGenerator instance used to record statistics.
        """
        self.stat_generator: StatGenerator = stat_generator
        self.algorithms = {
            "brute_force": self.brute_force_search,
            "divide_and_conquer": self.divide_and_conquer_search,
            "dynamic_programming": self.dynamic_programming_search,
            "greedy_algorithm_size": self.greedy_algorithm_size_search,
            "greedy_algorithm_minecount": self.greedy_algorithm_minecount_search,
            "bfs": self.bfs_search,
            "dfs": self.dfs_search
        }

    def select_algorithm(self, algorithm_name: str):
        """
        Select and return the search algorithm method based on the provided algorithm name.

        :param algorithm_name: The name of the algorithm to select.
        :return: The selected algorithm method.
        """
        algorithm = self.algorithms.get(algorithm_name)
        if algorithm:
            return algorithm
        print(f"ERROR: Algorithm '{algorithm_name}' not found, defaulting to Brute Force")
        return self.brute_force_search

    def brute_force_search(self, knowledge_base: List[KnowledgeStatement], subset_comparisons: int = 0) -> List[KnowledgeStatement]:
        """
        Perform a brute-force search to infer new KnowledgeStatements.

        :param knowledge_base: The current knowledge base of KnowledgeStatement objects.
        :param subset_comparisons: The initial count of subset comparisons (default is 0).
        :return: A list of inferred KnowledgeStatement objects.
        """
        inferred_statements: List[KnowledgeStatement] = []
        inferred_statements_set = set()

        for statement in knowledge_base:
            for other_statement in knowledge_base:
                subset_comparisons += 1
                if statement.get_cell_positions().issubset(other_statement.get_cell_positions()):
                    inferred_cells = other_statement.get_cell_positions() - statement.get_cell_positions()
                    inferred_count = other_statement.get_mine_count() - statement.get_mine_count()
                    new_inferred_statement = KnowledgeStatement(inferred_cells, inferred_count)
                    if new_inferred_statement not in inferred_statements_set:
                        inferred_statements.append(new_inferred_statement)
                        inferred_statements_set.add(new_inferred_statement)

        self.stat_generator.update_subset_comparisons(subset_comparisons)
        self.stat_generator.update_inferences(len(inferred_statements))

        return inferred_statements

    def divide_and_conquer_search(self, knowledge_base: List[KnowledgeStatement], subset_comparisons: int = 0) -> List[KnowledgeStatement]:
        """
        Perform a divide-and-conquer search to infer new KnowledgeStatements.

        :param knowledge_base: The current knowledge base of KnowledgeStatement objects.
        :param subset_comparisons: The initial count of subset comparisons (default is 0).
        :return: A list of inferred KnowledgeStatement objects.
        """
        if not knowledge_base:
            return []

        def divide_and_conquer(a_knowledge_base: List[KnowledgeStatement], start: int, end: int):
            if start > end:
                return [], 0, 0  # Return empty list, 0 comparisons, 0 inferences

            if start == end:
                return [a_knowledge_base[start]], 0, 0  # Single element, no comparisons

            mid = (start + end) // 2
            left_inferred, left_comparisons, left_inferences = divide_and_conquer(a_knowledge_base, start, mid)
            right_inferred, right_comparisons, right_inferences = divide_and_conquer(a_knowledge_base, mid + 1, end)

            merge_statements = left_inferred + right_inferred
            merge_comparisons = left_comparisons + right_comparisons
            merge_inferences = left_inferences + right_inferences

            for left_statement in left_inferred:
                for right_statement in right_inferred:
                    merge_comparisons += 1
                    if left_statement.get_cell_positions().issubset(right_statement.get_cell_positions()):
                        inferred_cells = right_statement.get_cell_positions() - left_statement.get_cell_positions()
                        inferred_count = right_statement.get_mine_count() - left_statement.get_mine_count()
                        new_inferred_statement = KnowledgeStatement(inferred_cells, inferred_count)
                        if new_inferred_statement not in merge_statements:
                            merge_statements.append(new_inferred_statement)
                            merge_inferences += 1

            return merge_statements, merge_comparisons, merge_inferences

        inferred_statements, total_comparisons, total_inferences = divide_and_conquer(knowledge_base, 0, len(knowledge_base) - 1)

        self.stat_generator.update_subset_comparisons(total_comparisons)
        self.stat_generator.update_inferences(total_inferences)

        return inferred_statements

    def dynamic_programming_search(self, knowledge_base: List[KnowledgeStatement], subset_comparisons: int = 0) -> List[KnowledgeStatement]:
        """
        Perform a dynamic programming search to infer new KnowledgeStatements.

        :param knowledge_base: The current knowledge base of KnowledgeStatement objects.
        :param subset_comparisons: The initial count of subset comparisons (default is 0).
        :return: A list of inferred KnowledgeStatement objects.
        """
        dp_cache = set()
        inferred_statements: List[KnowledgeStatement] = []

        sorted_knowledge_base = sorted(knowledge_base)

        for i, statement in enumerate(sorted_knowledge_base):
            for j in range(i + 1, len(sorted_knowledge_base)):
                other_statement = sorted_knowledge_base[j]

                key = (statement, other_statement)
                if key in dp_cache:
                    continue

                subset_comparisons += 1
                if statement.get_cell_positions().issubset(other_statement.get_cell_positions()):
                    inferred_cells = other_statement.get_cell_positions() - statement.get_cell_positions()
                    inferred_count = other_statement.get_mine_count() - statement.get_mine_count()

                    if inferred_count < 0 or not inferred_cells:
                        continue

                    new_inferred_statement = KnowledgeStatement(inferred_cells, inferred_count)

                    dp_cache.add(key)

                    if new_inferred_statement not in inferred_statements:
                        inferred_statements.append(new_inferred_statement)

                        if len(inferred_cells) > 1:
                            dp_cache.add((new_inferred_statement, statement))

        self.stat_generator.update_subset_comparisons(subset_comparisons)
        self.stat_generator.update_inferences(len(inferred_statements))

        return inferred_statements

    def greedy_algorithm_size_search(self, knowledge_base: List[KnowledgeStatement], subset_comparisons: int = 0) -> List[KnowledgeStatement]:
        """
        Perform a greedy search based on the size of cell positions to infer new KnowledgeStatements.

        :param knowledge_base: The current knowledge base of KnowledgeStatement objects.
        :param subset_comparisons: The initial count of subset comparisons (default is 0).
        :return: A list of inferred KnowledgeStatement objects.
        """
        inferred_statements: set = set()

        sorted_knowledge_base = sorted(knowledge_base, key=lambda x: len(x.get_cell_positions()))

        for i, current_statement in enumerate(sorted_knowledge_base):
            for next_statement in sorted_knowledge_base[i + 1:]:
                subset_comparisons += 1

                if len(next_statement.get_cell_positions()) >= len(current_statement.get_cell_positions()):
                    break

                if next_statement.get_cell_positions().issubset(current_statement.get_cell_positions()):
                    inferred_cells = current_statement.get_cell_positions() - next_statement.get_cell_positions()
                    inferred_count = current_statement.get_mine_count() - next_statement.get_mine_count()
                    new_inferred_statement = KnowledgeStatement(inferred_cells, inferred_count)

                    if new_inferred_statement not in inferred_statements:
                        inferred_statements.add(new_inferred_statement)
                        knowledge_base.append(new_inferred_statement)

            sorted_knowledge_base = sorted(knowledge_base, key=lambda x: len(x.get_cell_positions()))

        self.stat_generator.update_subset_comparisons(subset_comparisons)
        self.stat_generator.update_inferences(len(inferred_statements))

        return list(inferred_statements)

    def greedy_algorithm_minecount_search(self, knowledge_base: List[KnowledgeStatement], subset_comparisons: int = 0) -> List[KnowledgeStatement]:
        """
        Perform a greedy search based on mine count to infer new KnowledgeStatements.

        :param knowledge_base: The current knowledge base of KnowledgeStatement objects.
        :param subset_comparisons: The initial count of subset comparisons (default is 0).
        :return: A list of inferred KnowledgeStatement objects.
        """
        inferred_statements: List[KnowledgeStatement] = []

        sorted_knowledge_base = sorted(knowledge_base, reverse=True)

        for i, current_statement in enumerate(sorted_knowledge_base):
            for next_statement in sorted_knowledge_base[i + 1:]:
                subset_comparisons += 1
                if next_statement.get_cell_positions().issubset(current_statement.get_cell_positions()):
                    inferred_cells = current_statement.get_cell_positions() - next_statement.get_cell_positions()
                    inferred_count = current_statement.get_mine_count() - next_statement.get_mine_count()
                    new_inferred_statement = KnowledgeStatement(inferred_cells, inferred_count)
                    if new_inferred_statement not in inferred_statements:
                        inferred_statements.append(new_inferred_statement)
                else:
                    break

        self.stat_generator.update_subset_comparisons(subset_comparisons)
        self.stat_generator.update_inferences(len(inferred_statements))

        return inferred_statements

    def bfs_search(self, knowledge_base: List[KnowledgeStatement], subset_comparisons: int = 0) -> List[
        KnowledgeStatement]:
        """
        Perform a breadth-first search (BFS) to infer new KnowledgeStatements.

        :param knowledge_base: The current knowledge base of KnowledgeStatement objects.
        :param subset_comparisons: The initial count of subset comparisons (default is 0).
        :return: A list of inferred KnowledgeStatement objects.
        """
        # Sort by the size of cell positions to ensure we start with smaller, simpler sets
        sorted_knowledge_base = sorted(knowledge_base, key=lambda ks: len(ks.get_cell_positions()))
        root = TreeNode(sorted_knowledge_base)
        queue = deque([root])
        inferred_statements: List[KnowledgeStatement] = []
        visited = set()

        while queue:
            current_node = queue.popleft()
            current_kb = current_node.knowledge_base
            kb_key = tuple(sorted(tuple(ks.get_cell_positions()) for ks in current_kb))

            if kb_key in visited:
                continue
            visited.add(kb_key)

            # Iterate over the knowledge base statements at the current depth level
            for i, statement in enumerate(current_kb):
                for other_statement in current_kb[i + 1:]:
                    subset_comparisons += 1
                    if statement.get_cell_positions().issubset(other_statement.get_cell_positions()):
                        inferred_cells = other_statement.get_cell_positions() - statement.get_cell_positions()
                        inferred_count = other_statement.get_mine_count() - statement.get_mine_count()
                        new_inferred_statement = KnowledgeStatement(inferred_cells, inferred_count)
                        if new_inferred_statement not in inferred_statements:
                            inferred_statements.append(new_inferred_statement)
                            new_kb = current_kb + [new_inferred_statement]
                            new_node = TreeNode(new_kb, current_node)
                            current_node.add_child(new_node)
                            queue.append(new_node)  # Add the node to explore in subsequent BFS levels

        self.stat_generator.update_subset_comparisons(subset_comparisons)
        self.stat_generator.update_inferences(len(inferred_statements))

        return inferred_statements

    def dfs_search(self, knowledge_base: List[KnowledgeStatement], subset_comparisons: int = 0) -> List[
                   KnowledgeStatement]:
        """
        Perform a depth-first search (DFS) to infer new KnowledgeStatements.

        :param knowledge_base: The current knowledge base of KnowledgeStatement objects.
        :param subset_comparisons: The initial count of subset comparisons (default is 0).
        :return: A list of inferred KnowledgeStatement objects.
        """
        # Sort the knowledge base by size, prioritizing larger sets for deeper exploration
        sorted_knowledge_base = sorted(knowledge_base, key=lambda ks: -len(ks.get_cell_positions()))
        root = TreeNode(sorted_knowledge_base)
        stack = [root]
        inferred_statements: List[KnowledgeStatement] = []
        visited = set()

        while stack:
            current_node = stack.pop()
            current_kb = current_node.knowledge_base
            kb_key = tuple(sorted(tuple(ks.get_cell_positions()) for ks in current_kb))

            if kb_key in visited:
                continue
            visited.add(kb_key)

            # Iterate over the knowledge base statements to find subsets
            for i, statement in enumerate(current_kb):
                for other_statement in current_kb[i + 1:]:
                    subset_comparisons += 1
                    if statement.get_cell_positions().issubset(other_statement.get_cell_positions()):
                        inferred_cells = other_statement.get_cell_positions() - statement.get_cell_positions()
                        inferred_count = other_statement.get_mine_count() - statement.get_mine_count()

                        if inferred_count >= 0 and inferred_cells:  # Ensure valid and meaningful inference
                            new_inferred_statement = KnowledgeStatement(inferred_cells, inferred_count)
                            if new_inferred_statement not in inferred_statements:
                                inferred_statements.append(new_inferred_statement)
                                new_kb = current_kb + [new_inferred_statement]
                                new_node = TreeNode(new_kb, current_node)
                                current_node.add_child(new_node)
                                stack.append(new_node)  # Continue exploring this path

        self.stat_generator.update_subset_comparisons(subset_comparisons)
        self.stat_generator.update_inferences(len(inferred_statements))

        return inferred_statements


