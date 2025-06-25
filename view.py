# File: view.py
# Handles visualization using Pygame

import pygame

DEFAULT_COLORS = {
    0: (227, 209, 166),        # dead cell
    1: (38, 57, 74),     # alive cell
}

def draw_grid(screen, cells, size, colors=DEFAULT_COLORS):
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
            color = colors.get(state, (255, 0, 0))  # fallback = red
            pygame.draw.rect(
                screen, color,
                (col * size, row * size, size - 1, size - 1)
            )
