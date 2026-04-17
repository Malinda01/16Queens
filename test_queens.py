import os
import unittest
import sqlite3

from database import DatabaseManager
from logic import NQueensLogic


class TestNQueensLogic(unittest.TestCase):

    # ---------------------------
    # SOLVER TESTS (USE SMALL BOARD)
    # ---------------------------
    def test_sequential_solution_count(self):
        logic = NQueensLogic(size=4)
        solutions, time_taken = logic.run_sequential()

        self.assertEqual(solutions, 2)
        self.assertTrue(time_taken >= 0)

    def test_threaded_equals_sequential(self):
        logic = NQueensLogic(size=4)

        seq_solutions, _ = logic.run_sequential()
        thr_solutions, _ = logic.run_threaded()

        self.assertEqual(seq_solutions, thr_solutions)

    # ---------------------------
    # VALIDATION TESTS
    # ---------------------------
    def test_valid_placement(self):
        logic = NQueensLogic(size=8)
        queens = [(0, 0), (1, 4), (2, 7), (3, 5), (4, 2), (5, 6), (6, 1), (7, 3)]

        self.assertTrue(logic.is_valid(queens))

    def test_invalid_same_row(self):
        logic = NQueensLogic(size=8)
        self.assertFalse(logic.is_valid([(0, 0), (0, 5)]))

    def test_invalid_same_column(self):
        logic = NQueensLogic(size=8)
        self.assertFalse(logic.is_valid([(0, 2), (5, 2)]))

    def test_invalid_diagonal(self):
        logic = NQueensLogic(size=8)
        self.assertFalse(logic.is_valid([(0, 0), (1, 1)]))

    # ---------------------------
    # PLAYER SIMULATION (10 USERS)
    # ---------------------------
    def test_10_users_attempts(self):
        logic = NQueensLogic(size=8)

        max_solutions = 92

        users = {
            "User1": [(0, 0), (1, 4), (2, 7), (3, 5), (4, 2), (5, 6), (6, 1), (7, 3)],
            "User2": [(0, 1), (1, 3), (2, 5), (3, 7), (4, 2), (5, 0), (6, 6), (7, 4)],
            "User3": [(0, 2), (1, 5), (2, 7), (3, 0), (4, 3), (5, 6), (6, 4), (7, 1)],
            "User4": [(0, 3), (1, 6), (2, 0), (3, 7), (4, 4), (5, 1), (6, 5), (7, 2)],
            "User5": [(0, 4), (1, 6), (2, 1), (3, 5), (4, 2), (5, 0), (6, 3), (7, 7)],
            "User6": [(0, 5), (1, 2), (2, 6), (3, 1), (4, 3), (5, 7), (6, 4), (7, 0)],
            "User7": [(0, 6), (1, 3), (2, 1), (3, 7), (4, 5), (5, 0), (6, 2), (7, 4)],
            "User8": [(0, 7), (1, 1), (2, 3), (3, 0), (4, 6), (5, 4), (6, 2), (7, 5)],
            "User9": [(0, 0), (1, 1), (2, 2), (3, 3)],  # invalid
            "User10": [(0, 0), (1, 4), (2, 7), (3, 5), (4, 2), (5, 6), (6, 1), (7, 3)],
        }

        valid_count = 0
        for placement in users.values():
            if logic.is_valid(placement):
                valid_count += 1

        self.assertTrue(valid_count <= max_solutions)

    # ---------------------------
    # DATABASE TESTS
    # ---------------------------
    def test_save_player_response(self):
        db = DatabaseManager("test_db.db")

        name = "TestUser"
        answer = str([(0, 0), (1, 2)])

        db.save_player_response(name, answer)

        conn = sqlite3.connect("test_db.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Player_Responses WHERE name=?", (name,))
        result = cursor.fetchone()

        self.assertIsNotNone(result)

        conn.close()

    def test_duplicate_solution(self):
        db = DatabaseManager("test_db.db")

        answer = str([(0, 0), (1, 2)])

        db.save_player_response("User1", answer)

        with self.assertRaises(sqlite3.IntegrityError):
            db.save_player_response("User2", answer)

    def test_save_performance(self):
        db = DatabaseManager("test_db.db")

        db.save_performance_stats(10, 10, 0.5, 0.3)

        conn = sqlite3.connect("test_db.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Program_Respond")
        result = cursor.fetchone()

        self.assertIsNotNone(result)

        conn.close()


# ---------------------------
# RUN TESTS
# ---------------------------
if __name__ == "__main__":
    unittest.main()
