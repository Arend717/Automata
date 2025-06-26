#file: main.py 

import pygame
import numpy as np
import sys

from two_dimensional import TwoDimensional
from gol_rule import gol_rule
from one_dimensional import one_dimensional
from rule30_rule import rule30
from interaction import (
    show_start_menu,
    handle_common_events,
    handle_gol_events,
    initialize_case
)

# -------------------------------
# Configuration
# -------------------------------
CELL_SIZE = 8
GRID_WIDTH = 180
GRID_HEIGHT = 90
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Colors
DEAD_COLOR = (227, 209, 166)
ALIVE_COLOR = (38, 57, 74)

# -------------------------------
# Drawing Functions
# -------------------------------
def draw_grid(screen, cells, size, alive_color=ALIVE_COLOR, dead_color=DEAD_COLOR):
    for row in range(len(cells)):
        for col in range(len(cells[0])):
            color = alive_color if cells[row][col] == 1 else dead_color
            pygame.draw.rect(
                screen, color,
                (col * size, row * size, size - 1, size - 1)
            )

def draw_rule30_row(screen, grid, row):
    for x in range(GRID_WIDTH):
        color = ALIVE_COLOR if grid.cells[x] == 1 else DEAD_COLOR
        pygame.draw.rect(screen, color, (x * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# -------------------------------
# Game Loop for Game of Life
# -------------------------------
def run_gol(screen):
    cell_size = CELL_SIZE
    grid_size = (GRID_HEIGHT, GRID_WIDTH)
    ca = TwoDimensional(grid_size, gol_rule, boundary='fixed')
    ca.cells[GRID_HEIGHT//2, GRID_WIDTH//2 - 1:GRID_WIDTH//2 + 2] = 1

    clock = pygame.time.Clock()
    paused = False
    running = True

    while running:
        screen.fill(DEAD_COLOR)
        draw_grid(screen, ca.cells, cell_size)
        pygame.display.flip()

        for event in pygame.event.get():
          result = handle_common_events(event)

          if result == "exit":
              pygame.quit()
              sys.exit()
          elif result == "menu":
              return
          elif result == "pause":
              paused = not paused


            handle_gol_events(event, ca, cell_size, grid_size)

        if not paused:
            ca.evolve()
            clock.tick(5)

# -------------------------------
# Game Loop for Rule 30
# -------------------------------
def run_rule30(screen, version):
    from interaction import Rule30Grid  # Avoid circular import

    clock = pygame.time.Clock()
    grid = initialize_case(version)

    history = []
    paused = False
    running = True
    row = 0

    while running:
        screen.fill(DEAD_COLOR)

        for i, past_grid in enumerate(history):
            draw_rule30_row(screen, past_grid, i)

        if not paused:
            draw_rule30_row(screen, grid, row)
            history.append(Rule30Grid(GRID_WIDTH, initial_state=np.copy(grid.cells)))

            if row < GRID_HEIGHT - 1:
                grid.evolve()
                row += 1

        pygame.display.flip()
        clock.tick(10)

        for event in pygame.event.get():
            result = handle_common_events(event, paused)
            if result == "exit":
                pygame.quit()
                sys.exit()
            elif result == "menu":
                return
            elif result == "pause":
                paused = not paused

# -------------------------------
# Main Entry
# -------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cellular Automaton")
    font = pygame.font.SysFont(None, 28)

    while True:
        choice = show_start_menu(screen, font)

        if choice == 1:
            run_gol(screen)
        elif choice in [2, 3, 4]:
            run_rule30(screen, version=choice - 1)

if __name__ == "__main__":
    main()
