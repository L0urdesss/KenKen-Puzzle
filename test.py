
class KenAiSolver:
    def __init__(self,puzzle):
        self.puzzle = puzzle
    def solve_kenken(self,puzzle, size):
        def parse_input(puzzle):
            groups = []
            for group in puzzle:
                cells = group[:-2]
                operation = group[-2]
                total = group[-1]
                groups.append((cells, operation, total))
            return groups

        def is_valid(board, groups):
            for cells, operation, total in groups:
                values = [board[x][y] for x, y in cells if board[x][y] != 0]
                if len(values) == len(cells):
                    if not check_constraint(values, operation, total) and operation != "-" and total != 0:
                        return False
            return True

        def check_constraint(values, operation, total):
            if operation == '+':
                return sum(values) == total
            elif operation == '-':
                return abs(values[0] - values[1]) == total
            elif operation == '*':
                product = 1
                for value in values:
                    product *= value
                return product == total
            elif operation == '/':
                return max(values) / min(values) == total
            elif operation == ' ':
                return total
            return False

        def is_safe(board, row, col, num):
            # Check the row and column constraints
            for x in range(size):
                if board[row][x] == num or board[x][col] == num:
                    return False
            return True

        def backjumping(board, groups, row, col):
            if row == size:
                return board

            next_row, next_col = (row, col + 1) if col + 1 < size else (row + 1, 0)

            if board[row][col] != 0:
                return backjumping(board, groups, next_row, next_col)

            for num in range(1, size + 1):
                if is_safe(board, row, col, num):
                    board[row][col] = num
                    if is_valid(board, groups):
                        result = backjumping(board, groups, next_row, next_col)
                        if result:
                            return result
                    board[row][col] = 0

            return None

        groups = parse_input(puzzle)
        
        board = [[0] * size for _ in range(size)]
        solution = backjumping(board, groups, 0, 0)
        return solution


if __name__ == "__main__":
    # Example usage
    puzzle = [
        [(0, 1), (0, 0), (1, 0), '-', 0],
        [(0, 2), (1, 2),"-", 1],
        [(1,1)," ",1],
        [(2, 0), (2, 2),(2, 1), '+', 6],
    ]
    size = 3
    solver = KenAiSolver(puzzle)
    solution = solver.solve_kenken(puzzle, size)
    for row in solution:
        print(row)
