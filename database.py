import sqlite3


class DatabaseManager:
    def __init__(self, db_name="chess_game.db"):
        self.db_name = db_name
        self.init_db()  # Initialize tables upon instantiation

    def init_db(self):
        # Establish connection to the SQLite file
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Create table for player solutions with a UNIQUE constraint on the answer string
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS Player_Responses (name TEXT, answer TEXT UNIQUE)"
            )
            # Create table for performance benchmarking results
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS Program_Respond 
                              (id INTEGER PRIMARY KEY AUTOINCREMENT, sequential INTEGER, 
                               threaded INTEGER, num_of_max_solutions INTEGER, 
                               time_taken_seq REAL, time_taken_thread REAL)"""
            )
            conn.commit()

    def save_player_response(self, name, sorted_ans):
        # Persist a specific player's valid Queen placement
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Player_Responses VALUES (?, ?)", (name, sorted_ans)
            )
            conn.commit()

    def save_performance_stats(self, s_count, t_count, s_time, t_time):
        # Persist the timing results from the performance test
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Program_Respond (sequential, threaded, num_of_max_solutions, time_taken_seq, time_taken_thread) VALUES (?,?,?,?,?)",
                (s_count, t_count, s_count, s_time, t_time),
            )
            conn.commit()
