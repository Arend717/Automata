# file: interaction.py

import pygame
import sys
import random
import numpy as np

# Custom modules for cellular automaton logic
from rule30_rule import rule30
from one_dimensional import OneDimensional
from two_dimensional import TwoDimensional
from gol_rule import gol_rule
from threestates_class import threestates_class

# Grid and screen settings
CELL_SIZE = 12
GRID_WIDTH = 100
GRID_HEIGHT = 50
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
FONT_SIZE = 36

# Colors used for UI
BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (227, 209, 166)
HIGHLIGHT_COLOR = (38, 57, 74)

# Menu option labels
MENU_OPTIONS = [
    "1. Conway's Game of Life",
    "2. Rule 30 - Symmetric Start (pyramid)",
    "3. Rule 30 - Random Start",
    "4. Rule 30 - Classic"
    "5. Three-State Rule 30"
]

# --------------------------
# Display the start menu
# --------------------------
def show_start_menu(screen, font):
    pygame.font.init()
    font = pygame.font.SysFont(None, FONT_SIZE)
    selected_option = None

    while selected_option is None:
        screen.fill(BACKGROUND_COLOR)

        # Render and draw each menu option
        for i, option in enumerate(MENU_OPTIONS):
            text = font.render(option, True, TEXT_COLOR)
            screen.blit(text, (100, 100 + i * (FONT_SIZE + 20)))

        # Draw the welcome prompt
        prompt = font.render("Welcome to CA! Press 1-5 to choose.", True, HIGHLIGHT_COLOR)
        screen.blit(prompt, (100, 100 + len(MENU_OPTIONS) * (FONT_SIZE + 30)))

        pygame.display.flip()

        # Handle keyboard input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Only allow keys 1-4 to make a selection
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    selected_option = int(event.unicode)
    return selected_option

# --------------------------
# Shared key event handling
# --------------------------

def handle_common_events(event):
    if event.type == pygame.QUIT: 
        return "exit"  # User clicks close window
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return "exit"  # Esc = quit game
        elif event.key == pygame.K_RETURN:
            return "menu"  # Enter = back to main menu
        elif event.key == pygame.K_SPACE:
            return "pause"  # Space = pause/unpause
    return None  # No relevant key pressed

# --------------------------
# Game of Life mouse control
# --------------------------
def handle_gol_events(event, ca, cell_size, grid_size):
    if event.type == pygame.MOUSEBUTTONDOWN:
        # Calculate grid position from mouse click
        mouse_x, mouse_y = pygame.mouse.get_pos()
        col = mouse_x // cell_size
        row = mouse_y // cell_size

        # If within grid, toggle cell state (0 ↔ 1)
        if 0 <= row < grid_size[0] and 0 <= col < grid_size[1]:
            ca.cells[row, col] = 1 - ca.cells[row, col]

# --------------------------
# Initialize Rule 30 variants
# --------------------------
def initialize_case(case_number):
    grid_width = 100

    # Case 0 and 1: Middle cell set to 1 (pyramid)
    if case_number == 0: 
        state = np.zeros(grid_width, dtype=int)
        state[grid_width // 2] = 1
    elif case_number == 1:
        state = np.zeros(grid_width, dtype=int)
        state[grid_width // 2] = 1

    # Case 2: Every 20th cell gets random 0 or 1
    elif case_number == 2:
        state = np.zeros(grid_width, dtype=int)
        for i in range(0, grid_width, 20):
            state[i] = random.choice([0, 1])

    # Case 3 (default): Fully random initial state
    elif case_number == 3:
        state = np.random.randint(0, 2, size=grid_width)

    # Case 4：threestates Rule 30
    else:
        return threestates_class()

    # Return a one-dimensional automaton using Rule 30
    return OneDimensional(cells=grid_width, rule_func=rule30, initial_state=state)
