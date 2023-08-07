import pygame
import sys

pygame.init()

size = (640, 640)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chess Game")

board = pygame.Surface((600, 600))
board.fill((124, 252, 0))

for x in range(0, 8, 2):
    for y in range(0, 8, 2):
        pygame.draw.rect(board, (210, 180, 140), (x*75, y*75, 75, 75))
        pygame.draw.rect(board, (210, 180, 140), ((x+1)*75, (y+1)*75, 75, 75))

screen.blit(board, (20, 20))

pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    class Piece:
        def __init__(self, color, x, y, piece_type):
            self.color = color
            self.x = x
            self.y = y
            self.type = piece_type

        def draw(self, surface):
            img = pygame.image.load('Chess_plt45.svg.png')
            DEFAULT_IMAGE_SIZE = (75, 75)
            img = pygame.transform.scale(img, DEFAULT_IMAGE_SIZE)
            surface.blit(img, (self.x*75+10, self.y*75+10))

    pieces = []
    for i in range(8):
        pieces.append(Piece("black", i, 1, "pawn"))
        pieces.append(Piece("white", i, 6, "pawn"))

    for piece in pieces:
        piece.draw(board)

    while True:
        for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(pos)

            x = (pos[0] - 20) // 75
            y = (pos[1] - 20) // 75

            for piece in pieces:
                if piece.x == x and piece.y == y:
                    pos = pygame.mouse.get_pos()
                    x = (pos[0] - 20) // 75
                    y = (pos[1] - 20) // 75
                    piece.x = x
                    piece.y = y

        board.fill((255, 206, 158))
        for x in range(0, 8, 2):
          for y in range(0, 8, 2):
            pygame.draw.rect(board, (210, 180, 140), (x*75, y*75, 75, 75))
            pygame.draw.rect(board, (210, 180, 140), ((x+1)*75, (y+1)*75, 75, 75))

        for piece in pieces:
            piece.draw(board)
        screen.blit(board, (20, 20))
        pygame.display.update()

        