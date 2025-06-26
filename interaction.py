# file: interaction.py

import pygame
import sys
import random
import numpy as np
from rule30_rule import rule30
from one_dimensional import one_dimensional
from two_dimensional import TwoDimensional
from gol_rule import gol_rule

CELL_SIZE = 12
GRID_WIDTH = 100
GRID_HEIGHT = 50
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
FONT_SIZE = 36

BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (227, 209, 166)
HIGHLIGHT_COLOR = (38, 57, 74)

MENU_OPTIONS = [
    "1. Conway's Game of Life",
    "2. Rule 30 - Symmetric Start (pyramid)",
    "3. Rule 30 - Random Start",
    "4. Rule 30 - Classic"
]
#Creating the start screen
def show_start_menu(screen, font):
    pygame.font.init()
    font = pygame.font.SysFont(None, FONT_SIZE)
    selected_option = None

    while selected_option is None:
        screen.fill(BACKGROUND_COLOR)

        for i, option in enumerate(MENU_OPTIONS):
            text = font.render(option, True, TEXT_COLOR)
            screen.blit(text, (100, 100 + i * (FONT_SIZE + 20)))

        prompt = font.render("Welcome to CA! Press 1-4 to choose.", True, HIGHLIGHT_COLOR)
        screen.blit(prompt, (100, 100 + len(MENU_OPTIONS) * (FONT_SIZE + 30)))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    selected_option = int(event.unicode)
    return selected_option

#Interactions used for both games 
def handle_common_events(event):
    if event.type == pygame.QUIT: 
        return "exit" 
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE: #esc = quit if you are in a game 
            return "exit"
        elif event.key == pygame.K_RETURN: #return = back to menu 
            return "menu"
        elif event.key == pygame.K_SPACE: #space = pause game 
            return "pause"
    return None

#Interactions only used in Game of Life 
def handle_gol_events(event, ca, cell_size, grid_size):
    if event.type == pygame.MOUSEBUTTONDOWN: #Toggle cell 0/1 with mouseclick 
        mouse_x, mouse_y = pygame.mouse.get_pos()
        col = mouse_x // cell_size
        row = mouse_y // cell_size
        if 0 <= row < grid_size[0] and 0 <= col < grid_size[1]:
            ca.cells[row, col] = 1 - ca.cells[row, col]

#Different cases when they are chosen in the menu 
def initialize_case(case_number):
    grid_width = 100

    if case_number == 0: 
        state = np.zeros(grid_width, dtype=int)
        state[grid_width // 2] = 1
    elif case_number == 1:          # Standard pyramid schape with middle cell = 1
        state = np.zeros(grid_width, dtype=int)
        state[grid_width // 2] = 1
    elif case_number == 2:
        state = np.zeros(grid_width, dtype=int)
        for i in range(0, grid_width, 20):
            state[i] = random.choice([0, 1])

    else:
        state = np.random.randint(0, 2, size=grid_width)

    return one_dimensional(cells=grid_width, state=2, rule_func=rule30, initial_state=state)