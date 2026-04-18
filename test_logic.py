import unittest
import sqlite3
from database import DatabaseManager


class TestInsertMainDB(unittest.TestCase):

    def setUp(self):
        # 🔥 USE MAIN DATABASE
        self.db = DatabaseManager("chess_game.db")

        # OPTIONAL: clear before test (comment if you want to keep old data)
        with sqlite3.connect(self.db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Player_Responses")
            conn.commit()

    def test_insert_20_answers(self):

        solutions = [
            # Your given ones
            (
                "Malinda",
                [(0, 0), (1, 2), (2, 4), (3, 6), (4, 8), (5, 10), (6, 12), (7, 14)],
            ),
            (
                "Greshan",
                [(0, 15), (1, 13), (2, 11), (3, 9), (4, 7), (5, 5), (6, 3), (7, 1)],
            ),
            # 18 more
            ("P1", [(0, 1), (1, 3), (2, 5), (3, 7), (4, 9), (5, 11), (6, 13), (7, 15)]),
            ("P2", [(0, 2), (1, 4), (2, 6), (3, 8), (4, 10), (5, 12), (6, 14), (7, 0)]),
            ("P3", [(0, 3), (1, 5), (2, 7), (3, 9), (4, 11), (5, 13), (6, 15), (7, 1)]),
            ("P4", [(0, 4), (1, 6), (2, 8), (3, 10), (4, 12), (5, 14), (6, 0), (7, 2)]),
            ("P5", [(0, 5), (1, 7), (2, 9), (3, 11), (4, 13), (5, 15), (6, 1), (7, 3)]),
            ("P6", [(0, 6), (1, 8), (2, 10), (3, 12), (4, 14), (5, 0), (6, 2), (7, 4)]),
            ("P7", [(0, 7), (1, 9), (2, 11), (3, 13), (4, 15), (5, 1), (6, 3), (7, 5)]),
            ("P8", [(0, 8), (1, 10), (2, 12), (3, 14), (4, 0), (5, 2), (6, 4), (7, 6)]),
            ("P9", [(0, 9), (1, 11), (2, 13), (3, 15), (4, 1), (5, 3), (6, 5), (7, 7)]),
            (
                "P10",
                [(0, 10), (1, 12), (2, 14), (3, 0), (4, 2), (5, 4), (6, 6), (7, 8)],
            ),
            (
                "P11",
                [(0, 11), (1, 13), (2, 15), (3, 1), (4, 3), (5, 5), (6, 7), (7, 9)],
            ),
            (
                "P12",
                [(0, 12), (1, 14), (2, 0), (3, 2), (4, 4), (5, 6), (6, 8), (7, 10)],
            ),
            (
                "P13",
                [(0, 13), (1, 15), (2, 1), (3, 3), (4, 5), (5, 7), (6, 9), (7, 11)],
            ),
            (
                "P14",
                [(0, 14), (1, 0), (2, 2), (3, 4), (4, 6), (5, 8), (6, 10), (7, 12)],
            ),
            (
                "P15",
                [(0, 15), (1, 1), (2, 3), (3, 5), (4, 7), (5, 9), (6, 11), (7, 13)],
            ),
            ("P16", [(0, 1), (1, 4), (2, 7), (3, 10), (4, 13), (5, 0), (6, 3), (7, 6)]),
            ("P17", [(0, 2), (1, 5), (2, 8), (3, 11), (4, 14), (5, 1), (6, 4), (7, 7)]),
            ("P18", [(0, 3), (1, 6), (2, 9), (3, 12), (4, 15), (5, 2), (6, 5), (7, 8)]),
        ]

        inserted = 0

        for name, sol in solutions:
            try:
                self.db.save_player_response(name, str(sorted(sol)))
                inserted += 1
            except sqlite3.IntegrityError:
                print(f"Duplicate skipped: {sol}")

        count = self.db.get_player_solution_count()

        print(f"\nInserted: {inserted}")
        print(f"Total in DB: {count}")

        self.assertEqual(count, 20)


if __name__ == "__main__":
    unittest.main()
