import random

board_size = 3
subgrid = 1

class KenPuzzleMaker:
    def __init__(self,board_size):
        self.board = [[0] * board_size for _ in range(board_size)]
        self.random = random.Random()
        self.groups = {}

    def generate_answer_board(self,board_size , subgrid):
        self.initialize_board(board_size)
        self.fill_board(0, 0 ,subgrid ,board_size)
        self.group_cells()
        self.print_board()
        self.print_groups()
        self.print_board_coord()

    def initialize_board(self,board_size):
        self.board = [[0] * board_size for _ in range(board_size)]

    def fill_board(self, row, col , subgrid, board_size):
        if row == board_size:
            return True
        if col == board_size:
            return self.fill_board(row + 1, 0 , subgrid, board_size)
        
        possible_numbers = self.get_possible_numbers(row, col , subgrid , board_size)
        while possible_numbers:
            num = self.random.choice(possible_numbers)
            self.board[row][col] = num
            if self.fill_board(row, col + 1, subgrid , board_size):
                return True
            self.board[row][col] = 0
            possible_numbers.remove(num)
        return False

    def get_possible_numbers(self, row, col ,subgrid, board_size):
        possible_numbers = []
        for num in range(1, board_size + 1):
            if self.is_valid_move(row, col, num , subgrid,board_size):
                possible_numbers.append(num)
        return possible_numbers
    
    def is_valid_move(self, row, col, num, subgrid,board_size):
        # Check row and column constraints
        for i in range(board_size):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False
        
        # Check subgrid constraints
        start_row = row - row % subgrid
        start_col = col - col % (board_size // subgrid)
        for i in range(subgrid):
            for j in range(board_size // subgrid):
                if self.board[i + start_row][j + start_col] == num:
                    return False
        return True

    def group_cells(self):
        group_number = 1
        for i in range(board_size):
            for j in range(board_size):
                if group_number not in self.groups:
                    self.groups[group_number] = []
                if not self.is_coordinate_in_any_group((i, j)) and (i, j) not in self.groups[group_number]:
                    self.groups[group_number].append((i, j))
                else:
                    if group_number in self.groups and len(self.groups[group_number]) != 0:
                        group_number += 1
                    continue
                group_size = self.random.randint(2, (subgrid * 2) + 1)
                for m in range(i + 1, board_size):
                    if self.random.random() < 0.5:
                        if not self.is_coordinate_in_any_group((m, j)) and (m, j) not in self.groups[group_number]:
                            self.groups[group_number].append((m, j))
                        if len(self.groups[group_number]) >= group_size or m == board_size - 1:
                            break
                    else:
                        break
                if len(self.groups[group_number]) >= group_size:
                    group_number += 1
        if group_number in self.groups and len(self.groups[group_number]) != 0:
            group_number += 1

    def is_coordinate_in_any_group(self, coordinate):
        for group in self.groups.values():
            if coordinate in group:
                return True
        return False

    def get_board_value(self, x, y):
        print(x, " and " , y)
        return self.board[x][y]

    def print_board(self):
        for row in self.board:
            print(' '.join(map(str, row)))

    def print_board_coord(self):
        for i in range(board_size):
            for j in range(board_size):
                print(f'({i},{j})', end=' ')
            print()

    def add_1_plus_to_list(self, cells):
        board_values_array = []
        print("cells: ",cells)
        for cell in cells:
            num = self.get_board_value(*cell)
            board_values_array.append((*cell, num, 1, "+"))
        return board_values_array

    def print_groups(self):
        for group_number, group in self.groups.items():
            if not group:
                continue
            print(f"Group {group_number}:")
            board_values_array = self.add_1_plus_to_list(group)
            board_values_array.sort(key=lambda x: x[2], reverse=True)
            total = sum(cell[2] for cell in board_values_array)
            difference = board_values_array[0][2] - sum(cell[2] for cell in board_values_array[1:])
            quotient = total / len(board_values_array)
            product = 1
            for cell in board_values_array:
                product *= cell[2]
            operation = ""
            if len(group) == 2 and quotient.is_integer():
                random_operation = self.random.randint(0, 3)
            elif difference < 0:
                random_operation = self.random.randint(0, 1)
            else:
                random_operation = self.random.randint(0, 2)
            if random_operation == 0:
                operation = "+"
                total = sum(cell[2] for cell in board_values_array)
            elif random_operation == 1:
                operation = "*"
                total = product
            elif random_operation == 2:
                operation = "-"
                total = difference
            elif random_operation == 3:
                operation = "/"
                total = int(quotient)
            if len(group) == 1:
                operation = " "
                total = 0
            for cell in board_values_array:
                print(f"Cell ({cell[0]}, {cell[1]}) {cell[2]} {operation} {total}")
            print()

if __name__ == "__main__":
    solver = KenPuzzleMaker(board_size)
    solver.generate_answer_board(3,1)
