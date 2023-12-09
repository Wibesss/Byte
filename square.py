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

    def draw(self, window,rows):
        global ROWS
        pygame.draw.rect(window, self.color, (self.x + 50, self.y + 50, BOARD_WIDTH / rows, BOARD_WIDTH / rows))
        i = 0
        for piece in self.pieces:
            window.blit(pygame.transform.scale(piece.image, (BOARD_WIDTH / rows, BOARD_WIDTH / rows)),
                        (self.x + 50, self.y + 50 - i * BOARD_WIDTH / rows * 0.15625))
            i += 1
    
    def removePieces(self, index):
        self.pieces = self.pieces[:index]

    def clearPieces(self):
        self.pieces.clear()
    
    def returnPiece(self,index):
        return self.pieces[index]

    def returnNumberOfPieces(self):
        return len(self.pieces)

    def hasPieces(self):
        return True if len(self.pieces) > 0 else False
    
    def checkIfCompleted(self):
        return True if self.returnNumberOfPieces()==8 else False
