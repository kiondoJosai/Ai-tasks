import random
import time



def count_conflicts(board):
   
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j]:                  
                conflicts += 1
            if abs(board[i] - board[j]) == abs(i - j):  
                conflicts += 1
    return conflicts




def random_board(n):
    
    return [random.randint(0, n - 1) for _ in range(n)]


def best_neighbour(board):
    
    n = len(board)
    current_conflicts = count_conflicts(board)
    best_board = board[:]
    best_conflicts = current_conflicts

    for col in range(n):
        original_row = board[col]
        for row in range(n):
            if row == original_row:
                continue
            board[col] = row
            c = count_conflicts(board)
            if c < best_conflicts:
                best_conflicts = c
                best_board = board[:]
        board[col] = original_row  

    return best_board, best_conflicts




def hill_climbing(n, max_sideways=100):
    
    board = random_board(n)
    conflicts = count_conflicts(board)
    sideways = 0

    while conflicts > 0:
        neighbour, neighbour_conflicts = best_neighbour(board)

        if neighbour_conflicts > conflicts:
           
            return None

        if neighbour_conflicts == conflicts:
            sideways += 1
            if sideways > max_sideways:
                return None  #
        else:
            sideways = 0

        board = neighbour
        conflicts = neighbour_conflicts

    return board  


def random_restart_hill_climbing(n, max_restarts=1000, max_sideways=100):
    
    start_time = time.time()

    for attempt in range(1, max_restarts + 1):
        solution = hill_climbing(n, max_sideways)
        if solution is not None:
            elapsed = time.time() - start_time
            return solution, attempt, elapsed

    elapsed = time.time() - start_time
    return None, max_restarts, elapsed



def print_board(board):
   
    n = len(board)
    separator = "+" + ("---+" * n)
    print(separator)
    for row in range(n):
        line = "|"
        for col in range(n):
            line += " Q |" if board[col] == row else "   |"
        print(line)
        print(separator)



def solve(n):
    print(f"\n{'='*50}")
    print(f"  N-Queens Hill Climbing  (N = {n})")
    print(f"{'='*50}")

    solution, restarts, elapsed = random_restart_hill_climbing(n)

    if solution:
        print(f"\n✓ Solution found in {restarts} restart(s)  ({elapsed:.4f}s)")
        print(f"  Board encoding (column → row): {solution}")
        print(f"  Conflicts remaining: {count_conflicts(solution)}\n")
        if n <= 20:
            print_board(solution)
    else:
        print("\n✗ No solution found within the restart limit.")


if __name__ == "__main__":
    for size in [8, 12, 20]:
        solve(size)
