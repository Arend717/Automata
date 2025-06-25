import pygame
import sys
from one_dimensional import one_dimensional
from rule30_rule import rule30
import random

# Set size of each cell and screen size
CELL_SIZE = 5
WIDTH = 101
HEIGHT = 600

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Draw one row of cells on the screen at a vertical position y_offset
def draw_row(screen, row, y_offset):
    for i, cell in enumerate(row):
        color = WHITE if cell == 1 else BLACK
        pygame.draw.rect(screen, color, (i * CELL_SIZE, y_offset, CELL_SIZE, CELL_SIZE))

# Ask the user to press 1, 2 or 3 to choose a starting configuration
def wait_for_choice():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT))
    pygame.display.set_caption("Rule 30 - Choose Start")
    font = pygame.font.SysFont(None, 28)

    # Show message
    screen.fill(BLACK)
    msg = font.render("Press 1 (standard), 2 (random) or 3 (symmetrical) to choose a starting pattern", True, WHITE)
    screen.blit(msg, (20, HEIGHT // 2))
    pygame.display.flip()

    # Wait for key press
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode in ['1', '2', '3']:
                    return event.unicode

# Set initial state based on chosen pattern
def set_start_state(ca, choice):
    if choice == '1':
        ca.grid[WIDTH // 2] = 1  # Single live cell in the center
    elif choice == '2':
        ca.grid = [random.randint(0, 1) for _ in range(WIDTH)]  # Random
    elif choice == '3':
        center = WIDTH // 2
        ca.grid[center - 1:center + 2] = [1, 1, 1]  # Three live cells in the center

def main():
    ca = one_dimensional(WIDTH, 2, rule30)
    set_start_state(ca, choice)

    generation = 0
    max_generations = HEIGHT // CELL_SIZE
    screen.fill(BLACK)

    running = True
    while running and generation < max_generations:
        draw_row(screen, ca.grid, generation * CELL_SIZE)
        pygame.display.flip()
        ca.step()
        generation += 1
        clock.tick(10)  # Slow down to 10 generations per second

        # Check for quit or enter key
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()