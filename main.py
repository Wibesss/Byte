import pygame
import sys

WINDOW_WIDTH = 1680
BOARD_WIDTH = 880
ROWS = 8

RED_PLAYER = pygame.image.load('CheckersRed.png')
BLUE_PLAYER = pygame.image.load('CheckersBlue.png')
pygame.init()
ClientWindow = pygame.display.set_mode((WINDOW_WIDTH, BOARD_WIDTH + 100))
pygame.display.set_caption('Checkers')
boardLabels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
priorMoves = []

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (235, 168, 52)
BLUE = (76, 252, 241)

# GUI
GUI_WIDTH = 800
GUI_COLOR = (150, 150, 150)

FONT = pygame.font.Font(None, 36)

MOVE_INPUT_RECT = pygame.Rect(BOARD_WIDTH + 50, 300, 270, 150)
MOVE_INPUT_BOXES = [
    pygame.Rect(MOVE_INPUT_RECT.left + 50, MOVE_INPUT_RECT.top, 270, 32),
    pygame.Rect(MOVE_INPUT_RECT.left + 50, MOVE_INPUT_RECT.top + 50, 270, 32),
    pygame.Rect(MOVE_INPUT_RECT.left + 50, MOVE_INPUT_RECT.top + 100, 270, 32),
    pygame.Rect(MOVE_INPUT_RECT.left + 50, MOVE_INPUT_RECT.top + 150, 270, 32),
]
BTN_MOVE_RECT = pygame.Rect(MOVE_INPUT_RECT.left + 50, MOVE_INPUT_RECT.top + 200, 160, 50)
MOVE_INPUT_TEXTS = ["", "", "", ""]
PIECE_INPUT_TEXTS=["","",""]
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
color = COLOR_ACTIVE
MOVE_INPUT_TEXTS_SURFACE = [FONT.render(text, True, color) for text in MOVE_INPUT_TEXTS]
PIECE_INPUT_TEXTS_SURFACE = [FONT.render(text, True, color) for text in PIECE_INPUT_TEXTS]

PIECE_INPUT_RECT = pygame.Rect(BOARD_WIDTH + 50+ 350, 300, 270, 150)
PIECE_INPUT_BOXES = [
    pygame.Rect(PIECE_INPUT_RECT.left + 50, PIECE_INPUT_RECT.top, 270, 32),
    pygame.Rect(PIECE_INPUT_RECT.left + 50, PIECE_INPUT_RECT.top + 50, 270, 32),
    pygame.Rect(PIECE_INPUT_RECT.left + 50, PIECE_INPUT_RECT.top + 100, 270, 32),

]
BTN_PIECE_RECT = pygame.Rect(PIECE_INPUT_RECT.left + 50, PIECE_INPUT_RECT.top + 200, 160, 50)

BUTTON_RECT = pygame.Rect(BOARD_WIDTH + 100, 250, 160, 50)
BUTTON_COLOR = pygame.Color('dodgerblue2')

BTN_CLEAN_BOARD_RECT = pygame.Rect(BOARD_WIDTH + 100, BOARD_WIDTH, 180, 50)
BTN_CLEAN_BOARD_COLOR = pygame.Color('red')

BTN_RESET_BOARD_RECT = pygame.Rect(BOARD_WIDTH + 100, BOARD_WIDTH - 70, 180, 50)


class Piece:
    def __init__(self, team):
        self.team = team
        self.image = BLUE_PLAYER if self.team == 'B' else RED_PLAYER

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
        pygame.draw.rect(window, self.colour, (self.x + 50, self.y + 50, BOARD_WIDTH / ROWS, BOARD_WIDTH / ROWS))
        i = 0
        for piece in self.pieces:
            window.blit(pygame.transform.scale(piece.image, (BOARD_WIDTH / ROWS, BOARD_WIDTH / ROWS)),
                        (self.x + 50, self.y + 50 - i * BOARD_WIDTH / ROWS * 0.15625))
            i += 1

    def clearPieces(self):
        self.pieces.clear()

    def returnNumberOfPieces(self):
        return len(self.pieces)  


def update_display(win, grid, rows, width):
    drawGrid(win, rows, width)
    drawGui(win)
    drawLabels(win)
    for row in grid:
        for spot in row:
            spot.draw(win)
    pygame.display.update()


def makeBoard(rows, width):
    board = []
    nodeWidth = width // rows
    for i in range(rows):
        board.append([])
        for j in range(rows):
            node = Node(j, i, nodeWidth)
            if abs(i - j) % 2 == 0:
                node.colour = BLACK
            if abs(i) % 2 == 0 and rows - 1 > i > 0 == abs(i - j) % 2:
                node.add(Piece("B"))
            if abs(i) % 2 == 1 and i < rows - 1 and abs(i - j) % 2 == 0:
                node.add(Piece("R"))
            board[i].append(node)
    return board


def clearBoard(board):
    for row in board:
        for col in row:
            col.clearPieces()


def resetBoard(board):
    clearBoard(board)
    board.clear()
    nodeWidth = BOARD_WIDTH / ROWS
    for i in range(ROWS):
        board.append([])
        for j in range(ROWS):
            node = Node(j, i, nodeWidth)
            if abs(i - j) % 2 == 0:
                node.colour = BLACK
            if abs(i) % 2 == 0 and ROWS - 1 > i > 0 == abs(i - j) % 2:
                node.add(Piece("B"))
            if abs(i) % 2 == 1 and i < ROWS - 1 and abs(i - j) % 2 == 0:
                node.add(Piece("R"))
            board[i].append(node)


