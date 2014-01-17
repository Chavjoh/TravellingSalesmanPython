#!/usr/bin/python
# coding: latin-1

# Libraries import
import pygame
import sys

from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN

# If this is the main module, run this
if __name__ == '__main__':

    # Variables initialization
    color_black = [0, 0, 0]
    color_blue = [0, 0, 255]
    color_green = [0, 255, 0]
    color_red = [255, 0, 0]
    color_white = [255, 255, 255]

    # Pygame initialization
    pygame.init()
    pygame.display.set_caption('Travelling salesman solver - Chavaillaz & Jupille')

    # Create window and get useful informations
    screen_dimensions = (500, 500)
    screen_window = pygame.display.set_mode(screen_dimensions)
    screen_surface = pygame.display.get_surface()

    # Start main loop
    while True:
        screen_surface.fill(color_black)

        # Events management
        for event in pygame.event.get():

            # Red cross / Alt+F4
            if event.type == QUIT:
                sys.exit(0)

            # Keyboard events
            elif event.type == KEYDOWN:
                pass

            # Mouse button down events
            elif event.type == MOUSEBUTTONDOWN:
                pass

        # Flip display (double buffering)
        pygame.display.flip()
