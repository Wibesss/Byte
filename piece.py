import pygame

RED_PLAYER = pygame.image.load('assets/CheckersRed.png')
BLUE_PLAYER = pygame.image.load('assets/CheckersBlue.png')


class Piece:
    def __init__(self, team):
        self.team = team
        self.image = BLUE_PLAYER if self.team == 'B' else RED_PLAYER
