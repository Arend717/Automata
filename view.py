# File: visual.py
# This file handles the visualization of the CA grid using Pygame

import pygame

def draw_grid(screen, cells, size, colors):
    """
    Draws the entire grid on the screen.
    :param screen: Pygame screen surface
    :param cells: 2D numpy array of cell states
    :param size: Size of each cell in pixels
    :param colors: Dictionary mapping cell states to RGB colors
    """
    for row in range(len(cells)):
        for col in range(len(cells[0])):
            state = cells[row][col]
            color = colors[state]
            pygame.draw.rect(
                screen, color,
                (col * size, row * size, size - 1, size - 1)
            )
