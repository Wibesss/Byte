import sys
import math
from board import *
from gui import *
from constants import BOARD_WIDTH
from constants import ROWS
from constants import COLOR_ACTIVE

WINDOW_WIDTH = 1680

pygame.init()

FONT = pygame.font.Font(None, 36)
MOVE_INPUT_TEXTS = ["", "", "", ""]
PIECE_INPUT_TEXTS = ["", "", ""]
MOVE_INPUT_TEXTS_SURFACE = [FONT.render(text, True, COLOR_ACTIVE) for text in MOVE_INPUT_TEXTS]
PIECE_INPUT_TEXTS_SURFACE = [FONT.render(text, True, COLOR_ACTIVE) for text in PIECE_INPUT_TEXTS]

COMPUTER = "B"
PLAYER = "R"
CURRENT_TURN="B"

RED_PLAYER_POINTS=0
BLUE_PLAYER_POINTS=0


def getNumberOfRows():
    global ROWS
    while True:
        ROWS = int(input("Choose the number of rows (8, 10, or 16): "))
        if ROWS not in [8, 10, 16]:
            print("Invalid input. Please choose 8, 10, or 16.")
        else:
            return

def handleButtonClick(mouse_pos):
    for i, box in enumerate(MOVE_INPUT_BOXES):
        if box.collidepoint(mouse_pos):
            return "move", i
    for i, box in enumerate(PIECE_INPUT_BOXES):
        if box.collidepoint(mouse_pos):
            return "piece", i

    if BTN_MOVE_RECT.collidepoint(mouse_pos):
        return "button_move", None

    if BTN_PIECE_RECT.collidepoint(mouse_pos):
        return "button_piece", None

    if BTN_CLEAN_BOARD_RECT.collidepoint(mouse_pos):
        return "button_clean", None

    if BTN_RESET_BOARD_RECT.collidepoint(mouse_pos):
        return "button_reset", None

    return None, None

def changeTurn():
    global CURRENT_TURN
    if CURRENT_TURN == "B":
        print("Next turn: RED")
        CURRENT_TURN="R"
    else:
        print("Next turn: BLUE")
        CURRENT_TURN = "B"

def playMove(row, col, heightInStack, direction, board, ROWS):
    global BLUE_PLAYER_POINTS
    global RED_PLAYER_POINTS
    intRow = boardLabels.index(row)
    intCol = int(col) - 1
    intHeightInStack=int(heightInStack)

    currentSquare = board[intRow][intCol]

    if direction == 'GL':
        newRow, newCol = intRow - 1, intCol - 1
    elif direction == 'GD':
        newRow, newCol = intRow - 1, intCol + 1
    elif direction == 'DL':
        newRow, newCol = intRow + 1, intCol - 1
    elif direction == 'DD':
        newRow, newCol = intRow + 1, intCol + 1

    if not (0 <= newRow < ROWS) or not (0 <= newCol < ROWS):
        return

    newSquare = board[newRow][newCol]

    for i in range(intHeightInStack, currentSquare.returnNumberOfPieces()):
        piece = currentSquare.returnPiece(i)
        newSquare.add(piece)

    currentSquare.removePieces(intHeightInStack)
    if newSquare.checkIfCompleted():
        topPieceColor=newSquare.returnPiece(7).returnColor()
        if topPieceColor=='B':
            BLUE_PLAYER_POINTS+=1
        else:
            RED_PLAYER_POINTS+=1
        newSquare.clearPieces()


def handleInputEvent(event, active_input_list, active_input_index):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            active_input_list[active_input_index] = active_input_list[active_input_index][:-1]
        else:
            active_input_list[active_input_index] += event.unicode

        active_input_surface = FONT.render(active_input_list[active_input_index], True, COLOR_ACTIVE)

        return active_input_surface

    return None

def update_display(win, grid, rows, width):
    if CURRENT_TURN=="B":
        drawGui(win, MOVE_INPUT_TEXTS_SURFACE, PIECE_INPUT_TEXTS_SURFACE,"BLUE")
    else:
        drawGui(win, MOVE_INPUT_TEXTS_SURFACE, PIECE_INPUT_TEXTS_SURFACE,"RED")
    drawLabels(win, rows, width)
    for row in grid:
        for spot in row:
            spot.draw(win,rows)
    pygame.display.update()


