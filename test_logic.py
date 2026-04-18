import unittest
from logic import NQueensLogic


class TestNQueens(unittest.TestCase):

    def test_valid_solution(self):
        logic = NQueensLogic(4)
        sol = [(0, 1), (1, 3), (2, 0), (3, 2)]
        self.assertTrue(logic.is_valid(sol))

    def test_invalid_solution(self):
        logic = NQueensLogic(4)
        sol = [(0, 0), (1, 1)]
        self.assertFalse(logic.is_valid(sol))

    def test_sequential(self):
        logic = NQueensLogic(4, max_solutions=10)
        count, time_taken, _ = logic.run_sequential()
        self.assertEqual(count, 2)

    def test_threaded(self):
        logic = NQueensLogic(4, max_solutions=10)
        count, time_taken, _ = logic.run_threaded()
        self.assertEqual(count, 2)


if __name__ == "__main__":
    unittest.main()
