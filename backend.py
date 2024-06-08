import random


class KenPuzzleMaker:
    def __init__(self,board_size):
        self.board = [[0] * board_size for _ in range(board_size)]
        self.random = random.Random()
        self.groups = {}
        self.groupwithnumber = []
        self.groupwithval = []
        self.solver_group = []
        self.op = None
        self.size = board_size
    def generate_answer_board(self,board_size , subgrid):
        self.initialize_board(board_size)
        self.fill_board(0, 0 ,subgrid ,board_size)
        self.group_cells(board_size,subgrid)
        self.getEachGroups()
        self.print_board()
        self.print_board_coord(board_size)
        self.print_group_cells()
    
    def generate_empty_board(self):
        self.initialize_board(self.size)
        self.print_board()
        self.print_board_coord(self.size)
        
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
    
    def add_group(self,group):
        sort = sorted(group)
        self.solver_group.append(sort)
    
    def find_group(self,target_cell):
        for group in self.solver_group:
            for cell in group:
                if target_cell == cell:
                    return group
        return None

    def findGroup(self, target_group):
        print("target inside find: ", target_group)
        print("group self: ",self.solver_group)
        for item in self.solver_group:
            print("Current item:", item)
            print("itemchecked: ",item[:-2])
            if item[:-2] == target_group:
                print("FOUND")
                return item
        return None
    
    def generate_tuples(self,grid_size):
        return [(i, j) for i in range(grid_size) for j in range(grid_size)]

    def check_tuples_in_group(self, grid_size, puzzle):
        # Generate all tuples for the given grid size
        required_tuples = self.generate_tuples(grid_size)
        
        # Initialize a set to keep track of missing tuples
        missing_tuples = set()
        
        # Iterate over each required tuple
        for item in required_tuples:
            found = False
            # Check if the tuple is present in any of the sub-arrays
            for sub_array in puzzle:
                if item in sub_array:
                    found = True
                    # Check if the sub-array has more than one tuple
                    if sum(isinstance(i, tuple) for i in sub_array) > 1:
                        # If it has more than one tuple, check both conditions
                        if isinstance(sub_array[-2], int) and sub_array[-1] in ['+', '-', '/', '*']:
                            # All conditions are met, break out of the inner loop
                            break
                        else:
                            # If found but conditions are not met, add to missing_tuples
                            missing_tuples.add(item)
                            break
                    else:
                        # If it has only one tuple, check only the integer condition
                        if len(sub_array) == 1:
                            missing_tuples.add(item)
                            break    

                        if isinstance(sub_array[-2], int):
                            # All conditions are met, break out of the inner loop
                            break
                        else:
                            # If found but conditions are not met, add to missing_tuples
                            missing_tuples.add(item)
                            break
            
            if not found:
                # If not found, add it to the missing_tuples set
                missing_tuples.add(item)
        
        # If there are missing tuples, return False and the missing tuples
        if missing_tuples:
            return False, list(missing_tuples)
        
        # If all tuples are found with the required conditions, return True
        return True, []


    def removeGroup(self, group):
        target_group = self.findGroup(group)
        for item in self.solver_group:
            if item == group:
                self.solver_group.remove(group)
            elif target_group == item:
                self.solver_group.remove(target_group)
                
    def getGroupOp(self,target_group):
        for group in self.solver_group:
            print("groups: ",group)
            print("targetgroups: ",target_group)
            if target_group == group:
                print("found")
                return group[-1]
        return ""
    
    def getGroupTotal(self,target_group):
        for group in self.solver_group:
            print("groups: ",group)
            print("targetgroups: ",target_group)
            if target_group == group:
                print("found")
                return group[-2]
        return 0
    
    def find_group_coordinates(self,target_cell):
        tuple_array = []
        for group in self.solver_group:
            if target_cell in group:
                tuple_array = [item for item in group if isinstance(item, tuple)]
                return tuple_array
        return None

    def update_group(self, group, total, operation):
        for row in self.solver_group:
            if set(group) == set(row[:len(group)]):  # Ensure group matches part of the row
                total_updated = False
                operation_updated = False
                
                for i, item in enumerate(row[len(group):], start=len(group)):
                    if isinstance(item, int):
                        row[i] = total
                        total_updated = True
                    if isinstance(item, str):
                        row[i] = operation
                        operation_updated = True
                
                if not total_updated:
                    row.append(total)
                
                if not operation_updated:
                    row.append(operation)
                
                break

