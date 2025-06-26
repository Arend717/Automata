# File: main_visual_1d.py

import pygame
import sys
import random
import numpy as np
from rule30_rule import rule30
from one_dimensional import OneDimensional

# Screen dimensions and grid size
CELL_SIZE = 8
GRID_WIDTH = 180
GRID_HEIGHT = 90
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def draw_grid(screen, grid, row):
    """
    Draw a single row of the cellular automaton.
    """
    for x in range(GRID_WIDTH):
        color = WHITE if grid.cells[x] == 1 else BLACK
        pygame.draw.rect(screen, color, (x * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def show_start_screen(screen, font, rule_func):
    """
    Display the start screen with 3 pattern choices.
    """
    screen.fill(BLACK)
    title = font.render("Choose a starting condition (1, 2, or 3):", True, WHITE)
    opt1 = font.render("1: One cell in the middle", True, WHITE)
    opt2 = font.render("2: Every 15th cell random", True, WHITE)
    opt3 = font.render("3: Asymmetric wave pattern", True, WHITE)
    screen.blit(title, (50, 100))
    screen.blit(opt1, (50, 160))
    screen.blit(opt2, (50, 200))
    screen.blit(opt3, (50, 240))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return initialize_case(1, rule_func)
                elif event.key == pygame.K_2:
                    return initialize_case(2, rule_func)
                elif event.key == pygame.K_3:
                    return initialize_case(3, rule_func)

def initialize_case(case, rule_func):
    """
    Initialize grid with selected starting pattern.
    """
    # grid = Rule30Grid(GRID_WIDTH)
    grid = OneDimensional(GRID_WIDTH, rule_func)
    if case == 1:
        grid.cells[GRID_WIDTH // 2] = 1  # Single center cell
    elif case == 2:
        for i in range(0, GRID_WIDTH, 15):
            grid.cells[i] = random.choice([0, 1])  # Every 15th cell random
    elif case == 3:
        for i in range(GRID_WIDTH):
        # Set cell active if the binary representation of i has an odd number of 1s
        # This creates a complex, seemingly random initial pattern with some structure
            if bin(i).count('1') % 2 == 1:
                grid.cells[i] = 1
    return grid

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Rule 30 - 1D Cellular Automaton")
    font = pygame.font.SysFont(None, 28)

    clock = pygame.time.Clock()

    rule_func = rule30
    grid = show_start_screen(screen, font, rule_func)

    history = []  # Stores previous generations
    running = True
    paused = False
    row = 0
    screen.fill(BLACK)
    while running:

        # Draw current row and evolve if not paused
        if not paused:
            draw_grid(screen, grid, row)
            # Append a copy of the current grid to history
            past = OneDimensional(GRID_WIDTH, rule_func)
            past.cells[:] = np.copy(grid.cells)
            history.append(past)

            if row < GRID_HEIGHT - 1:
                grid.evolve()
                row += 1
            
            print(history)

        pygame.display.flip()
        clock.tick(10)  # 10 frames per second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False  # Exit on Enter
                elif event.key == pygame.K_SPACE:
                    paused = not paused  # Pause on Space

    pygame.quit()

if __name__ == "__main__":
    main()