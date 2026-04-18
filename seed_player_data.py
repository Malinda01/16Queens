import sqlite3
import random

DB_NAME = "chess_game.db"


def generate_solution():
    """
    Generate a fake (but unique-looking) 8-queen placement.
    Format: "r-c,r-c,..."
    NOTE: Doesn't need to be valid for testing DB behavior.
    """
    positions = set()

    while len(positions) < 8:
        r = random.randint(0, 15)
        c = random.randint(0, 15)
        positions.add((r, c))

    return ",".join([f"{r}-{c}" for r, c in sorted(positions)])


def seed_player_responses():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    inserted = 0
    attempts = 0

    while inserted < 30:
        name = f"Player_{inserted+1}"
        answer = generate_solution()

        try:
            cursor.execute(
                "INSERT INTO Player_Responses (name, answer) VALUES (?, ?)",
                (name, answer),
            )
            inserted += 1
        except sqlite3.IntegrityError:
            # Skip duplicates
            pass

        attempts += 1
        if attempts > 200:  # safety break
            break

    conn.commit()
    conn.close()

    print(f"✅ Inserted {inserted} records into Player_Responses")


if __name__ == "__main__":
    seed_player_responses()
