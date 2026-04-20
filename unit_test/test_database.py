import unittest
import sqlite3
import os
from database import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        # Use a temporary database file for isolated testing
        self.test_db = "test_chess.db"
        self.db = DatabaseManager(self.test_db)

    def tearDown(self):
        # Delete the test database after each test finishes
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_initialization_creates_tables(self):
        # Verify the tables exist
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            self.assertIn("Player_Responses", tables)
            self.assertIn("Solutions", tables)

    def test_save_and_get_player_response(self):
        # Test inserting and reading data
        self.db.save_player_response("Malinda", "0-0,1-2,2-4")
        count = self.db.get_player_solution_count()
        self.assertEqual(count, 1)

    def test_unique_constraint_on_answer(self):
        # Test that duplicate solutions raise an error
        self.db.save_player_response("Player1", "0-0,1-2")
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.save_player_response("Player2", "0-0,1-2")

    def test_clear_player_responses(self):
        self.db.save_player_response("Yash", "0-0,1-2")
        self.db.clear_player_responses()
        count = self.db.get_player_solution_count()
        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