class KenAiSolver:
    def __init__(self, puzzle, draw_update):
        self.puzzle = puzzle
        self.draw_update = draw_update

    def solve_kenken(self, size):
        def parse_input(puzzle):
            groups = []
            for group in puzzle:
                cells = group[:-2]
                total = group[-2]
                operation = group[-1]
                groups.append((cells, operation, total))
            return groups

        def is_valid(board, groups):
            for cells, operation, total in groups:
                values = [board[x][y] for x, y in cells if board[x][y] != 0]
                if len(values) == len(cells):
                    if not check_constraint(values, operation, total):
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
            elif operation == '':
                return values[0] == total
            return False

        def is_safe(board, row, col, num):
            for x in range(size):
                if board[row][x] == num or board[x][col] == num:
                    return False
            return True

        def algorithm(board, groups, row, col):
            if row == size:
                return board, None

            next_row, next_col = (row, col + 1) if col + 1 < size else (row + 1, 0)

            if board[row][col] != 0:
                return algorithm(board, groups, next_row, next_col)

            for num in range(1, size + 1):
                if is_safe(board, row, col, num):
                    board[row][col] = num
                    # self.draw_update(board)
                    if is_valid(board, groups):
                        result, conflict_var = algorithm(board, groups, next_row, next_col)
                        if result:
                            return result, None
                    board[row][col] = 0
                    # self.draw_update(board)

            # If no valid number can be placed, backjump to the most recent conflict variable
            return None, (row, col)

        def backjump(board, groups, row, col):
            conflict_row, conflict_col = row, col
            while conflict_row is not None and conflict_col is not None:
                result, conflict_var = algorithm(board, groups, conflict_row, conflict_col)
                if result:
                    return result
                if conflict_var is None:
                    break
                conflict_row, conflict_col = conflict_var
            return None

        groups = parse_input(self.puzzle)
        board = [[0] * size for _ in range(size)]
        solution = backjump(board, groups, 0, 0)
        return solution

        
# if __name__ == "__main__":
#     puzzle = [
#         [(1, 0), (0, 0), 3, '*'],
#         [(2, 0), 2,''],
#         [(0,1), (0,2), 3, '+'],
#         [(1, 1), (2, 1), 3, '/'],
#         [(1, 2), 2, ''],
#         [(2, 2), 3, ''],

#     ]
#     def draw_update(board):
#         for row in board:
#             print(row)
#         print()

#     solver = KenAiSolver(puzzle, draw_update)
#     solution = solver.solve_kenken(3)
#     print("Solution:")
#     for row in solution:
#         print(row)

    # solver = KenPuzzleMaker(6)
    # solver.updateOp("*/")
    # getgroups = solver.getAllGroups()
    # solver.generate_answer_board(6,3)
    # print("each group: ",solver.groupwithval)
    # print("all groups: ",getgroups)
    # print("group: ",solver.groups)

    # solver = KenPuzzleMaker(6)
    # solver.generate_empty_board()
    # group1 = [(0,1),(0,2)]
    # group2 = [(2,1),(2,2)]
    # group3 = [(0,1)]
    # solver.add_group(group1)
    # solver.add_group(group2)

    # print("update1: ",solver.solver_group)
    # solver.update_group(group3,10,"+")
    # solver.update_group(group2,20,"/")
    # solver.update_group(group1,20,"-")
    # print("update2: ",solver.solver_group)

    # solver.update_group(group1,30,"*")

    # print("update3: ",solver.solver_group)
    
    # found = solver.find_group((0,1))
    # print("update3.5: ",found)

    # group = solver.findGroup([(0,1),(0,2)])
    # print("update4: ",group)
    # groupop = solver.getGroupOp(group)
    # print("update5: ",groupop)


    # size = 3
    # ai = KenAiSolver(puzzle)
    # solution = ai.solve_kenken(size)
    # for row in solution:
    #     print(row)

