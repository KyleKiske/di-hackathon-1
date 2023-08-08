class Figure:
    def __init__(self, color = 'white', x_pos = 0, y_pos = 0) -> None:
        if not (0 <= x_pos <= 7) or not (0 <= y_pos <= 7):
            print('invalid placement of figure')
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.moved = False
        self.notation = ""
        self.route = []
        self.name = ""
    def can_move(self, input: tuple) -> bool:
        if (input[0] == self.x_pos and input[1] == self.y_pos):
            print('invalid move, figure stays in its place.')
            return False
        return True

class Pawn(Figure):
    def __init__(self, color, grid: list[list], x_pos = 0, y_pos = 0) -> None:
        super().__init__(color, x_pos, y_pos)
        self.route = []
        if self.color == 'white':
            self.notation = 'P'
        else :
            self.notation = 'p'
        self.attacked_fields = self.calculate_attacked_fields(grid)
        self.name = "Pawn"
    def calculate_attacked_fields(self, grid):
        self.attacked_fields = []
        if self.color == 'white':
            if (self.x_pos - 1 >= 0) and (self.y_pos + 1 <= 7):
                self.attacked_fields.append(tuple([self.x_pos - 1, self.y_pos + 1]))
            if (self.x_pos - 1 >= 0) and (self.y_pos - 1 >= 0):            
                self.attacked_fields.append(tuple([self.x_pos - 1, self.y_pos - 1]))
        if self.color == 'black':
            if (self.x_pos + 1 <= 7) and (self.y_pos + 1 <= 7):
                self.attacked_fields.append(tuple([self.x_pos + 1, self.y_pos + 1]))
            if (self.x_pos + 1 <= 7) and (self.y_pos - 1 >= 0):            
                self.attacked_fields.append(tuple([self.x_pos + 1, self.y_pos - 1]))
        return self.attacked_fields
    def can_move(self, input: tuple) -> bool:
        self.route = []
        if not (super().can_move(input)):
            return False
        if self.color == 'white':
            if self.x_pos < input[0]:
                print("Pawn can't move backwards.")
                return False
            if not self.moved:
                if abs(self.x_pos - input[0]) > 2:
                    return False
            else:
                if abs(self.x_pos - input[0]) > 1:
                    return False
        else:
            if self.x_pos > input[0]:
                print("Pawn can't move backwards.")
                return False
            if not self.moved:
                if abs(self.x_pos - input[0]) > 2:
                    return False
            else:
                if abs(self.x_pos - input[0]) > 1:
                    return False
        if abs(self.x_pos - input[0]) == 2:
            self.route.append(tuple([(self.x_pos + input[0]) // 2, self.y_pos]))
            return True
        return True

class Knight(Figure):
    def __init__(self, color, grid: list[list], x_pos = 0, y_pos = 0) -> None:
        super().__init__(color, x_pos, y_pos)
        if self.color == 'white':
            self.notation = 'N'
        else :
            self.notation = 'n'
        self.attacked_fields = self.calculate_attacked_fields(grid)
        self.name = "Knight"
    def calculate_attacked_fields(self, grid):
        self.attacked_fields = []
        for i in (-2, -1, 1, 2):
            for j in (-2, -1, 1, 2):
                if abs(i * j) == 2:
                    if (7 >= self.x_pos + i >= 0) and (7 >= self.y_pos + j >= 0):
                        self.attacked_fields.append(tuple([self.x_pos + i, self.y_pos + j]))
        return self.attacked_fields
    def can_move(self, input: tuple) -> bool:
        if not (super().can_move(input)):
            return False
        elif abs(self.x_pos - input[0]) * abs(self.y_pos - input[1]) != 2:
            print('invalid move, knight can\'t go like this.')
            return False
        if not self.moved:
            self.moved = True
        return True
    
    pass

class Bishop(Figure):
    def __init__(self, color, grid: list[list], x_pos = 0, y_pos = 0, ) -> None:
        super().__init__(color, x_pos, y_pos)
        self.route = []
        if self.color == 'white':
            self.notation = 'B'
        else :
            self.notation = 'b'
        self.attacked_fields = self.calculate_attacked_fields(grid)
        self.name = "Bishop"
    def calculate_attacked_fields(self, grid: list[list]):
        self.attacked_fields = []
        for i in range(1, 8):
            j = i
            if (7 >= self.x_pos + i >= 0) and (7 >= self.y_pos + j >= 0):
                self.attacked_fields.append(tuple([self.x_pos + i,self.y_pos + j]))
                if grid[self.x_pos + i][self.y_pos + j].figure != None:
                    break
        for i in range(-1, -8, -1):
            j = i
            if (7 >= self.x_pos + i >= 0) and (7 >= self.y_pos + j >= 0):
                self.attacked_fields.append(tuple([self.x_pos + i,self.y_pos + j]))
                if grid[self.x_pos + i][self.y_pos + j].figure != None:
                    break
        for i in range(1, 8):
            j = -i
            if (7 >= self.x_pos + i >= 0) and (7 >= self.y_pos + j >= 0):
                self.attacked_fields.append(tuple([self.x_pos + i,self.y_pos + j]))
                if grid[self.x_pos + i][self.y_pos + j].figure != None:
                    break
        for i in range(-1, -8, -1):
            j = -i
            if (7 >= self.x_pos + i >= 0) and (7 >= self.y_pos + j >= 0):
                self.attacked_fields.append(tuple([self.x_pos + i,self.y_pos + j]))
                if grid[self.x_pos + i][self.y_pos + j].figure != None:
                    break
        return self.attacked_fields
    def can_move(self, input: tuple) -> bool:
        self.route = []
        if not (super().can_move(input)):
            return False
        if (abs(input[0] - self.x_pos) != abs(input[1] - self.y_pos)) :
            print('invalid move, bishop can\'t go like this.')
            return False
        
        current_field = tuple([self.x_pos, self.y_pos])
        fields_between = []
        if input[0] > self.x_pos and input[1] > self.y_pos:
            while True:
                current_field = tuple([current_field[0] + 1, current_field[1] + 1])
                if current_field == input:
                    break
                fields_between.append(current_field)
        elif input[0] > self.x_pos and input[1] < self.y_pos:
            while True:
                current_field = tuple([current_field[0] + 1, current_field[1] - 1])
                if current_field == input:
                    break
                fields_between.append(current_field)
        elif input[0] < self.x_pos and input[1] > self.y_pos:
            while True:
                current_field = tuple([current_field[0] - 1, current_field[1] + 1])
                if current_field == input:
                    break
                fields_between.append(current_field)
        elif input[0] < self.x_pos and input[1] < self.y_pos:
            while True:
                current_field = tuple([current_field[0] - 1, current_field[1] - 1])
                if current_field == input:
                    break
                fields_between.append(current_field)
        if not self.moved:
            self.moved = True
        self.route = fields_between
        return True

class Rook(Figure):
    def __init__(self, color, grid: list[list], x_pos = 0, y_pos = 0) -> None:
        super().__init__(color, x_pos, y_pos)
        self.route = []
        if self.color == 'white':
            self.notation = 'R'
        else :
            self.notation = 'r'
        self.attacked_fields = self.calculate_attacked_fields(grid)
        self.name = "Rook"
    def calculate_attacked_fields(self,  grid: list[list]):
        self.attacked_fields = []
        for i in range(-1, -8, -1):
            if (7 >= self.x_pos + i >= 0):
                self.attacked_fields.append(tuple([self.x_pos + i, self.y_pos]))
                if grid[self.x_pos + i][self.y_pos].figure != None:
                    break
        for i in range(1, 8):
            if (7 >= self.x_pos + i >= 0):
                self.attacked_fields.append(tuple([self.x_pos + i, self.y_pos]))
                if grid[self.x_pos + i][self.y_pos].figure != None:
                    break
        for j in range(-1, -8, -1):
            if (7 >= self.y_pos + j >= 0):
                self.attacked_fields.append(tuple([self.x_pos, self.y_pos + j]))
                if grid[self.x_pos][self.y_pos + j].figure != None:
                    break
        for j in range(1, 8):
            if (7 >= self.y_pos + j >= 0):
                self.attacked_fields.append(tuple([self.x_pos, self.y_pos + j]))
                if grid[self.x_pos][self.y_pos + j].figure != None:
                    break
        return self.attacked_fields
    def can_move(self, input: tuple) -> bool:
        self.route = []
        if not (super().can_move(input)):
            return False
        if (input[0] - self.x_pos != 0) and (input[1] - self.y_pos != 0):
            print('invalid move, rook can\'t go like this.')
            return False
        current_field = tuple([self.x_pos, self.y_pos])
        fields_between = []
        if input[0] > self.x_pos:
            while True:
                current_field = tuple([current_field[0] + 1, current_field[1]])
                if current_field == input:
                    break
                fields_between.append(current_field)
        elif input[0] < self.x_pos:
            while True:
                current_field = tuple([current_field[0] - 1, current_field[1]])
                if current_field == input:
                    break
                fields_between.append(current_field)
        elif input[1] > self.y_pos:
            while True:
                current_field = tuple([current_field[0], current_field[1] + 1])
                if current_field == input:
                    break
                fields_between.append(current_field)
        elif input[1] < self.y_pos:
            while True:
                current_field = tuple([current_field[0], current_field[1] - 1])
                if current_field == input:
                    break
                fields_between.append(current_field)
        if not self.moved:
            self.moved = True
        self.route = fields_between
        return True        

class Queen(Figure):
    def __init__(self, color, grid: list[list], x_pos = 0, y_pos = 0) -> None:
        super().__init__(color, x_pos, y_pos)
        self.route = []
        if self.color == 'white':
            self.notation = 'Q'
        else :
            self.notation = 'q'
        self.attacked_fields = self.calculate_attacked_fields(grid)
        self.name = "Queen"
    def calculate_attacked_fields(self, grid: list[list]):
        self.attacked_fields = []
        for i in range(1, 8):
            j = i
            if (7 >= self.x_pos + i >= 0) and (7 >= self.y_pos + j >= 0):
                self.attacked_fields.append(tuple([self.x_pos + i,self.y_pos + j]))
                if grid[self.x_pos + i][self.y_pos + j].figure != None:
                    break
        for i in range(-1, -8, -1):
            j = i
            if (7 >= self.x_pos + i >= 0) and (7 >= self.y_pos + j >= 0):
                self.attacked_fields.append(tuple([self.x_pos + i,self.y_pos + j]))
                if grid[self.x_pos + i][self.y_pos + j].figure != None:
                    break
        for i in range(1, 8):
            j = -i
            if (7 >= self.x_pos + i >= 0) and (7 >= self.y_pos + j >= 0):
                self.attacked_fields.append(tuple([self.x_pos + i,self.y_pos + j]))
                if grid[self.x_pos + i][self.y_pos + j].figure != None:
                    break
        for i in range(-1, -8, -1):
            j = -i
            if (7 >= self.x_pos + i >= 0) and (7 >= self.y_pos + j >= 0):
                self.attacked_fields.append(tuple([self.x_pos + i, self.y_pos + j]))
                if grid[self.x_pos + i][self.y_pos + j].figure != None:
                    break
        for i in range(-1, -8, -1):
            if (7 >= self.x_pos + i >= 0):
                self.attacked_fields.append(tuple([self.x_pos + i, self.y_pos]))
                if grid[self.x_pos + i][self.y_pos].figure != None:
                    break
        for i in range(1, 8):
            if (7 >= self.x_pos + i >= 0):
                self.attacked_fields.append(tuple([self.x_pos + i, self.y_pos]))
                if grid[self.x_pos + i][self.y_pos].figure != None:
                    break
        for j in range(-1, -8, -1):
            if (7 >= self.y_pos + j >= 0):
                self.attacked_fields.append(tuple([self.x_pos, self.y_pos + j]))
                if grid[self.x_pos][self.y_pos + j].figure != None:
                    break
        for j in range(1, 8):
            if (7 >= self.y_pos + j >= 0):
                self.attacked_fields.append(tuple([self.x_pos, self.y_pos + j]))
                if grid[self.x_pos][self.y_pos + j].figure != None:
                    break
        return self.attacked_fields
    def can_move(self, input: tuple) -> bool:
        self.route = []
        if not (super().can_move(input)):
            return False
        if (abs(input[0] - self.x_pos) != abs(input[1] - self.y_pos)) and ((input[0] - self.x_pos != 0) and (input[1] - self.y_pos != 0)):
            print('invalid move, queen can\'t go like this.')
            return False
        current_field = tuple([self.x_pos, self.y_pos])
        fields_between = []
        if input[0] > self.x_pos and input[1] > self.y_pos:
            while True:
                current_field = tuple([current_field[0] + 1, current_field[1] + 1])
                if current_field == input:
                    break
                fields_between.append(current_field)
        elif input[0] > self.x_pos and input[1] < self.y_pos:
            while True:
                current_field = tuple([current_field[0] + 1, current_field[1] - 1])
                if current_field == input:
                    break
                fields_between.append(current_field)
        elif input[0] < self.x_pos and input[1] > self.y_pos:
            while True:
                current_field = tuple([current_field[0] - 1, current_field[1] + 1])
                if current_field == input:
                    break
                fields_between.append(current_field)
        elif input[0] < self.x_pos and input[1] < self.y_pos:
            while True:
                current_field = tuple([current_field[0] - 1, current_field[1] - 1])
                if current_field == input:
                    break
                fields_between.append(current_field)
        elif input[0] > self.x_pos:
            while True:
                current_field = tuple([current_field[0] + 1, current_field[1]])
                if current_field == input:
                    break
                fields_between.append(current_field)
        elif input[0] < self.x_pos:
            while True:
                current_field = tuple([current_field[0] - 1, current_field[1]])
                if current_field == input:
                    break
                fields_between.append(current_field)
        elif input[1] > self.y_pos:
            while True:
                current_field = tuple([current_field[0], current_field[1] + 1])
                if current_field == input:
                    break
                fields_between.append(current_field)
        elif input[1] < self.y_pos:
            while True:
                current_field = tuple([current_field[0], current_field[1] - 1])
                if current_field == input:
                    break
                fields_between.append(current_field)
        if not self.moved:
            self.moved = True
        self.route = fields_between
        return True

class King(Figure):
    def __init__(self, color, grid: list[list], x_pos = 0, y_pos = 0) -> None:
        super().__init__(color, x_pos, y_pos)
        if self.color == 'white':
            self.notation = 'K'
        else :
            self.notation = 'k'
        self.attacked_fields = self.calculate_attacked_fields(grid)
        self.name = "King"
    def calculate_attacked_fields(self, grid):
        self.attacked_fields = []
        for i in range(-1,2):
            for j in range(-1,2):
                if (7 >= self.x_pos + i >= 0) and (7 >= self.y_pos + j >= 0):
                    if i == 0 and j == 0:
                        continue
                    self.attacked_fields.append(tuple([self.x_pos + i,self.y_pos + j]))
        return self.attacked_fields
    def can_move(self, input: tuple) -> bool:
        if not (super().can_move(input)):
            return False
        if abs(input[0] - self.x_pos) > 1 or abs(input[1] - self.y_pos) > 1:
            print('invalid move, king can\'t go like this.')
            return False
        
        if not self.moved:
            self.moved = True
        return True
    