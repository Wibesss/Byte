import pygame
from piece import Piece
from square import Square
from constants import ROWS
from constants import BLACK
from constants import WHITE


boardLabels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']


def makeBoard(rows, width):
    board = []
    squareWidth = width // rows
    for i in range(rows):
        board.append([])
        for j in range(rows):
            square = Square(j, i, squareWidth)
            if abs(i - j) % 2 == 0:
                square.color = BLACK
            if abs(i) % 2 == 0 and rows - 1 > i > 0 == abs(i - j) % 2:
                square.add(Piece("B"))
            if abs(i) % 2 == 1 and i < rows - 1 and abs(i - j) % 2 == 0:
                square.add(Piece("R"))
            board[i].append(square)
    return board


def clearBoard(board):
    for row in board:
        for col in row:
            col.clearPieces()


def resetBoard(board, rows, width):
    clearBoard(board)
    board.clear()
    squareWidth = width / rows
    for i in range(rows):
        board.append([])
        for j in range(rows):
            square = Square(j, i, squareWidth)
            if abs(i - j) % 2 == 0:
                square.color = BLACK
            if abs(i) % 2 == 0 and rows - 1 > i > 0 == abs(i - j) % 2:
                square.add(Piece("B"))
            if abs(i) % 2 == 1 and i < rows - 1 and abs(i - j) % 2 == 0:
                square.add(Piece("R"))
            board[i].append(square)


def drawGrid(win, rows, boardWidth):
    squareWidth = boardWidth // rows
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * squareWidth), (boardWidth, i * squareWidth))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * squareWidth, 0), (j * squareWidth, boardWidth))


def drawLabels(win, rows, boardWidth):
    font = pygame.font.Font(None, 36)
    for i in range(rows):
        letter = font.render(boardLabels[i], True, (0, 0, 0))
        win.blit(letter, (20, 40 + boardWidth / rows / 2 + boardWidth / rows * i))
        number = font.render(str(i + 1), True, (0, 0, 0))
        win.blit(number, (40 + boardWidth / rows / 2 + boardWidth / rows * i, 20))


def addPieceToSquare(row, col, pieceColor, board):

    if board[row][col].color == WHITE:
        raise ValueError("You can only add pieces to black squares")

    if board[row][col].returnNumberOfPieces() == 7:
        raise ValueError("You cannot add more than 7 pieces to a stack")

    if 0 <= row < len(board) and 0 <= col < len(board[0]):
        if pieceColor not in ["B", "R"]:
            raise ValueError("Invalid color. Accepted values are 'B' or 'R'.")
        new_piece = Piece(pieceColor)
        board[row][col].add(new_piece)


def checkIfMoveIsValid(row, col, heightInStack, direction, board):
    if not squareInBoard(row, col):
        print("Square not in board")
        return
    elif not piecesOnSquare(row, col, board):
        print("There are no pieces on this square")
    elif not pieceInStack(row, col, heightInStack, board):
        print("There is no piece of that height in stack")
    elif not directionPossible(row, col, direction):
        print("Direction you chose is not possible")
    else:
        print("Move is Valid")


def squareInBoard(row, col):
    return True if row in boardLabels and boardLabels.index(row) < ROWS and int(col) - 1 < ROWS else False


def piecesOnSquare(row, col, board):
    return board[boardLabels.index(row)][int(col)-1].hasPieces()


def pieceInStack(row, col, heightInStack, board):
    return True if 0 <= int(heightInStack) < board[boardLabels.index(row)][int(col)-1].returnNumberOfPieces() else False


def directionPossible(row, col, direction):
    if direction == "DD":
        return True if boardLabels.index(row) < ROWS-1 and int(col) < ROWS else False

    if direction == "DL":
        return True if boardLabels.index(row) < ROWS-1 and int(col) > 1 else False

    if direction == "GD":
        return True if boardLabels.index(row) > 0 and int(col) < ROWS else False

    if direction == "GL":
        return True if boardLabels.index(row) > 0 and int(col) > 1 else False
