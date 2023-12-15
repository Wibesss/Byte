import pygame
from constants import BOARD_WIDTH
from constants import COLOR_ACTIVE

GUI_WIDTH = 800
GUI_COLOR = (150, 150, 150)


MOVE_INPUT_RECT = pygame.Rect(BOARD_WIDTH + 300, 150, 270, 150)
MOVE_INPUT_BOXES = [
    pygame.Rect(MOVE_INPUT_RECT.left + 50, MOVE_INPUT_RECT.top, 270, 32),
    pygame.Rect(MOVE_INPUT_RECT.left + 50, MOVE_INPUT_RECT.top + 50, 270, 32),
    pygame.Rect(MOVE_INPUT_RECT.left + 50, MOVE_INPUT_RECT.top + 100, 270, 32),
    pygame.Rect(MOVE_INPUT_RECT.left + 50, MOVE_INPUT_RECT.top + 150, 270, 32),
]
BTN_MOVE_RECT = pygame.Rect(MOVE_INPUT_RECT.left + 50, MOVE_INPUT_RECT.top + 200, 200, 50)


PIECE_INPUT_RECT = pygame.Rect(BOARD_WIDTH + 300, 450, 270, 150)
PIECE_INPUT_BOXES = [
    pygame.Rect(PIECE_INPUT_RECT.left + 50, PIECE_INPUT_RECT.top, 270, 32),
    pygame.Rect(PIECE_INPUT_RECT.left + 50, PIECE_INPUT_RECT.top + 50, 270, 32),
    pygame.Rect(PIECE_INPUT_RECT.left + 50, PIECE_INPUT_RECT.top + 100, 270, 32),

]
BTN_PIECE_RECT = pygame.Rect(PIECE_INPUT_RECT.left + 50, PIECE_INPUT_RECT.top + 150, 200, 50)


BUTTON_COLOR = pygame.Color('dodgerblue2')

BTN_CLEAN_BOARD_RECT = pygame.Rect(BOARD_WIDTH + 200, BOARD_WIDTH, 180, 50)
BTN_CLEAN_BOARD_COLOR = pygame.Color('red')

BTN_RESET_BOARD_RECT = pygame.Rect(BOARD_WIDTH + 200, BOARD_WIDTH - 70, 180, 50)


def drawGui(win, MOVE_INPUT_TEXTS_SURFACE, PIECE_INPUT_TEXTS_SURFACE, current_turn, blue_player_points, red_player_points):
    pygame.draw.rect(win, GUI_COLOR, (BOARD_WIDTH + 50, 0, GUI_WIDTH, BOARD_WIDTH + 100))
    pygame.draw.rect(win, GUI_COLOR, (0, 0, 50, BOARD_WIDTH + 50))
    pygame.draw.rect(win, GUI_COLOR, (50, 0, BOARD_WIDTH + 50, 50))
    pygame.draw.rect(win, GUI_COLOR, (0, BOARD_WIDTH + 50, BOARD_WIDTH + 50, BOARD_WIDTH + 50))

    labels = ["Row:", "Col:", "Place on stack:", "Move direction:"]
    font = pygame.font.Font(None, 36)
    for i, label in enumerate(labels):
        label_surface = font.render(label, True, COLOR_ACTIVE)
        win.blit(label_surface, (MOVE_INPUT_BOXES[i].left - 250, MOVE_INPUT_BOXES[i].top + 5))

    for i, box in enumerate(MOVE_INPUT_BOXES):
        pygame.draw.rect(win, COLOR_ACTIVE, box, 2)
        win.blit(MOVE_INPUT_TEXTS_SURFACE[i], (box.x + 5, box.y + 5))

    piece_labels = ["Row:", "Col:", "Color (R or B):"]

    for i, label in enumerate(piece_labels):
        label_surface = font.render(label, True, COLOR_ACTIVE)
        win.blit(label_surface, (PIECE_INPUT_BOXES[i].left - 250, PIECE_INPUT_BOXES[i].top + 5))

    for i, box in enumerate(PIECE_INPUT_BOXES):
        pygame.draw.rect(win, COLOR_ACTIVE, box, 2)
        win.blit(PIECE_INPUT_TEXTS_SURFACE[i], (box.x + 5, box.y + 5))

    pygame.draw.rect(win, BUTTON_COLOR, BTN_MOVE_RECT)
    font = pygame.font.Font(None, 36)
    button_text = font.render("Confirm Move", True, (255, 255, 255))
    win.blit(button_text, (BTN_MOVE_RECT.x + 20, BTN_MOVE_RECT.y + 15))

    pygame.draw.rect(win, BUTTON_COLOR, BTN_PIECE_RECT)
    font = pygame.font.Font(None, 36)
    button_text = font.render("Add a Piece", True, (255, 255, 255))
    win.blit(button_text, (BTN_PIECE_RECT.x + 20, BTN_PIECE_RECT.y + 15))

    pygame.draw.rect(win, BTN_CLEAN_BOARD_COLOR, BTN_CLEAN_BOARD_RECT)
    font = pygame.font.Font(None, 36)
    button_text = font.render("Clear Board", True, (255, 255, 255))
    win.blit(button_text, (BTN_CLEAN_BOARD_RECT.x + 20, BTN_CLEAN_BOARD_RECT.y + 15))

    pygame.draw.rect(win, BUTTON_COLOR, BTN_RESET_BOARD_RECT)
    font = pygame.font.Font(None, 36)
    button_text = font.render("Reset Board", True, (255, 255, 255))
    win.blit(button_text, (BTN_RESET_BOARD_RECT.x + 20, BTN_RESET_BOARD_RECT.y + 15))

    if current_turn == "BLUE":
        turn_text = font.render(f"Current Turn: {current_turn}", True, (0, 0, 255))
    else:
        turn_text = font.render(f"Current Turn: {current_turn}", True, (255, 0, 0))
    win.blit(turn_text, (BOARD_WIDTH + 100, 100))

    blue_score_text = font.render(f"BLUE {blue_player_points}", True, (0, 0, 255))
    win.blit(blue_score_text, (BOARD_WIDTH + 100, 50))
    blue_score_text = font.render(f" : ", True, (0, 0, 0))
    win.blit(blue_score_text, (BOARD_WIDTH + 181, 50))
    red_score_text = font.render(f"{red_player_points} RED", True, (255, 0, 0))
    win.blit(red_score_text, (BOARD_WIDTH + 200, 50))
