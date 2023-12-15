import copy
import math
import pygame
from piece import Piece
from square import Square
from constants import ROWS
from constants import BLACK
from constants import WHITE
from main import drawGui



boardLabels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']


class Board:
    def __init__(self, rows,width):
        self.width=width
        self.rows = rows
        self.board = self.makeBoard()
        self.blue_player_points=0
        self.red_player_points=0
        self.current_turn='B'
        self.possible_boards=[]


    def copy(self):
        new_board = Board(self.rows, self.width)
        new_board.blue_player_points = self.blue_player_points
        new_board.red_player_points = self.red_player_points
        new_board.current_turn = self.current_turn

       
        for i in range(self.rows):
            for j in range(self.rows):
                new_board.board[i][j].pieces = self.board[i][j].pieces.copy()

        return new_board
        
    def makeBoard(self):
        board = []

        squareWidth = self.width // self.rows
        for i in range(self.rows):
            board.append([])
            for j in range(self.rows):
                square = Square(j, i, squareWidth)
                if abs(i - j) % 2 == 0:
                    square.color = BLACK
                if abs(i) % 2 == 0 and self.rows - 1 > i > 0 == abs(i - j) % 2:
                    square.add(Piece("B"))
                if abs(i) % 2 == 1 and i < self.rows - 1 and abs(i - j) % 2 == 0:
                    square.add(Piece("R"))
                board[i].append(square)
        return board


    def clearBoard(self):
        for row in self.board:
            for col in row:
                col.clearPieces()


    def resetBoard(self):
        self.clearBoard()
        self.board.clear()
        squareWidth = self.width / self.rows
        for i in range(self.rows):
            self.board.append([])
            for j in range( self.rows):
                square = Square(j, i, squareWidth)
                if abs(i - j) % 2 == 0:
                    square.color = BLACK
                if abs(i) % 2 == 0 and  self.rows - 1 > i > 0 == abs(i - j) % 2:
                    square.add(Piece("B"))
                if abs(i) % 2 == 1 and i <  self.rows - 1 and abs(i - j) % 2 == 0:
                    square.add(Piece("R"))
                self.board[i].append(square)
    
    def changeTurn(self):
        if self.current_turn == "B":
            self.current_turn="R"
        else:
            self.current_turn = "B"

    def addPieceToSquare(self,row, col, pieceColor):
        intRow=boardLabels.index(row)
        intCol=int(col)
        if not self.squareInBoard(row, col,self.rows) or intCol< 1:
            print("Square not in board")
            return
        if self.board[intRow][intCol-1].color == WHITE:
            print("You can only add pieces to black squares")
            return
        if self.board[intRow][intCol-1].returnNumberOfPieces() == 7:
            print("You cannot add more than 7 pieces to a stack")
            return
        if 0 <= intRow < len(self.board) and 0 <= intCol-1 < len(self.board[0]):
            if pieceColor not in ["B", "R"]:
                print("Invalid color. Accepted values are 'B' or 'R'.")
            new_piece = Piece(pieceColor)
            self.board[intRow][intCol-1].add(new_piece)


    def isBoardClear(self):
        isClear=True
        for row in self.board:
            for col in row:
                if col.hasPieces():
                    isClear=False
        return isClear
    
    def squareInBoard(self,row, col):
        return True if row in boardLabels and boardLabels.index(row) < self.rows and int(col) - 1 < self.rows and int(col)-1 >=0 else False


    def piecesOnSquare(self,row, col):
        return self.board[boardLabels.index(row)][int(col)-1].hasPieces()


    def pieceInStack(self,row, col, heightInStack):
        return True if 0 <= int(heightInStack) < self.board[boardLabels.index(row)][int(col)-1].returnNumberOfPieces() else False


    def directionPossible(self,row, col, direction):
        if direction == "DD":
            return True if boardLabels.index(row) < self.rows-1 and int(col) < self.rows else False

        if direction == "DL":
            return True if boardLabels.index(row) < self.rows-1 and int(col) > 1 else False

        if direction == "GD":
            return True if boardLabels.index(row) > 0 and int(col) < self.rows else False

        if direction == "GL":
            return True if boardLabels.index(row) > 0 and int(col) > 1 else False



    def checkIfMoveIsValid(self,row, col, heightInStack, direction):
    
        if not self.squareInBoard(row, col):
            return False
        elif not self.piecesOnSquare(row, col):
            return False
        elif not self.pieceInStack(row, col, heightInStack):
            return False
        elif not self.directionPossible(row, col, direction):
            return False
        else:
            if self.checkIfPieceIsValidColor(row,col,heightInStack):
                intRow=boardLabels.index(row)
                intCol=int(col)-1
                if self.checkAdjacent(intRow,intCol,intRow,intCol):
                    return self.checkMerging(row,col,heightInStack,direction)
                else:
                    if int(heightInStack) == 0:
                        return self.compareDistances(intRow,intCol,direction)
                    else:
                        print("You have to move the whole stack")
                        return False
                    

        
    def checkAdjacent(self,intRow, intCol,ignoreRow,ignoreCol):
        if intRow -1 >= 0 and intCol-1 >= 0 and self.board[intRow-1][intCol-1].hasPieces() and (intRow-1!=ignoreRow or intCol-1!=ignoreCol):
            return True
        if intRow -1 >= 0 and intCol+1 < self.rows and self.board[intRow-1][intCol+1].hasPieces() and (intRow-1!=ignoreRow or intCol+1!=ignoreCol):
            return True
        if intRow+1 < self.rows and intCol - 1 >=0  and self.board[intRow+1][intCol-1].hasPieces() and (intRow+1!=ignoreRow or intCol-1!=ignoreCol):
            return True
        if intRow+1 < self.rows and intCol+1 < self.rows and self.board[intRow+1][intCol+1].hasPieces() and (intRow+1!=ignoreRow or intCol+1!=ignoreCol):
            return True
        else:
            return False
        
    def checkIfPieceIsValidColor(self,row,col,heightInStack):
        intRow=boardLabels.index(row)
        intCol=int(col)-1
        if self.pieceInStack(row,col,heightInStack):
            if self.board[intRow][intCol].returnPiece(int(heightInStack)).returnColor()==self.current_turn:
                return True
            else:
                return False
        else:
            return False
        
    def isGameFinished(self):
        if self.isBoardClear():
            return True
        elif self.red_player_points == math.ceil(((self.rows/2)*(self.rows-2)/8)/2):
            return True
        elif self.blue_player_points == math.ceil(((self.rows/2)*(self.rows-2)/8)/2):
            return True
        return False



                    
    def checkMerging(self,row, col, heightInStack, direction):
        if direction == "DD":
            if boardLabels.index(row) < self.rows - 1 and int(col) < self.rows:
                return True if self.board[boardLabels.index(row) + 1][int(col)].hasPieces() and self.board[boardLabels.index(row) + 1][int(col)].returnNumberOfPieces() + self.board[boardLabels.index(row)][int(col) - 1].returnNumberOfPieces() - int(heightInStack) <= 8 and self.board[boardLabels.index(row)+1][int(col)].returnNumberOfPieces()>int(heightInStack)  else False

        if direction == "DL":
            if boardLabels.index(row) < self.rows - 1 and int(col) > 1:
                return True if self.board[boardLabels.index(row) + 1][int(col) - 2].hasPieces() and self.board[boardLabels.index(row) + 1][int(col) - 2].returnNumberOfPieces() + self.board[boardLabels.index(row)][int(col) - 1].returnNumberOfPieces() - int(heightInStack) <= 8 and self.board[boardLabels.index(row)+1][int(col) - 2].returnNumberOfPieces()>int(heightInStack)  else False

        if direction == "GD":
            if boardLabels.index(row) > 0 and int(col) < self.rows:
                return True if self.board[boardLabels.index(row) - 1][int(col)].hasPieces() and self.board[boardLabels.index(row) - 1][int(col)].returnNumberOfPieces() + self.board[boardLabels.index(row)][int(col) - 1].returnNumberOfPieces() - int(heightInStack) <= 8  and self.board[boardLabels.index(row)-1][int(col)].returnNumberOfPieces()>int(heightInStack) else False

        if direction == "GL":
            if boardLabels.index(row) > 0 and int(col) > 1:
                return True if self.board[boardLabels.index(row) - 1][int(col) - 2].hasPieces() and self.board[boardLabels.index(row) - 1][int(col) - 2].returnNumberOfPieces() + self.board[boardLabels.index(row)][int(col) - 1].returnNumberOfPieces() - int(heightInStack) <= 8 and self.board[boardLabels.index(row)-1][int(col) - 2].returnNumberOfPieces()>int(heightInStack) else False


    def findClosestPiece(self,row,col,distance):
        for i in range(row-distance,row+distance+1):
            if i>=0 and i<self.rows:
                    if (col-distance>=0  and self.board[i][col-distance].hasPieces()) or (col+distance<self.rows and self.board[i][col+distance].hasPieces()):
                        return distance
        for i in range(col-distance,col+distance+1):
            if i>=0 and i<self.rows:
                if (row-distance>=0 and self.board[row-distance][i].hasPieces()) or (row+distance<self.rows and self.board[row+distance][i].hasPieces()):
                        return distance
        return self.findClosestPiece(row,col,distance+1)
        

    def compareDistances(self,intRow,intCol,direction):
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

        oldDistance=self.findClosestPiece(intRow,intCol,2)
        newDistance=self.findClosestPiece(newRow,newCol,2)

        if newDistance < oldDistance or self.checkAdjacent(newRow,newCol,intRow,intCol):
            return True
        else:
            return False
        
    def getAllMoves(self):
        all_valid_moves = []
        all_invalid_moves = []

        for i in range(self.rows):
            for j in range(self.rows):
                if self.board[i][j].returnColor() == BLACK and self.board[i][j].hasPieces():
                    for direction in ["DD", "DL", "GD", "GL"]:
                        for height in range(self.board[i][j].returnNumberOfPieces()):
                            move_validity = self.checkIfMoveIsValid(boardLabels[i], str(j + 1), height, direction)

                            move_info = {"position": (boardLabels[i], str(j + 1)), "direction": direction, "height": height}

                            if move_validity:
                                all_valid_moves.append(move_info)

                                new_board = self.copy()
                                new_board.playMove(move_info['position'][0],move_info['position'][1],move_info['height'],move_info['direction'])
                                self.possible_boards.append(new_board)

                            else:
                                all_invalid_moves.append(move_info)

        print(f"Valid Moves {self.current_turn}: ")
        for move in all_valid_moves:
            print(f"  {move['position'][0]} {move['position'][1]} {move['height']} {move['direction']}")

        print(f"\nInvalid Moves {self.current_turn}:")
        for move in all_invalid_moves:
            print(f"  {move['position'][0]} {move['position'][1]} {move['height']} {move['direction']}")

        

    def updateDisplay(self,win,moveInputs,pieceInputs):
        if self.current_turn=="B":
            drawGui(win, moveInputs, pieceInputs,"BLUE")
        else:
            drawGui(win,moveInputs, pieceInputs,"RED")
        drawLabels(win, self.rows, self.width)

        for row in self.board:
            for spot in row:
                spot.draw(win,self.rows)
        pygame.display.update()

    def playMove(self,row, col, heightInStack, direction):
        intRow = boardLabels.index(row)
        intCol = int(col) - 1
        intHeightInStack=int(heightInStack)

        currentSquare = self.board[intRow][intCol]

        if direction == 'GL':
            newRow, newCol = intRow - 1, intCol - 1
        elif direction == 'GD':
            newRow, newCol = intRow - 1, intCol + 1
        elif direction == 'DL':
            newRow, newCol = intRow + 1, intCol - 1
        elif direction == 'DD':
            newRow, newCol = intRow + 1, intCol + 1

        if not (0 <= newRow < self.rows) or not (0 <= newCol < self.rows):
            return

        newSquare = self.board[newRow][newCol]

        for i in range(intHeightInStack, currentSquare.returnNumberOfPieces()):
            piece = currentSquare.returnPiece(i)
            newSquare.add(piece)

        currentSquare.removePieces(intHeightInStack)
        if newSquare.checkIfCompleted():
            topPieceColor=newSquare.returnPiece(7).returnColor()
            if topPieceColor=='B':
                self.blue_player_points+=1
            else:
                self.red_player_points+=1
            newSquare.clearPieces()

    

def drawLabels(win, rows, boardWidth):
    font = pygame.font.Font(None, 36)
    for i in range(rows):
        letter = font.render(boardLabels[i], True, (0, 0, 0))
        win.blit(letter, (20, 40 + boardWidth / rows / 2 + boardWidth / rows * i))
        number = font.render(str(i + 1), True, (0, 0, 0))
        win.blit(number, (40 + boardWidth / rows / 2 + boardWidth / rows * i, 20))



               
               



          


    


                               









