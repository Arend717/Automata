import pygame
import numpy as np
import sys

# Importing custom modules for simulation rules and interactions
from two_dimensional import TwoDimensional
from gol_rule import gol_rule
from one_dimensional import OneDimensional
from rule30_rule import rule30
from interaction import (
    show_start_menu,
    handle_common_events,
    handle_gol_events,
    initialize_case
)

# Constants for grid and screen dimensions
CELL_SIZE = 12
GRID_WIDTH = 100   # number of columns
GRID_HEIGHT = 50   # number of rows
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Colors used for dead and alive cells
DEAD_COLOR = (227, 209, 166)
ALIVE_COLOR = (38, 57, 74)
DORMANT_COLOR = (171, 76, 3)


# Draw the 2D grid (Game of Life style)
def draw_grid(screen, cells, size, alive_color=ALIVE_COLOR, dead_color=DEAD_COLOR):
    for row in range(len(cells)):
        for col in range(len(cells[0])):
            color = alive_color if cells[row][col] == 1 else dead_color
            # Draw slightly smaller rectangles to leave grid lines visible
            pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))


# Draw one row for Rule 30 automaton
def draw_rule30_row(screen, cells, row_index):
    for x in range(len(cells)):
        color = ALIVE_COLOR if cells[x] == 1 else DEAD_COLOR
        rect = pygame.Rect(x * CELL_SIZE, row_index * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, color, rect)


# Run the 2D Conway's Game of Life simulation
def run_gol(screen):
    cell_size = CELL_SIZE
    grid_size = (GRID_HEIGHT, GRID_WIDTH)

    # Initialize the 2D automaton with a fixed boundary and central pattern
    ca = TwoDimensional(grid_size, gol_rule, boundary='fixed')
    ca.cells[GRID_HEIGHT // 2, GRID_WIDTH // 2 - 1:GRID_WIDTH // 2 + 2] = 1  # initial 3-cell "blinker"

    clock = pygame.time.Clock()
    paused = False
    running = True

    while running:
        screen.fill(DEAD_COLOR)
        draw_grid(screen, ca.cells, cell_size)  # draw current state
        pygame.display.flip()

        # Handle input and events
        for event in pygame.event.get():
            result = handle_common_events(event)
            if result == "exit":
                pygame.quit()
                sys.exit()
            elif result == "menu":
                return  # go back to main menu
            elif result == "pause":
                paused = not paused

            # Allow manual editing of grid when paused
            handle_gol_events(event, ca, cell_size, grid_size)

        # Advance simulation if not paused
        if not paused:
            ca.evolve()
            clock.tick(5)  # 5 frames per second


# Run the Rule 30 (1D) automaton
def run_rule30(screen, version):
    clock = pygame.time.Clock()
    grid, state = initialize_case(version)
    current_state = state
    history = []

    paused = False
    running = True
    row = 0

    while running:
        screen.fill(DEAD_COLOR)

        # Draw previous generations
        for i, past in enumerate(history):
            draw_rule30_row(screen, past, i)

        # Draw current state
        if not paused and row < GRID_HEIGHT:
            draw_rule30_row(screen, current_state, row)
            history.append(current_state.copy())

            new_state = []
            for i in range(len(current_state)):
                left = current_state[(i - 1) % len(current_state)]
                center = current_state[i]
                right = current_state[(i + 1) % len(current_state)]
                neighbors = (left, center, right)
                new_val = grid.rule((i,), center, neighbors)
                new_state.append(new_val)

            current_state = new_state
            row += 1

        pygame.display.flip()
        clock.tick(10)

        # Handle input
        for event in pygame.event.get():
            result = handle_common_events(event)
            if result == "exit":
                pygame.quit()
                sys.exit()
            elif result == "menu":
                return
            elif result == "pause":
                paused = not paused

# Entry point of the program
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cellular Automaton")

    font = pygame.font.SysFont(None, 28)  # font for menu text

    while True:
        # Show start menu and get user choice
        choice = show_start_menu(screen, font)

        if choice == 1:
            run_gol(screen)
        elif choice in [2, 3, 4]:  # Rule 30 cases
            run_rule30(screen, version=choice - 1)


# Run the main function if script is executed directly
if __name__ == "__main__":
    main()