def drawGrid(win, rows, width):
    nodeWidth = width // ROWS
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * nodeWidth), (width, i * nodeWidth))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * nodeWidth, 0), (j * nodeWidth, width))


def getNode(rows, width):
    nodeWidth = width // rows
    RowX, RowY = pygame.mouse.get_pos()
    Row = RowX // nodeWidth
    Col = RowY // nodeWidth
    return Col, Row


def drawLabels(win):
    font = pygame.font.Font(None, 36)
    for i in range(ROWS):
        letter = FONT.render(boardLabels[i], True, (0, 0, 0))
        win.blit(letter, (20, 40 + BOARD_WIDTH / ROWS / 2 + BOARD_WIDTH / ROWS * i))
        number = FONT.render(str(i + 1), True, (0, 0, 0))
        win.blit(number, (40 + BOARD_WIDTH / ROWS / 2 + BOARD_WIDTH / ROWS * i, 20))


def drawGui(win):
    pygame.draw.rect(win, GUI_COLOR, (BOARD_WIDTH + 50, 0, GUI_WIDTH, BOARD_WIDTH + 100))
    pygame.draw.rect(win, GUI_COLOR, (0, 0, 50, BOARD_WIDTH + 50))
    pygame.draw.rect(win, GUI_COLOR, (50, 0, BOARD_WIDTH + 50, 50))
    pygame.draw.rect(win, GUI_COLOR, (0, BOARD_WIDTH + 50, BOARD_WIDTH + 50, BOARD_WIDTH + 50))

    for i, box in enumerate(MOVE_INPUT_BOXES):
        pygame.draw.rect(win, color, box, 2)
        win.blit(MOVE_INPUT_TEXTS_SURFACE[i], (box.x + 5, box.y + 5))

    for i, box in enumerate(PIECE_INPUT_BOXES):
        pygame.draw.rect(win, color, box, 2)
        win.blit(PIECE_INPUT_TEXTS_SURFACE[i], (box.x + 5, box.y + 5))

    pygame.draw.rect(win, BUTTON_COLOR, BTN_MOVE_RECT)
    font = pygame.font.Font(None, 36)
    button_text = font.render("Odigraj", True, (255, 255, 255))
    win.blit(button_text, (BTN_MOVE_RECT.x + 20, BTN_MOVE_RECT.y + 15))

    pygame.draw.rect(win, BUTTON_COLOR, BTN_PIECE_RECT)
    font = pygame.font.Font(None, 36)
    button_text = font.render("Dodaj", True, (255, 255, 255))
    win.blit(button_text, (BTN_PIECE_RECT.x + 20, BTN_PIECE_RECT.y + 15))



    pygame.draw.rect(win, BTN_CLEAN_BOARD_COLOR, BTN_CLEAN_BOARD_RECT)
    font = pygame.font.Font(None, 36)
    button_text = font.render("Clear Board", True, (255, 255, 255))
    win.blit(button_text, (BTN_CLEAN_BOARD_RECT.x + 20, BTN_CLEAN_BOARD_RECT.y + 15))

    pygame.draw.rect(win, BUTTON_COLOR, BTN_RESET_BOARD_RECT)
    font = pygame.font.Font(None, 36)
    button_text = font.render("Reset Board", True, (255, 255, 255))
    win.blit(button_text, (BTN_RESET_BOARD_RECT.x + 20, BTN_RESET_BOARD_RECT.y + 15))


def handleButtonClick(mouse_pos, board):
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


# def checkIfMoveValid(row,col,depth,direction):


def handleInputEvent(event, active_input_list, active_input_index):
    global color

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            active_input_list[active_input_index] = active_input_list[active_input_index][:-1]
        else:
            active_input_list[active_input_index] += event.unicode

        active_input_surface = FONT.render(active_input_list[active_input_index], True, color)

        return active_input_surface

    return None

def addPieceToNode(row,col,color,board):

    if board[row][col].returnNumberOfPieces() == 7:
        raise ValueError("You cannot add more than 7 pieces to a stack")

    if 0 <= row < len(board) and 0 <= col < len(board[0]):
        if color not in ["B", "R"]:
            raise ValueError("Invalid color. Accepted values are 'B' or 'R'.")
    
        new_piece = Piece(color)
        board[row][col].add(new_piece)




def main(width, rows, firstMove):
    board = makeBoard(rows, width)
    highlightedPiece = None

    MOVE_ACTIVE_INPUT = None
    PIECE_ACTIVE_INPUT = None

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
                input_type, clicked_input = handleButtonClick(pygame.mouse.get_pos(), board)
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
                        resetBoard(board)
                    elif input_type == "button_move":
                        if all(text != '' for text in MOVE_INPUT_TEXTS):
                            print("Move Button Clicked - Text inputs:", MOVE_INPUT_TEXTS)
                    elif input_type == "button_piece":
                        if all(text != '' for text in PIECE_INPUT_TEXTS):
                            try:
                                row = boardLabels.index(PIECE_INPUT_TEXTS[0])
                                col = int(PIECE_INPUT_TEXTS[1])-1  
                                color = PIECE_INPUT_TEXTS[2]
                                addPieceToNode(row, col, color,board)
                            except ValueError as e:
                                print(f"Error: {e}")

        update_display(ClientWindow, board, rows, width)


ChosenInitialState = []

main(BOARD_WIDTH, ROWS, "PLAYER")
