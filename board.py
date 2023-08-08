import numpy as np
from figures import *
import re
from player import Player

class Square:
    def __init__(self, x, y, figure: Figure() = None) -> None:
        self.x_pos = x
        self.y_pos = y
        self.figure = figure
    def __repr__ (self) -> str:
        if self.figure is None:
            return('-')    
        else:
            return (self.figure.notation)

class Board:
    FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    def __init__(self) -> None:
        self.grid = [["-" for _ in range(8)] for _ in range(8)]
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                self.grid[x][y] = Square(x,y)
        self.last_move = None
        self.white_king_cheched = False
        self.black_king_cheched = False
        self.black_attacked_fields = []
        self.white_attacked_fields = []
    def default_placement(self):
        fen_list = re.split("/| ", self.FEN)[:8]
        new_list = []
        for x in fen_list:
            new_string = ''
            for c in range(len(x)):
                if x[c].isdigit() :
                    new_string += (" " * int(x[c]))
                else :
                    new_string += x[c]
            new_list.append(new_string)
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                if new_list[x][y] == 'r':
                    self.grid[x][y].figure = Rook('black', self.grid, x, y)
                elif new_list[x][y] == 'n':
                    self.grid[x][y].figure = Knight('black', self.grid, x, y)
                elif new_list[x][y] == 'b':
                    self.grid[x][y].figure = Bishop('black', self.grid, x, y)
                elif new_list[x][y] == 'k':
                    self.grid[x][y].figure = King('black', self.grid, x, y)
                elif new_list[x][y] == 'q':
                    self.grid[x][y].figure = Queen('black', self.grid, x, y)
                elif new_list[x][y] == 'p':
                    self.grid[x][y].figure = Pawn('black', self.grid, x, y)
                elif new_list[x][y] == 'R':
                    self.grid[x][y].figure = Rook('white', self.grid, x, y)
                elif new_list[x][y] == 'N':
                    self.grid[x][y].figure = Knight('white', self.grid, x, y)
                elif new_list[x][y] == 'B':
                    self.grid[x][y].figure = Bishop('white', self.grid, x, y)
                elif new_list[x][y] == 'K':
                    self.grid[x][y].figure = King('white', self.grid, x, y)
                elif new_list[x][y] == 'Q':
                    self.grid[x][y].figure = Queen('white', self.grid, x, y)
                elif new_list[x][y] == 'P':
                    self.grid[x][y].figure = Pawn('white', self.grid, x, y)
                else: self.grid[x][y].figure = None
    def calculate_attacked_by_white(self):
        self.white_attacked_fields = []
        for i in range(8):
            for j in range(8):
                if self.grid[i][j].figure == None:
                    continue
                elif self.grid[i][j].figure.color == 'white':
                    self.white_attacked_fields.extend(self.grid[i][j].figure.calculate_attacked_fields(self.grid))
        self.white_attacked_fields = list(dict.fromkeys(self.white_attacked_fields))
        return self.white_attacked_fields
    def calculate_attacked_by_black(self):
        self.black_attacked_fields = []
        for i in range(8):
            for j in range(8):
                if self.grid[i][j].figure == None:
                    continue
                elif self.grid[i][j].figure.color == 'black':
                    self.black_attacked_fields.extend(self.grid[i][j].figure.calculate_attacked_fields(self.grid))
        self.black_attacked_fields = list(dict.fromkeys(self.black_attacked_fields))
        return self.black_attacked_fields
    def display(self):
        print(np.matrix(self.grid))

