import pygame
import sys


BOARD_WIDTH = 800
ROWS = 8

COMPUTER = pygame.image.load('CheckersRed.png')
PLAYER = pygame.image.load('CheckersBlue.png')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (235, 168, 52)
BLUE = (76, 252, 241)


pygame.init()
ClientWindow = pygame.display.set_mode((BOARD_WIDTH, BOARD_WIDTH))
pygame.display.set_caption('Checkers')

priorMoves = []


class Piece:
    def __init__(self, team):
        self.team = team
        self.image = COMPUTER if self.team == 'COMPUTER' else PLAYER

    def draw(self, x, y):
        ClientWindow.blit(self.image, (x, y))


class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = WHITE
        self.pieces = []

    def add(self, newPiece):
        self.pieces.append(newPiece)

    def draw(self, window):
        pygame.draw.rect(window, self.colour, (self.x, self.y, BOARD_WIDTH / ROWS, BOARD_WIDTH / ROWS))
        i = 0
        for piece in self.pieces:
            window.blit(pygame.transform.scale(piece.image, (BOARD_WIDTH / ROWS, BOARD_WIDTH / ROWS)), (self.x, self.y - i * BOARD_WIDTH / ROWS * 0.15625))
            i += 1


def update_display(win, grid, rows, width):
    draw_grid(win, rows, width)
    for row in grid:
        for spot in row:
            spot.draw(win)
    pygame.display.update()


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j, i, gap)
            if abs(i-j) % 2 == 0:
                node.colour = BLACK
            if abs(i) % 2 == 0 and rows - 1 > i > 0 == abs(i - j) % 2:
                node.add(Piece("COMPUTER"))
            if abs(i) % 2 == 1 and i < rows-1 and abs(i-j) % 2 == 0:
                node.add(Piece("COMPUTER"))
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // ROWS
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))


def getNode(grid, rows, width):
    gap = width//rows
    RowX, RowY = pygame.mouse.get_pos()
    Row = RowX//gap
    Col = RowY//gap
    return Col, Row


def resetColours(grid, node):
    positions = generatePotentialMoves(node, grid)
    positions.append(node)

    for colouredNodes in positions:
        nodeX, nodeY = colouredNodes
        grid[nodeX][nodeY].colour = BLACK if abs(nodeX - nodeY) % 2 == 0 else WHITE


def HighlightPotentialMoves(piecePosition, grid):
    positions = generatePotentialMoves(piecePosition, grid)
    for position in positions:
        Column, Row = position
        grid[Column][Row].colour = BLUE


def opposite(team):
    return "COMPUTER" if team == "COMPUTER" else "PLAYER"


def generatePotentialMoves(nodePosition, grid):
    positions = []
    column, row = nodePosition

    return positions


"""
Error with locating possible moves row col error
"""


def highlight(ClickedNode, Grid, OldHighlight):
    Column, Row = ClickedNode
    Grid[Column][Row].colour = ORANGE
    if OldHighlight:
        resetColours(Grid, OldHighlight)
    HighlightPotentialMoves(ClickedNode, Grid)
    return Column, Row


"""
def move(grid, piecePosition, newPosition):
"""


def main(width, rows, firstMove):
    grid = make_grid(rows, width)
    highlightedPiece = None
    currMove = firstMove

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('EXIT SUCCESSFUL')
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                clickedNode = getNode(grid, rows, width)
                ClickedPositionColumn, ClickedPositionRow = clickedNode
                if grid[ClickedPositionColumn][ClickedPositionRow].colour == BLUE:
                    """ if highlightedPiece:
                        pieceColumn, pieceRow = highlightedPiece """
                    """ if currMove == grid[pieceColumn][pieceRow].piece.team:
                        resetColours(grid, highlightedPiece)
                         currMove=move(grid, highlightedPiece, clickedNode)"""

                """ elif highlightedPiece == clickedNode:
                    pass
                else:
                    if grid[ClickedPositionColumn][ClickedPositionRow].piece:
                        if currMove == grid[ClickedPositionColumn][ClickedPositionRow].piece.team:
                            highlightedPiece = highlight(clickedNode, grid, highlightedPiece) """

        update_display(ClientWindow, grid, rows, width)


ChosenInitialState = []

main(BOARD_WIDTH, ROWS, "PLAYER")
