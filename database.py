import sqlite3


class DatabaseManager:
    def __init__(self, db_name="chess_game.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Player_Responses (
                    name TEXT,
                    answer TEXT UNIQUE
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Solutions (
                    solution TEXT UNIQUE
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Program_Respond (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sequential INTEGER,
                    threaded INTEGER,
                    time_taken_seq REAL,
                    time_taken_thread REAL
                )
            """
            )

            conn.commit()

    def save_player_response(self, name, answer):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Player_Responses VALUES (?, ?)", (name, answer))
            conn.commit()

    def save_solution(self, solution):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Solutions VALUES (?)", (solution,))
            conn.commit()

    def save_performance_stats(self, s_count, t_count, s_time, t_time):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Program_Respond (sequential, threaded, time_taken_seq, time_taken_thread) VALUES (?,?,?,?)",
                (s_count, t_count, s_time, t_time),
            )
            conn.commit()

    # Helper methods to clear flag
    def get_total_solutions_count(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Solutions")
            return cursor.fetchone()[0]

    def get_player_solution_count(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM solutions")
            return cursor.fetchone()[0]

    def clear_player_responses(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM solutions")
            conn.commit()
