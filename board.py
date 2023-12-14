import copy
import math
import pygame
from piece import Piece
from square import Square
from constants import ROWS
from constants import BLACK
from constants import WHITE
from main import RED_PLAYER_POINTS
from main import BLUE_PLAYER_POINTS
from main import playMove


boardLabels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']

RED_PLAYER_POINTS=0
BLUE_PLAYER_POINTS=0

def makeBoard(rows, width):
    global ROWS
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
    global ROWS
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


def drawLabels(win, rows, boardWidth):
    global ROWS
    font = pygame.font.Font(None, 36)
    for i in range(rows):
        letter = font.render(boardLabels[i], True, (0, 0, 0))
        win.blit(letter, (20, 40 + boardWidth / rows / 2 + boardWidth / rows * i))
        number = font.render(str(i + 1), True, (0, 0, 0))
        win.blit(number, (40 + boardWidth / rows / 2 + boardWidth / rows * i, 20))


def addPieceToSquare(row, col, pieceColor, board,rows):
    intRow=boardLabels.index(row)
    intCol=int(col)
    if not squareInBoard(row, col,rows) or intCol< 1:
        print("Square not in board")
        return
    if board[intRow][intCol-1].color == WHITE:
        print("You can only add pieces to black squares")
        return
    if board[intRow][intCol-1].returnNumberOfPieces() == 7:
        print("You cannot add more than 7 pieces to a stack")
        return
    if 0 <= intRow < len(board) and 0 <= intCol-1 < len(board[0]):
        if pieceColor not in ["B", "R"]:
            print("Invalid color. Accepted values are 'B' or 'R'.")
        new_piece = Piece(pieceColor)
        board[intRow][intCol-1].add(new_piece)


def isBoardClear(board):
    isClear=True
    for row in board:
        for col in row:
            if col.hasPieces():
                isClear=False
    
    return isClear


def checkIfMoveIsValid(row, col, heightInStack, direction, board,rows,currentTurn):
    
    if not squareInBoard(row, col,rows):
        print("Square not in board")
        return False
    elif not piecesOnSquare(row, col, board):
        print("There are no pieces on this square")
        return False
    elif not pieceInStack(row, col, heightInStack, board):
        print("There is no piece of that height in stack")
        return False
    elif not directionPossible(row, col, direction,rows):
        print("Direction you chose is not possible")
        return False
    else:
        if checkIfPieceIsValidColor(row,col,heightInStack, board,currentTurn):
            intRow=boardLabels.index(row)
            intCol=int(col)-1
            if checkAdjacent(intRow,intCol,board,rows,intRow,intCol):
                x=checkMerging(row,col,heightInStack,direction,rows,board)
                return x
            else:
                if int(heightInStack) == 0:
                    x=compareDistances(intRow,intCol,direction,rows,board)
                    return x
                else:
                    print("You have to move the whole stack")
                    return False
               
               


def findClosestPiece(row,col,rows,board,distance):
        for i in range(row-distance,row+distance+1):
            if i>=0 and i<rows:
                    if (col-distance>=0  and board[i][col-distance].hasPieces()) or (col+distance<rows and board[i][col+distance].hasPieces()):
                        return distance
        for i in range(col-distance,col+distance+1):
            if i>=0 and i<rows:
                if (row-distance>=0 and board[row-distance][i].hasPieces()) or (row+distance<rows and board[row+distance][i].hasPieces()):
                        return distance
        return findClosestPiece(row,col,rows,board,distance+1)
          

def compareDistances(intRow,intCol,direction,rows,board):
    if direction=="DD":
        newRow=intRow+1
        newCol=intCol+1
    if direction=="DL":
        newRow=intRow+1
        newCol=intCol-1
    if direction=="GL":
        newRow=intRow-1
        newCol=intCol-1
    if direction=="GD":
        newRow=intRow-1
        newCol=intCol+1

    oldDistance=findClosestPiece(intRow,intCol,rows,board,2)
    newDistance=findClosestPiece(newRow,newCol,rows,board,2)

    if newDistance < oldDistance or checkAdjacent(newRow,newCol,board,rows,intRow,intCol):
        print("New move makes the distance smaller, so its valid")
        return True
    else:
        print("New move doesnt make the distance smaller, so its not valid")
        return False

    
def getAllMoves(board, rows, current_turn):
    all_valid_moves = []
    all_invalid_moves = []
    newBoards = []

    for i in range(rows):
        for j in range(rows):
            if board[i][j].returnColor() == BLACK and board[i][j].hasPieces():
                for direction in ["DD", "DL", "GD", "GL"]:
                    for height in range(board[i][j].returnNumberOfPieces()):
                        move_validity = checkIfMoveIsValid(boardLabels[i], str(j + 1), height, direction, board, rows, current_turn)

                        move_info = {"position": (boardLabels[i], str(j + 1)), "direction": direction, "height": height}

                        if move_validity:
                            all_valid_moves.append(move_info)

                            new_board = [row[:] for row in board]
                           #playMove(move_info['position'][0],move_info['position'][1],move_info['height'],move_info['direction'],new_board,rows)
                            newBoards.append(new_board)

                        else:
                            all_invalid_moves.append(move_info)

    print(f"Valid Moves {current_turn}: ")
    for move in all_valid_moves:
        print(f"  {move['position'][0]} {move['position'][1]} {move['height']} {move['direction']}")

    print(f"\nInvalid Moves {current_turn}:")
    for move in all_invalid_moves:
        print(f"  {move['position'][0]} {move['position'][1]} {move['height']} {move['direction']}")

