class Figure:
    def __init__(self, color = 'w', x_pos = 0, y_pos = 0) -> None:
        if not (0 <= x_pos <= 7) or not (0 <= y_pos <= 7):
            print('invalid placement of figure')
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.moved = False
        self.notation = ""
        self.route = []
    def can_move(self, input: tuple) -> bool:
        if (input[0] == self.x_pos and input[1] == self.y_pos):
            print('invalid move, figure stays in its place.')
            return False
        return True

class Pawn(Figure):
    
    def __init__(self, color, x_pos = 0, y_pos = 0) -> None:
        super().__init__(color, x_pos, y_pos)
        self.route = []
        if self.color == 'w':
            self.notation = 'P'
        else :
            self.notation = 'p'
    def can_move(self, input: tuple) -> bool:
        self.route = []
        if not (super().can_move(input)):
            return False
        if self.color == 'w':
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
    def __init__(self, color, x_pos = 0, y_pos = 0) -> None:
        super().__init__(color, x_pos, y_pos)
        if self.color == 'w':
            self.notation = 'N'
        else :
            self.notation = 'n'
    def can_move(self, input: tuple) -> bool:
        if not (super().can_move(input)):
            return False
        elif abs(self.x_pos - input[0]) * abs(self.x_pos - input[1]) != 2:
            print('invalid move, knight can\'t go like this.')
            return False
        if not self.moved:
            self.moved = True
        return True
    
    pass

class Bishop(Figure):
    def __init__(self, color, x_pos = 0, y_pos = 0) -> None:
        super().__init__(color, x_pos, y_pos)
        self.route = []
        if self.color == 'w':
            self.notation = 'B'
        else :
            self.notation = 'b'
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
    def __init__(self, color, x_pos = 0, y_pos = 0) -> None:
        super().__init__(color, x_pos, y_pos)
        self.route = []
        if self.color == 'w':
            self.notation = 'R'
        else :
            self.notation = 'r'
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
    def __init__(self, color, x_pos = 0, y_pos = 0) -> None:
        super().__init__(color, x_pos, y_pos)
        self.route = []
        if self.color == 'w':
            self.notation = 'Q'
        else :
            self.notation = 'q'
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
    def __init__(self, color, x_pos = 0, y_pos = 0) -> None:
        super().__init__(color, x_pos, y_pos)
        if self.color == 'w':
            self.notation = 'K'
        else :
            self.notation = 'k'
    def can_move(self, input: tuple) -> bool:
        if not (super().can_move(input)):
            return False
        if abs(input[0] - self.x_pos) > 1 or abs(input[1] - self.y_pos) > 1:
            print('invalid move, king can\'t go like this.')
            return False
        
        if not self.moved:
            self.moved = True
        return True
    