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
                    self.grid[x][y].figure = Rook('b', x, y)
                elif new_list[x][y] == 'n':
                    self.grid[x][y].figure = Knight('b', x, y)
                elif new_list[x][y] == 'b':
                    self.grid[x][y].figure = Bishop('b', x, y)
                elif new_list[x][y] == 'k':
                    self.grid[x][y].figure = King('b', x, y)
                elif new_list[x][y] == 'q':
                    self.grid[x][y].figure = Queen('b', x, y)
                elif new_list[x][y] == 'p':
                    self.grid[x][y].figure = Pawn('b', x, y)
                elif new_list[x][y] == 'R':
                    self.grid[x][y].figure = Rook('w', x, y)
                elif new_list[x][y] == 'N':
                    self.grid[x][y].figure = Knight('w', x, y)
                elif new_list[x][y] == 'B':
                    self.grid[x][y].figure = Bishop('w', x, y)
                elif new_list[x][y] == 'K':
                    self.grid[x][y].figure = King('w', x, y)
                elif new_list[x][y] == 'Q':
                    self.grid[x][y].figure = Queen('w', x, y)
                elif new_list[x][y] == 'P':
                    self.grid[x][y].figure = Pawn('w', x, y)
                else: self.grid[x][y].figure = None
    def place_figure(self, figure: Figure):
        self.grid[figure.x_pos][figure.y_pos] = figure.notation
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
    def move(self):
        if self.start is None:
            print('invalid move, figure out of bounds.')
            return
        list_vert=['a','b','c','d','e','f','g','h']
        list_horiz=['8','7','6','5','4','3','2','1']
        print(f"move {list_vert[self.start.y_pos]}{list_horiz[self.start.x_pos]} to {list_vert[self.end.y_pos]}{list_horiz[self.end.x_pos]}")
        fig = self.start.figure
        if self.start.figure is None:
            print("No figure on this square")
            return
        if not fig.can_move(tuple([self.end.x_pos, self.end.y_pos])):
            return
        elif (self.start.figure.color != self.player.color):
            print("This figure belongs to other player.")
            return
        print(self.start.figure.route)
        for x in self.start.figure.route:
            print(x)
            if board.grid[x[0]][x[1]].figure != None:
                print("There is figure in the way.")
                return
        if (self.end.figure is None):
            if  self.start.figure.moved == False:
                self.start.figure.moved = True
            self.end.figure = self.start.figure
            self.end.figure.x_pos = self.end.x_pos
            self.end.figure.y_pos = self.end.y_pos
            self.start.figure = None
            return
        if (self.end.figure.color == self.player.color):
            print('Invalid move, same color figure on the end square')
            return
        
        if (self.end.figure.route == self.player.color):
            print('Invalid move, same color figure on the end square')
            return
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
                        return
                    else:
                        print("Pawn can't take that way.")
                        return
                else:
                    print("Pawn can't take that way.")
                    return
            else:
                print('Zhri ego!')
                if  self.start.figure.moved == False:
                    self.start.figure.moved = True
                self.end.figure = self.start.figure
                self.end.figure.x_pos = self.end.x_pos
                self.end.figure.y_pos = self.end.y_pos
                self.start.figure = None
                return
                
playerW = Player('w')
playerB = Player('b')

board = Board()
board.default_placement()

board.display()

movePa2 = Move(playerW, board, (6,0),(4,0))
movePb2 = Move(playerW, board, (6,1),(4,1))
movePc2 = Move(playerW, board, (6,2),(4,2))
movePd2 = Move(playerW, board, (6,3),(4,3))
movePe2 = Move(playerW, board, (6,4),(4,4))
movePf2 = Move(playerW, board, (6,5),(4,5))
movePg2 = Move(playerW, board, (6,6),(4,6))
movePh2 = Move(playerW, board, (6,7),(4,7))

move2 = Move(playerB, board, (1,2),(3,2))
moveR = Move(playerW, board, (7,0),(5,0))
moveR2 = Move(playerW, board, (7,0),(4,0))
moveRR = Move(playerW, board, (5,0),(5,4))
moveB = Move(playerW, board, (7,5), (5,7))
moveB_Black = Move(playerB, board, (0,2), (2,0))
moveOOB = Move(playerW, board, (7,8), (6,7))

moveQ = Move(playerW, board, (7,3),(4,3))
moveQ_bl = Move(playerB, board, (0,3),(2,1))
moveQ_b2 = Move(playerB, board, (2,1),(4,1))

moveTake = Move(playerW, board, (4,2), (3,2))
moveTakeReal = Move(playerW, board, (4,5), (3,2))

movePa2.move()
movePb2.move()
movePc2.move()
movePd2.move()
moveR.move()
moveRR.move()
movePe2.move()
movePf2.move()
movePg2.move()
movePh2.move()

board.display()
move2.move()
board.display()
moveR2.move()
board.display()
moveB.move()
moveB_Black.move()
board.display()

moveQ.move()
moveQ_bl.move()
moveQ_b2.move()
board.display()
moveTake.move()
moveTakeReal.move()
board.display()