class Move:
    def __init__(self, player: Player, board: Board, start: Square, end: Square) -> None:
        if not (0 <= end[0] <= 7) or not (0 <= end[1] <= 7) or not (0 <= start[0] <= 7) or not (0 <= start[1] <= 7):
            self.start = None
            self.end = None
            return None
        self.start = board.grid[start[0]][start[1]]
        self.end = board.grid[end[0]][end[1]]
        self.player = player
    def is_check_black(self):
        for x in range(len(board.grid)):
            for y in range(len(board.grid[x])):
                if isinstance(board.grid[x][y].figure, King):
                    if board.grid[x][y].figure.color == 'black':
                        if board.calculate_attacked_by_white().count(tuple([x,y])):
                            print("Black king is under attack!")
                            board.black_king_cheched = True
                            return True
        return False
    def is_check_white(self):
        for x in range(len(board.grid)):
            for y in range(len(board.grid[x])):
                if isinstance(board.grid[x][y].figure, King):
                    if board.grid[x][y].figure.color == 'white':
                        if board.calculate_attacked_by_black().count(tuple([x,y])):
                            print("White king is under attack!")
                            board.white_king_cheched = True
                            return True
        return False
    def is_checkmate():
        pass
    def move(self):
        if self.start is None:
            print('invalid move, figure out of bounds.')
            return False
        list_vert=['a','b','c','d','e','f','g','h']
        list_horiz=['8','7','6','5','4','3','2','1']
        
        print(f"move {list_vert[self.start.y_pos]}{list_horiz[self.start.x_pos]} to {list_vert[self.end.y_pos]}{list_horiz[self.end.x_pos]}")
        fig = self.start.figure
        if self.start.figure is None:
            print("No figure on this square")
            return False
        tempStart = Square (self.start.x_pos, self.start.y_pos, self.start.figure)
        tempEnd = Square (self.end.x_pos, self.end.y_pos, self.end.figure) 
        if not fig.can_move(tuple([self.end.x_pos, self.end.y_pos])):
            return False
        elif (self.start.figure.color != self.player.color):
            print("This figure belongs to other player.")
            return False
        print(self.start.figure.route)
        for x in self.start.figure.route:
            print(x)
            if board.grid[x[0]][x[1]].figure != None:
                print("There is figure in the way.")
                return False
        if (self.end.figure is None):
            if isinstance(self.start.figure, Pawn):
                if (abs(self.start.y_pos - self.end.y_pos) == 1):
                    if (abs(self.start.x_pos - self.end.x_pos) == 1):
                        if isinstance(board.last_move[0], Pawn):
                            if self.end.y_pos == board.last_move[2].y_pos:
                                if self.end.x_pos == ( (board.last_move[1].x_pos + board.last_move[2].x_pos) // 2):
                                    print('google en passant')
                                    tempPawn = board.grid[board.last_move[2].x_pos][board.last_move[2].y_pos].figure
                                    self.end.figure = self.start.figure
                                    self.end.figure.x_pos = self.end.x_pos
                                    self.end.figure.y_pos = self.end.y_pos
                                    self.start.figure = None
                                    board.grid[board.last_move[2].x_pos][board.last_move[2].y_pos].figure = None
                                    if tempStart.figure.color == 'white':
                                        if self.is_check_white() :
                                            print('Illegal move: White king is in check!')
                                            self.start = tempStart
                                            self.end = tempEnd
                                            board.grid[tempStart.x_pos][tempStart.y_pos] = tempStart
                                            board.grid[tempEnd.x_pos][tempEnd.y_pos] = tempEnd
                                            board.grid[board.last_move[2].x_pos][board.last_move[2].y_pos].figure = tempPawn
                                            return False
                                    if tempStart.figure.color == 'black':
                                        if self.is_check_black() :
                                            print('Illegal move: Black king is in check!')
                                            self.start = tempStart
                                            self.end = tempEnd
                                            board.grid[tempStart.x_pos][tempStart.y_pos] = tempStart
                                            board.grid[tempEnd.x_pos][tempEnd.y_pos] = tempEnd
                                            board.grid[board.last_move[2].x_pos][board.last_move[2].y_pos].figure = tempPawn
                                            return False
                                    return True
                        else:
                            print("Pawn can't move diagonally.")
                            return False

            if  self.start.figure.moved == False:
                self.start.figure.moved = True
            self.end.figure = self.start.figure
            self.end.figure.x_pos = self.end.x_pos
            self.end.figure.y_pos = self.end.y_pos
            self.start.figure = None
            if tempStart.figure.color == 'white':
                if self.is_check_white() :
                    print('Illegal move: White king is in check!')
                    board.grid[tempStart.x_pos][tempStart.y_pos] = tempStart
                    board.grid[tempEnd.x_pos][tempEnd.y_pos] = tempEnd
                    return False
            if tempStart.figure.color == 'black':
                if self.is_check_black() :
                    print('Illegal move: Black king is in check!')
                    board.grid[tempStart.x_pos][tempStart.y_pos] = tempStart
                    board.grid[tempEnd.x_pos][tempEnd.y_pos] = tempEnd
                    return False
            board.last_move = [self.end.figure, self.start, self.end]
            return True
        if (self.end.figure.color == self.player.color):
            print('Invalid move, same color figure on the end square')
            return False
        if (self.end.figure.route == self.player.color):
            print('Invalid move, same color figure in the way square')
            return False
        if (self.end.figure.color != self.player.color):
            if isinstance(self.start.figure, Pawn):
                if (abs(self.start.y_pos - self.end.y_pos) == 1):
                    if (abs(self.start.x_pos - self.end.x_pos) == 1):
                        print('Zhri ego!')
                        if  self.start.figure.moved == False:
                            self.start.figure.moved = True
                        self.end.figure = self.start.figure
                        self.end.figure.x_pos = self.end.x_pos
                        self.end.figure.y_pos = self.end.y_pos
                        self.start.figure = None
                        if tempStart.figure.color == 'white':
                            if self.is_check_white() :
                                print('Illegal move: White king is in check!')
                                self.start = tempStart
                                self.end = tempEnd
                                board.grid[tempStart.x_pos][tempStart.y_pos] = tempStart
                                board.grid[tempEnd.x_pos][tempEnd.y_pos] = tempEnd
                                return False
                        if tempStart.figure.color == 'black':
                            if self.is_check_black() :
                                print('Illegal move: Black king is in check!')
                                self.start = tempStart
                                self.end = tempEnd
                                board.grid[tempStart.x_pos][tempStart.y_pos] = tempStart
                                board.grid[tempEnd.x_pos][tempEnd.y_pos] = tempEnd
                                return False
                        board.last_move = [self.start, self.end]
                        return True
                    else:
                        print("Pawn can't take that way.")
                        return False
                else:
                    print("Pawn can't take that way.")
                    return False
            else:
                print('Zhri ego!')
                if  self.start.figure.moved == False:
                    self.start.figure.moved = True
                self.end.figure = self.start.figure
                self.end.figure.x_pos = self.end.x_pos
                self.end.figure.y_pos = self.end.y_pos
                self.start.figure = None
                if tempStart.figure.color == 'white':
                    if self.is_check_white() :
                        print('Illegal move: White king is in check!')
                        self.start = tempStart
                        self.end = tempEnd
                        board.grid[tempStart.x_pos][tempStart.y_pos] = tempStart
                        board.grid[tempEnd.x_pos][tempEnd.y_pos] = tempEnd
                        return False
                if tempStart.figure.color == 'black':
                    if self.is_check_black() :
                        print('Illegal move: Black king is in check!')
                        self.start = tempStart
                        self.end = tempEnd
                        board.grid[tempStart.x_pos][tempStart.y_pos] = tempStart
                        board.grid[tempEnd.x_pos][tempEnd.y_pos] = tempEnd
                        return False
                board.last_move = [self.start, self.end]
                return True
                
playerW = Player('white')
playerB = Player('black')

board = Board()
# board.default_placement()

# board.display()

def player_input(player):
    print (f"{player.color} turn...\n")
    while True:
        startrow = int(input("Enter start row: "))
        startcolumn = int(input("Enter start column: "))
        endrow = int(input("Enter end row: "))
        endcolumn = int(input("Enter end column: "))
        if not (7 >= startrow >= 0  or 7 >= startcolumn >= 0 or 7 >= endrow >= 0  or 7 >= endcolumn >= 0):
            print("This field is not on the board, try to write in proper field.")
        # elif ((("X", row, column) in list_of_inputs) or (("O", row, column) in list_of_inputs)):
            # print("This field is occupied, try to write in another field.")
        else:
            break
    return (player, tuple([startrow,startcolumn]), tuple([endrow, endcolumn]))

def play():
    board = Board()
    board.default_placement()
    board.display()
    list_of_moves = []
    while True:
        if len(list_of_moves) % 2 == 0:
            while True:
                player_move = player_input(playerW)
                moveW = Move(player_move[0], board, player_move[1], player_move[2])
                result = moveW.move()
                if result:
                    list_of_moves.append(moveW)
                    board.display()
                    break
                else:
                    board.display()
                
        else:
            while True:
                player_move = player_input(playerB)
                moveB = Move(player_move[0], board, player_move[1], player_move[2])
                result = moveB.move()
                if result:
                    list_of_moves.append(moveB)
                    board.display()
                    break
                else:
                    board.display()



# print('total white attack method')
# print(board.calculate_attacked_by_white())
# print(board.black_king_cheched)
# print('total black attack')
# print(board.calculate_attacked_by_black())

# board.display()

# movePa2 = Move(playerW, board, (6,0),(4,0))
# movePb2 = Move(playerW, board, (6,1),(4,1))
# movePc2 = Move(playerW, board, (6,2),(4,2))
# movePd2 = Move(playerW, board, (6,3),(4,3))
# movePe2 = Move(playerW, board, (6,4),(4,4))

# moveNB1 = Move(playerB, board, (0,1),(2,0))

# movePa2.move()
# movePb2.move()
# movePc2.move()
# movePd2.move()

# movePc4 = Move(playerW, board, (4,2),(3,2))
# movePc5 = Move(playerW, board, (3,2),(2,2))
# movePc6 = Move(playerW, board, (2,2),(1,3))
# movePb7 = Move(playerB, board, (1,2),(2,2))

# movePe2 = Move(playerW, board, (6,4),(4,4))
# movePe4 = Move(playerW, board, (4,4),(3,4))
# movePe5 = Move(playerW, board, (3,4),(2,4))

# movePc4.move()
# movePc5.move()
# movePc6.move()
# movePb7.move()

# movePe2.move()
# movePe4.move()
# movePe5.move()

# print('total white attack method after moves') 
# print(board.calculate_attacked_by_white())
# print(board.black_king_cheched)
# board.display()

# moveKtakesPawn = Move(playerB, board, (0,4),(1,3))
# moveKtakesPawn.move()
# moveBtakesPawn = Move(playerB, board, (0,2),(1,3))
# moveBtakesPawn.move()
# moveNB1.move()
# board.display()

play()