def giveColors(first_move):
    global PLAYER
    global COMPUTER
    if first_move == "PLAYER":
        COMPUTER = "R"
        PLAYER = "B"


def isGameFinished(board):
    global RED_PLAYER_POINTS, BLUE_PLAYER_POINTS, ROWS
    if isBoardClear(board):
        return True
    elif RED_PLAYER_POINTS == math.ceil(((ROWS/2)*(ROWS-2)/8)/2):
        return True
    elif BLUE_PLAYER_POINTS == math.ceil(((ROWS/2)*(ROWS-2)/8)/2):
        return True
    return False




def main():
    MOVE_ACTIVE_INPUT = None
    PIECE_ACTIVE_INPUT = None
    global PIECE_INPUT_TEXTS
    global PIECE_INPUT_TEXTS_SURFACE
    global ROWS
    global BOARD_WIDTH

    getNumberOfRows()

    giveColors(input("Choose who plays first PLAYER or COMPUTER: "))

    board = makeBoard(ROWS, BOARD_WIDTH)

    ClientWindow = pygame.display.set_mode((WINDOW_WIDTH, BOARD_WIDTH + 100))
    pygame.display.set_caption('Bytes')

    getAllMoves(board, ROWS, CURRENT_TURN)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('EXIT SUCCESSFUL')
                pygame.quit()
                sys.exit()
               

            if MOVE_ACTIVE_INPUT is not None:
                move_input_surface = handleInputEvent(event, MOVE_INPUT_TEXTS, MOVE_ACTIVE_INPUT)
                if move_input_surface is not None:
                    MOVE_INPUT_TEXTS_SURFACE[MOVE_ACTIVE_INPUT] = move_input_surface
            elif PIECE_ACTIVE_INPUT is not None:
                piece_input_surface = handleInputEvent(event, PIECE_INPUT_TEXTS, PIECE_ACTIVE_INPUT)
                if piece_input_surface is not None:
                    PIECE_INPUT_TEXTS_SURFACE[PIECE_ACTIVE_INPUT] = piece_input_surface

            if event.type == pygame.MOUSEBUTTONDOWN:
                input_type, clicked_input = handleButtonClick(pygame.mouse.get_pos())

                if clicked_input is not None:
                    if input_type == "move":
                        MOVE_ACTIVE_INPUT = clicked_input
                        PIECE_ACTIVE_INPUT = None

                    elif input_type == "piece":
                        PIECE_ACTIVE_INPUT = clicked_input
                        MOVE_ACTIVE_INPUT = None

                elif clicked_input is None and input_type is not None:
                    if input_type == "button_clean":
                        clearBoard(board)

                    elif input_type == "button_reset":
                        resetBoard(board, ROWS, BOARD_WIDTH)

                    elif input_type == "button_move":
                        if all(text != '' for text in MOVE_INPUT_TEXTS):
                            row = MOVE_INPUT_TEXTS[0]
                            col = MOVE_INPUT_TEXTS[1]
                            heightInStack = MOVE_INPUT_TEXTS[2]
                            direction = MOVE_INPUT_TEXTS[3]
                            if checkIfMoveIsValid(row, col, heightInStack, direction, board,ROWS,CURRENT_TURN):
                                changeTurn()
                                playMove(row, col, heightInStack, direction, board,ROWS)
                                print("Red Points:",RED_PLAYER_POINTS)
                                print("Blue Points:",BLUE_PLAYER_POINTS)
                                if isGameFinished(board):
                                    print('EXIT SUCCESSFUL')
                                    pygame.quit()
                                    sys.exit()
                                getAllMoves(board, ROWS, CURRENT_TURN)
                              

                    elif input_type == "button_piece":
                        if all(text != '' for text in PIECE_INPUT_TEXTS):
                            row = PIECE_INPUT_TEXTS[0]
                            col = PIECE_INPUT_TEXTS[1]
                            color = PIECE_INPUT_TEXTS[2]
                            addPieceToSquare(row, col, color, board,ROWS)
                            # PIECE_INPUT_TEXTS = ["", "", ""]
                            # PIECE_INPUT_TEXTS_SURFACE = [FONT.render(text, True, COLOR_ACTIVE) for text in PIECE_INPUT_TEXTS]
                        
        update_display(ClientWindow, board, ROWS, BOARD_WIDTH)


if __name__ == "__main__":
    main()
