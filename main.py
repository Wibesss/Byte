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


RED_PLAYER_POINTS=0
BLUE_PLAYER_POINTS=0




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




def handleInputEvent(event, active_input_list, active_input_index):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            active_input_list[active_input_index] = active_input_list[active_input_index][:-1]
        else:
            active_input_list[active_input_index] += event.unicode

        active_input_surface = FONT.render(active_input_list[active_input_index], True, COLOR_ACTIVE)

        return active_input_surface

    return None




def giveColors(first_move):
    global PLAYER
    global COMPUTER
    if first_move == "PLAYER":
        COMPUTER = "R"
        PLAYER = "B"

def getNumberOfRows():
    while True:
        rows = int(input("Choose the number of rows (8, 10, or 16): "))
        if rows not in [8, 10, 16]:
            print("Invalid input. Please choose 8, 10, or 16.")
        else:
            return rows


def main():
    MOVE_ACTIVE_INPUT = None
    PIECE_ACTIVE_INPUT = None
    global PIECE_INPUT_TEXTS
    global PIECE_INPUT_TEXTS_SURFACE
    global BOARD_WIDTH

    rows=getNumberOfRows()

    #giveColors(input("Choose who plays first PLAYER or COMPUTER: "))

    board = Board(rows,BOARD_WIDTH)

    ClientWindow = pygame.display.set_mode((WINDOW_WIDTH, BOARD_WIDTH + 100))
    pygame.display.set_caption('Bytes')

    board.getAllMoves()

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
                        board.clearBoard()

                    elif input_type == "button_reset":
                        board.resetBoard()

                    elif input_type == "button_move":
                        if all(text != '' for text in MOVE_INPUT_TEXTS):
                            row = MOVE_INPUT_TEXTS[0]
                            col = MOVE_INPUT_TEXTS[1]
                            heightInStack = MOVE_INPUT_TEXTS[2]
                            direction = MOVE_INPUT_TEXTS[3]
                            if board.checkIfMoveIsValid(row, col, heightInStack, direction):
                                board.changeTurn()
                                board.playMove(row, col, heightInStack, direction)
                                print("Red Points:",RED_PLAYER_POINTS)
                                print("Blue Points:",BLUE_PLAYER_POINTS)
                                if  board.isGameFinished():
                                    print('EXIT SUCCESSFUL')
                                    pygame.quit()
                                    sys.exit()
                                board.getAllMoves()
                              

                    elif input_type == "button_piece":
                        if all(text != '' for text in PIECE_INPUT_TEXTS):
                            row = PIECE_INPUT_TEXTS[0]
                            col = PIECE_INPUT_TEXTS[1]
                            color = PIECE_INPUT_TEXTS[2]
                            board.addPieceToSquare(row, col, color)
                            # PIECE_INPUT_TEXTS = ["", "", ""]
                            # PIECE_INPUT_TEXTS_SURFACE = [FONT.render(text, True, COLOR_ACTIVE) for text in PIECE_INPUT_TEXTS]
                        
        board.updateDisplay(ClientWindow,MOVE_INPUT_TEXTS_SURFACE,PIECE_INPUT_TEXTS_SURFACE)


if __name__ == "__main__":
    main()
