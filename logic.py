import time
import threading


class NQueensLogic:
    def __init__(self, size=16, max_solutions=20):
        self.size = size
        self.max_solutions = max_solutions

    def is_valid(self, queens):
        for i in range(len(queens)):
            for j in range(i + 1, len(queens)):
                r1, c1 = queens[i]
                r2, c2 = queens[j]
                if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                    return False
        return True

    # ---------------- SEQUENTIAL ----------------
    def run_sequential(self):
        count = 0
        solutions = []

        cols = set()
        diag1 = set()  # r - c
        diag2 = set()  # r + c

        board = []

        def backtrack(row):
            nonlocal count

            if count >= self.max_solutions:
                return

            if row == self.size:
                solutions.append(board.copy())
                count += 1
                return

            for col in range(self.size):
                if col in cols or (row - col) in diag1 or (row + col) in diag2:
                    continue

                cols.add(col)
                diag1.add(row - col)
                diag2.add(row + col)
                board.append((row, col))

                backtrack(row + 1)

                cols.remove(col)
                diag1.remove(row - col)
                diag2.remove(row + col)
                board.pop()

        start = time.time()
        backtrack(0)
        end = time.time()

        return count, end - start, solutions

    # ---------------- THREADED ----------------
    def run_threaded(self):
        total = 0
        solutions = []
        lock = threading.Lock()
        stop_event = threading.Event()

        start = time.time()

        def task(start_col):
            nonlocal total

            cols = {start_col}
            diag1 = {0 - start_col}
            diag2 = {0 + start_col}
            board = [(0, start_col)]

            def backtrack(row):
                nonlocal total

                if stop_event.is_set():
                    return

                if row == self.size:
                    with lock:
                        if total < self.max_solutions:
                            total += 1
                            solutions.append(board.copy())

                            if total >= self.max_solutions:
                                stop_event.set()
                    return

                for col in range(self.size):
                    if col in cols or (row - col) in diag1 or (row + col) in diag2:
                        continue

                    cols.add(col)
                    diag1.add(row - col)
                    diag2.add(row + col)
                    board.append((row, col))

                    backtrack(row + 1)

                    cols.remove(col)
                    diag1.remove(row - col)
                    diag2.remove(row + col)
                    board.pop()

            backtrack(1)

        threads = []
        for c in range(self.size):
            t = threading.Thread(target=task, args=(c,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        end = time.time()

        return total, end - start, solutions
