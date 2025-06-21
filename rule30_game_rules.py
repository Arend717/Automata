# File: Rule30_GameRules.py
# This file contains the Rule 30 update logic

"""
This version only draws the bottom row (as you would in a Rule 30 visualization).

It uses a lookup table (dictionary) for the logic, as is common with Rule 30.

cells[-2] is the second-to-last row — the last row is calculated from it.

"""

import numpy as np

# Colors used for visualization
COLOR_BG = (10, 10, 10)            # Background color (0)
COLOR_GRID = (40, 40, 40)          # Grid color (not used in current draw)
COLOR_ALIVE_NEXT = (255, 255, 255) # Color when cell is 1

# Rule 30 lookup table: maps (left, center, right) to new state
rule_30 = {
    (1, 1, 1): 0,
    (1, 1, 0): 0,
    (1, 0, 1): 0,
    (1, 0, 0): 1,
    (0, 1, 1): 1,
    (0, 1, 0): 1,
    (0, 0, 1): 1,
    (0, 0, 0): 0,
}

def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros_like(cells)

    rows, cols = cells.shape

    # Copy the previous state
    updated_cells[:-1] = cells[:-1]

    # Compute the new row based on the previous one
    for col in range(1, cols - 1):
        left = cells[-2, col - 1]
        center = cells[-2, col]
        right = cells[-2, col + 1]

        new_state = rule_30[(left, center, right)]
        updated_cells[-1, col] = new_state

        color = COLOR_BG if new_state == 0 else COLOR_ALIVE_NEXT

        if screen is not None:
            import pygame
            pygame.draw.rect(
                screen, color,
                (col * size, (rows - 1) * size, size - 1, size - 1)
            )

    return updated_cells
