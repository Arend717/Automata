# File: main_visual.py

import pygame
import numpy as np
from two_dimensional import TwoDimensional
from gol_rule import gol_rule
from view import draw_grid

# Initialise pygame
pygame.init()
cell_size = 20
grid_size = (25, 25)
screen = pygame.display.set_mode((grid_size[1] * cell_size, grid_size[0] * cell_size))
pygame.display.set_caption("Game of Life")

# Create CA
ca = TwoDimensional(grid_size, gol_rule, 2, boundary='fixed')
ca.cells[12, 11:14] = 1
ca.cells[11, 13] = 1
ca.cells[10, 12] = 1

running = True
paused = False
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))
    draw_grid(screen, ca.cells, cell_size)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = True

        # Pause/unpause with SPACE
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

        # Toggle cells with mouse click
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = mouse_x // cell_size
            row = mouse_y // cell_size
            if 0 <= row < grid_size[0] and 0 <= col < grid_size[1]:
                ca.cells[row, col] = 1 - ca.cells[row, col]  # Toggle between 0 and 1

    if not paused:
        ca.evolve()
        clock.tick(5)  # Only evolve when not paused

pygame.quit()
