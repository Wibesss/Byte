import pygame
from constants import BOARD_WIDTH
from constants import ROWS
from constants import WHITE


class Square:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.color = WHITE
        self.pieces = []

    def add(self, newPiece):
        self.pieces.append(newPiece)

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x + 50, self.y + 50, BOARD_WIDTH / ROWS, BOARD_WIDTH / ROWS))
        i = 0
        for piece in self.pieces:
            window.blit(pygame.transform.scale(piece.image, (BOARD_WIDTH / ROWS, BOARD_WIDTH / ROWS)),
                        (self.x + 50, self.y + 50 - i * BOARD_WIDTH / ROWS * 0.15625))
            i += 1

    def clearPieces(self):
        self.pieces.clear()

    def returnNumberOfPieces(self):
        return len(self.pieces)
