import time
import threading


class NQueensLogic:
    def __init__(self, size=16):
        self.size = size  # Define board dimensions (N x N)

    def is_valid(self, queens_array):
        """Checks for collisions between queens in rows, columns, or diagonals."""
        for i in range(len(queens_array)):  # index of first queen
            for j in range(i + 1, len(queens_array)):  # index of second queen
                r1, c1 = queens_array[i]
                r2, c2 = queens_array[j]
                # If rows match, cols match, or absolute diff of rows == absolute diff of cols (diagonal)
                if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                    return False
        return True

    def backtrack_solver(self, row, current_queens, results):
        """Depth-First Search (DFS) on the state-space tree."""
        if row == self.size:
            results[0] += 1  # Base case: All queens placed, increment solution counter
            return

        for col in range(self.size):
            temp_queens = current_queens + [(row, col)]
            # Pruning the tree: only recurse if the current placement is valid
            if self.is_valid(temp_queens):
                self.backtrack_solver(row + 1, temp_queens, results)

    def run_sequential(self):
        """Solves the puzzle using a single execution thread."""
        results = [0]
        start = time.time()
        self.backtrack_solver(0, [], results)
        return results[0], time.time() - start

    def run_threaded(self):
        """Parallelizes the search by assigning each starting column to a thread."""
        total_solutions = [0]
        lock = threading.Lock()  # Ensures thread-safe updates to the total counter
        threads = []
        start = time.time()

        def thread_task(start_col):
            local_res = [0]
            # Each thread handles one branch of the root node
            self.backtrack_solver(1, [(0, start_col)], local_res)
            with lock:
                total_solutions[0] += local_res[0]

        for c in range(self.size):
            t = threading.Thread(target=thread_task, args=(c,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()  # Wait for all threads to complete before returning

        return total_solutions[0], time.time() - start