def isGameFinished(board):
    global RED_PLAYER_POINTS, BLUE_PLAYER_POINTS, ROWS
    if isBoardClear(board):
        return True
    elif RED_PLAYER_POINTS == math.ceil(((ROWS/2)*(ROWS-2)/8)/2):
        return True
    elif BLUE_PLAYER_POINTS == math.ceil(((ROWS/2)*(ROWS-2)/8)/2):
        return True
    return False

                               
               
def checkMerging(row, col, heightInStack, direction, rows, board):
    if direction == "DD":
        if boardLabels.index(row) < rows - 1 and int(col) < rows:
            return True if board[boardLabels.index(row) + 1][int(col)].hasPieces() and board[boardLabels.index(row) + 1][int(col)].returnNumberOfPieces() + board[boardLabels.index(row)][int(col) - 1].returnNumberOfPieces() - int(heightInStack) <= 8 and board[boardLabels.index(row)+1][int(col)].returnNumberOfPieces()>int(heightInStack)  else False

    if direction == "DL":
        if boardLabels.index(row) < rows - 1 and int(col) > 1:
            return True if board[boardLabels.index(row) + 1][int(col) - 2].hasPieces() and board[boardLabels.index(row) + 1][int(col) - 2].returnNumberOfPieces() + board[boardLabels.index(row)][int(col) - 1].returnNumberOfPieces() - int(heightInStack) <= 8 and board[boardLabels.index(row)+1][int(col) - 2].returnNumberOfPieces()>int(heightInStack)  else False

    if direction == "GD":
        if boardLabels.index(row) > 0 and int(col) < rows:
            return True if board[boardLabels.index(row) - 1][int(col)].hasPieces() and board[boardLabels.index(row) - 1][int(col)].returnNumberOfPieces() + board[boardLabels.index(row)][int(col) - 1].returnNumberOfPieces() - int(heightInStack) <= 8  and board[boardLabels.index(row)-1][int(col)].returnNumberOfPieces()>int(heightInStack) else False

    if direction == "GL":
        if boardLabels.index(row) > 0 and int(col) > 1:
            return True if board[boardLabels.index(row) - 1][int(col) - 2].hasPieces() and board[boardLabels.index(row) - 1][int(col) - 2].returnNumberOfPieces() + board[boardLabels.index(row)][int(col) - 1].returnNumberOfPieces() - int(heightInStack) <= 8 and board[boardLabels.index(row)-1][int(col) - 2].returnNumberOfPieces()>int(heightInStack) else False



        





def checkIfPieceIsValidColor(row,col,heightInStack, board,currentTurn):
        intRow=boardLabels.index(row)
        intCol=int(col)-1
        if pieceInStack(row,col,heightInStack,board ):
            if board[intRow][intCol].returnPiece(int(heightInStack)).returnColor()==currentTurn:
                print("Selected piece is your color")
                return True
            else:
                print("Selected piece is not your color")
                return False
        else:
            return False
        


def checkAdjacent(intRow, intCol,board,rows,ignoreRow,ignoreCol):
    if intRow -1 >= 0 and intCol-1 >= 0 and board[intRow-1][intCol-1].hasPieces() and (intRow-1!=ignoreRow or intCol-1!=ignoreCol):
        print("[",intRow,"]","[",intCol,"]","Has adjacent ")
        return True
    if intRow -1 >= 0 and intCol+1 < rows and board[intRow-1][intCol+1].hasPieces() and (intRow-1!=ignoreRow or intCol+1!=ignoreCol):
        print("[",intRow,"]","[",intCol,"]","Has adjacent ")
        return True
    if intRow+1 < rows and intCol - 1 >=0  and board[intRow+1][intCol-1].hasPieces() and (intRow+1!=ignoreRow or intCol-1!=ignoreCol):
        print("[",intRow,"]","[",intCol,"]","Has adjacent ")
        return True
    if intRow+1 < rows and intCol+1 < rows and board[intRow+1][intCol+1].hasPieces() and (intRow+1!=ignoreRow or intCol+1!=ignoreCol):
        print("[",intRow,"]","[",intCol,"]","Has adjacent ")
        return True
    else:
        print("[",intRow,"]","[",intCol,"]","Doesnt have adjacent")
        return False


def squareInBoard(row, col,rows):
    return True if row in boardLabels and boardLabels.index(row) < rows and int(col) - 1 < rows and int(col)-1 >=0 else False


def piecesOnSquare(row, col, board):
    return board[boardLabels.index(row)][int(col)-1].hasPieces()


def pieceInStack(row, col, heightInStack, board):
    return True if 0 <= int(heightInStack) < board[boardLabels.index(row)][int(col)-1].returnNumberOfPieces() else False


def directionPossible(row, col, direction,rows):
    if direction == "DD":
        return True if boardLabels.index(row) < rows-1 and int(col) < rows else False

    if direction == "DL":
        return True if boardLabels.index(row) < rows-1 and int(col) > 1 else False

    if direction == "GD":
        return True if boardLabels.index(row) > 0 and int(col) < rows else False

    if direction == "GL":
        return True if boardLabels.index(row) > 0 and int(col) > 1 else False
