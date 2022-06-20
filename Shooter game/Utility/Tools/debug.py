import pygame
from Utility import constants

pygame.font.init()

FONT = pygame.font.SysFont("monospace", 20)

def debug(text, x=50, y=50):
    """
    Displays debug text on the screen.
    """
    text = FONT.render(text, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.x = x
    text_rect.y = y
    constants.SCREEN.blit(text, text_rect)


