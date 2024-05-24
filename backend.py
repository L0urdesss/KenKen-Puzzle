import random


class KenPuzzleMaker:
    def __init__(self,board_size):
        self.board = [[0] * board_size for _ in range(board_size)]
        self.random = random.Random()
        self.groups = {}
        self.groupwithnumber = []
        self.groupwithval = []
        self.op = None

    def generate_answer_board(self,board_size , subgrid):
        self.initialize_board(board_size)
        self.fill_board(0, 0 ,subgrid ,board_size)
        self.group_cells(board_size,subgrid)
        self.getEachGroups()
        self.print_board()
        self.print_board_coord(board_size)
        self.print_group_cells()

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

    def group_cells(self,board_size,subgrid):
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

    def print_board(self):
        for row in self.board:
            print(' '.join(map(str, row)))

    def print_board_coord(self,board_size):
        for i in range(board_size):
            for j in range(board_size):
                print(f'({i},{j})', end=' ')
            print()
    
    def getGroupVal(self,group,ops):
        if not group:
            return 0, ""
        possible_ops = ["+", "+-", "*/", "+-*/"]
        print("ops: ",ops)
        board_values_array = self.add_1_plus_to_list(group)
        board_values_array.sort(key=lambda x: x[2], reverse=True)
        total = sum(cell[2] for cell in board_values_array)
        difference = board_values_array[0][2] - sum(cell[2] for cell in board_values_array[1:])
        numerator = board_values_array[0][2]
        denominator = sum(cell[2] for cell in board_values_array[1:])
        if denominator != 0:
            quotient = numerator / denominator
        else:
            quotient = float('inf')  
        product = 1
        for cell in board_values_array:
            product *= cell[2]

        operation = ""

        if ops == "?":
            ops = random.choice(possible_ops)
        
        if '/' in ops and not (len(group) == 2 and quotient.is_integer()):
            ops = ops.replace('/', '')

        # Remove '-' if the difference condition is not met
        print("difference: ",difference)
        print("before: ",ops)
        if '-' in ops and difference < 0:
            print("got it")
            ops = ops.replace('-', '')
        print("after: ",ops )
        # Randomly select an operation from the remaining ops string
        random_operation = ops[self.random.randint(0, len(ops) - 1)]
        print("random_op: ",random_operation)
            
        if random_operation == "+":
            total = sum(cell[2] for cell in board_values_array)
            operation = "+"
        elif random_operation == "*":
            total = product
            operation = "*"
        elif random_operation == "-":
            total = difference
            operation = "-"
        elif random_operation == "/":
            total = int(quotient)
            operation = "/"

        if len(group) == 1:
            total = board_values_array[0][2]
            operation = " "
        # print("in grouping")
        # print(group)
        # print(total)
        # print(operation)
        return total, operation        

    def updateOp(self,operation):
        print("op inside: ",operation)
        self.op = operation
        print("updated op inside: ",self.op)

    def getEachGroups(self):
        self.groupwithval.clear()  # Clear the existing values
        for group_number, group in self.groups.items():
            if not group:
                continue

            print("selfop: ",self.op)
            total, operation = self.getGroupVal(group,self.op)

            board_values_array = self.add_1_plus_to_list(group)
            board_values_array.sort(key=lambda x: x[2], reverse=True)
            for cell in board_values_array:
                self.groupwithval.append([(cell[0], cell[1]), cell[2], operation, total])

    def print_group_cells(self):
        for group_number, cells in self.groups.items():
            if not cells:
                continue
            print(f"Group {group_number}:")
            group_output = self.groupwithval
            for cell_data in group_output:
                if (cell_data[0][0], cell_data[0][1]) in cells:
                    print(f"{cell_data[0]}, {cell_data[1]}, {cell_data[2]}, {cell_data[3]}")

    def getAllGroups(self):
        output = []
        for group_number, cells in self.groups.items():
            if not cells:
                continue
            group = []
            total = 0
            op = ""
            group_output = self.groupwithval
            for cell_data in group_output:
                if (cell_data[0][0], cell_data[0][1]) in cells:
                    group.append((cell_data[0]))
                    op = cell_data[2]
                    total = cell_data[3]
            group.sort()  
            group.append(op)
            group.append(total) 
            output.append(group)
        return output
    
    def add_1_plus_to_list(self, cells):
        board_values_array = []
        for cell in cells:
            num = self.get_board_value(*cell)
            board_values_array.append((*cell, num, 1, "+"))
        return board_values_array

    def get_board_value(self, x, y):
        return self.board[x][y]
    
# if __name__ == "__main__":
#     solver = KenPuzzleMaker(board_size)
#     solver.generate_answer_board(board_size,subgrid)
#     getgroups = solver.getAllGroups()
#     print("each group: ",solver.groupwithval)
#     print("all groups: ",getgroups)


