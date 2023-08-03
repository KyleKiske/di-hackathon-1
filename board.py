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
        self.start = board.grid[start[0]][start[1]]
        self.end = board.grid[end[0]][end[1]]
        self.player = player
    def move(self):
        if self.start.figure is None:
            print("No figure on this square")
            return
        elif (self.start.figure.color != self.player.color):
            print("This figure belongs to other player.")
            return
        if (self.end.figure is None):
            self.end.figure = self.start.figure
            self.start.figure = None
            return
        if (self.end.figure.color == self.player.color):
            print('Invalid move, same color figure on the end square')
            return
        if (self.end.figure.color != self.player.color):
            print('Zhri ego!')
            self.end.figure = self.start.figure
            self.start.figure = None
            return
                
playerW = Player('w')

board = Board()
board.default_placement()

board.display()

move = Move(playerW, board, (7,3),(0,4))

move.move()

board.display()