# File: GOL_GameRules.py
# This file contains the Game of Life update logic

import numpy as np

# Colors used for visualization
COLOR_BG = (10, 10, 10)           # Background color (dead cell)
COLOR_GRID = (40, 40, 40)         # Grid color (not used in current draw)
COLOR_DIE_NEXT = (170, 170, 170)  # Color when cell is dying
COLOR_ALIVE_NEXT = (255, 255, 255) # Color when cell becomes alive

def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros(cells.shape)  # New state of the grid

    for row, col in np.ndindex(cells.shape):
        # Count alive neighbors
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]

        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT

        # Apply Game of Life rules
        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_DIE_NEXT
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        # Draw cell rectangle if a screen is passed
        if screen is not None:
            import pygame  # Import locally to avoid circular imports
            pygame.draw.rect(
                screen, color,
                (col * size, row * size, size - 1, size - 1)
            )

    return updated_cells