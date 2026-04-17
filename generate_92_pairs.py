# generate_92_pairs.py


def is_valid(queens):
    for i in range(len(queens)):
        for j in range(i + 1, len(queens)):
            r1, c1 = i, queens[i]
            r2, c2 = j, queens[j]

            if c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                return False
    return True


def solve_n_queens(n):
    solutions = []

    def backtrack(row, current):
        if row == n:
            solutions.append(current[:])
            return

        for col in range(n):
            current.append(col)
            if is_valid(current):
                backtrack(row + 1, current)
            current.pop()

    backtrack(0, [])
    return solutions


# Convert to (row, col) pairs
def convert_to_pairs(solution):
    return [(row, col) for row, col in enumerate(solution)]


# Generate solutions
solutions = solve_n_queens(8)

print(f"Total solutions: {len(solutions)}")  # 92


# Save to Python file
with open("solutions_8queens_pairs.py", "w") as f:
    f.write("solutions = [\n")
    for sol in solutions:
        pairs = convert_to_pairs(sol)
        f.write(f"    {pairs},\n")
    f.write("]\n")

print("Saved as pairs in solutions_8queens_pairs.py")
