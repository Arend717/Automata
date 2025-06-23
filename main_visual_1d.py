import pygame
from one_dimensional import one_dimensional
from rule30_rule import rule30

# Pygame setup
pygame.init()

CELL_SIZE = 6
WIDTH = 100  # number of cells in the 1D automaton

# Window height set to show 100 generations
HEIGHT = CELL_SIZE * 100

screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT))
pygame.display.set_caption("Rule 30 - 1D Cellular Automaton")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def draw_grid(screen, cells, y_offset):
    """
    Draw a row of cells at vertical pixel position y_offset.
    """
    for col, cell in enumerate(cells):
        color = WHITE if cell == 1 else BLACK
        pygame.draw.rect(screen, color, (col * CELL_SIZE, y_offset, CELL_SIZE, CELL_SIZE))

def main():
    ca = one_dimensional(WIDTH, 2, rule30)
    # Initialize with a single live cell in the center
    ca.grid[WIDTH // 2] = 1
    
    clock = pygame.time.Clock()
    running = True
    paused = False
    generation = 0
    max_generations = 100  # max number of generations to display

    # Clear screen and draw initial state
    screen.fill(BLACK)
    draw_grid(screen, ca.grid, generation * CELL_SIZE)
    pygame.display.flip()
    generation += 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Pause/unpause simulation with SPACE key
                if event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused and generation < max_generations:
            ca.evolve()
            draw_grid(screen, ca.grid, generation * CELL_SIZE)
            pygame.display.flip()
            generation += 1

        clock.tick(10)  # 10 FPS

    pygame.quit()

if __name__ == "__main__":
    main()