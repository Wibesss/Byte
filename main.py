import pygame
import sys

WINDOW_WIDTH = 1280
BOARD_WIDTH = 880
ROWS = 8

COMPUTER = pygame.image.load('CheckersRed.png')
PLAYER = pygame.image.load('CheckersBlue.png')
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
GUI_WIDTH = 400
GUI_COLOR = (150, 150, 150)

FONT = pygame.font.Font(None, 36)
input_boxes = [
    pygame.Rect(BOARD_WIDTH + 100, 50, 270, 32),
    pygame.Rect(BOARD_WIDTH + 100, 100, 270, 32),
    pygame.Rect(BOARD_WIDTH + 100, 150, 270, 32),
    pygame.Rect(BOARD_WIDTH + 100, 200, 270, 32),
]
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
color = COLOR_INACTIVE
input_texts = ["", "", "", ""]
text_surfaces = [FONT.render(text, True, color) for text in input_texts]







BUTTON_RECT = pygame.Rect(BOARD_WIDTH + 100, 250, 160, 50)
BUTTON_COLOR = pygame.Color('dodgerblue2')


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
        pygame.draw.rect(window, self.colour, (self.x + 50, self.y + 50, BOARD_WIDTH / ROWS, BOARD_WIDTH / ROWS))
        i = 0
        for piece in self.pieces:
            window.blit(pygame.transform.scale(piece.image, (BOARD_WIDTH / ROWS, BOARD_WIDTH / ROWS)),
                        (self.x + 50, self.y + 50 - i * BOARD_WIDTH / ROWS * 0.15625))
            i += 1


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
                node.add(Piece("COMPUTER"))
            if abs(i) % 2 == 1 and i < rows - 1 and abs(i - j) % 2 == 0:
                node.add(Piece("PLAYER"))
            board[i].append(node)
    return board


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
        win.blit(letter, (20, 40 + BOARD_WIDTH/ROWS/2 + BOARD_WIDTH/ROWS * i))
        number = FONT.render(str(i + 1), True, (0, 0, 0))
        win.blit(number, (40 + BOARD_WIDTH / ROWS / 2 + BOARD_WIDTH / ROWS * i, 20 ))


def drawGui(win):
    pygame.draw.rect(win, GUI_COLOR, (BOARD_WIDTH + 50, 0, GUI_WIDTH, BOARD_WIDTH + 100))
    pygame.draw.rect(win, GUI_COLOR, (0, 0, 50, BOARD_WIDTH + 50))
    pygame.draw.rect(win, GUI_COLOR, (50, 0, BOARD_WIDTH + 50, 50))
    pygame.draw.rect(win, GUI_COLOR, (0, BOARD_WIDTH + 50, BOARD_WIDTH + 50, BOARD_WIDTH + 50))

    for i, box in enumerate(input_boxes):
        pygame.draw.rect(win, color, box, 2)
        win.blit(text_surfaces[i], (box.x + 5, box.y + 5))

    # Draw the button
    pygame.draw.rect(win, BUTTON_COLOR, BUTTON_RECT)
    font = pygame.font.Font(None, 36)
    button_text = font.render("Odigraj", True, (255, 255, 255))
    win.blit(button_text, (BUTTON_RECT.x + 20, BUTTON_RECT.y + 15))


def handleButtonClick(mouse_pos, input_boxes):
    for i, box in enumerate(input_boxes):
        if box.collidepoint(mouse_pos):
            return i  
    
    if BUTTON_RECT.collidepoint(mouse_pos):
        return "button"

    
    return None

#def checkIfMoveValid(row,col,depth,direction):
    

    


def handleInputEvent(event, input_texts, active_input):
    global color, text_surfaces

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            input_texts[active_input] = input_texts[active_input][:-1]
        else:
            input_texts[active_input] += event.unicode

        # Update the text surface for the active input
        text_surfaces[active_input] = FONT.render(input_texts[active_input], True, color)


def main(width, rows, firstMove):
    board = makeBoard(rows, width)
    highlightedPiece = None

    active_input = 0


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('EXIT SUCCESSFUL')
                pygame.quit()
                sys.exit()

            handleInputEvent(event, input_texts, active_input)

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_input = handleButtonClick(pygame.mouse.get_pos(), input_boxes)
                if clicked_input == "button":
                    if all(text != "" for text in input_texts):
                        print("Button clicked - Text inputs:", input_texts)
                elif clicked_input is not None:
                    active_input = clicked_input

        update_display(ClientWindow, board, rows, width)


ChosenInitialState = []

main(BOARD_WIDTH, ROWS, "PLAYER")
