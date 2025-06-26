import pygame

# Global constants
FPS = 10  # Frames per second, controls evolution speed
CELL_SIZE = 5  # Pixel size of each cell
WINDOW_HEIGHT = 600  # Window height in pixels
GRID_WIDTH = 100  # Number of cells in the grid
COLORS = {
    0: (255, 255, 255),  # White: dead
    1: (0, 0, 0),        # Black: active
    2: (128, 128, 128)   # Gray: dormant
}

class 3states:
    def __init__(self):
        """Initialize three states from Rule 30 Cellular automaton rule table"""
        self.rule_table = self._rule30_three_state_table()
        self.grid = [2] * GRID_WIDTH  # Initialize grid with dormant state
        self.grid[GRID_WIDTH // 2] = 1  # Set center cell to active
        self.history = [self.grid.copy()]  # Store initial grid state

    def _rule30_three_state_table(self) -> dict[tuple[int, int, int], int]:
        """
        This is the three-state Rule 30 rule table I designed, with 27 items.
        Based on the combination of neighbor states, simulate the complexity of Rule 30.
        Index 0-26 corresponds to the enumeration from [0,0,0] to [2,2,2].

        Rule design ideas:
        Keep propagating
        Use the dormant state as the third state
        Create complex dynamic patterns
        """
        return {
            # First digit = left, second = center, third = right
            (0, 0, 0): 0, (0, 0, 1): 1, (0, 0, 2): 0,
            (0, 1, 0): 1, (0, 1, 1): 2, (0, 1, 2): 1,
            (0, 2, 0): 0, (0, 2, 1): 1, (0, 2, 2): 2,
            (1, 0, 0): 1, (1, 0, 1): 0, (1, 0, 2): 2,
            (1, 1, 0): 2, (1, 1, 1): 1, (1, 1, 2): 0,
            (1, 2, 0): 1, (1, 2, 1): 2, (1, 2, 2): 1,
            (2, 0, 0): 0, (2, 0, 1): 2, (2, 0, 2): 1,
            (2, 1, 0): 2, (2, 1, 1): 0, (2, 1, 2): 2,
            (2, 2, 0): 1, (2, 2, 1): 2, (2, 2, 2): 0
        }

    def rule(self, cell_position: int, state: int, neighbor_states: list[int]) -> int:
        """
        Apply three-state Rule 30 based on neighbor configuration.
        Uses dictionary lookup for (left, center, right) patterns.
        """
        if len(neighbor_states) != 3 or not all(s in {0, 1, 2} for s in neighbor_states):
            return state
        
        # Return matching rule
        return self.rule_table[tuple(neighbor_states)]

    def get_neighbors(self, index: int) -> list[int]:
        """Get left, center, and right neighbor states with periodic boundary."""
        left = self.grid[(index - 1) % GRID_WIDTH]
        center = self.grid[index]
        right = self.grid[(index + 1) % GRID_WIDTH]
        return [left, center, right]

    def evolve(self):
        """Compute the next generation of the grid using three-state Rule 30."""
        self.history.append(self.grid.copy())
        new_grid = [0] * GRID_WIDTH
        for i in range(GRID_WIDTH):
            neighbors = self.get_neighbors(i)
            new_grid[i] = self.rule(i, self.grid[i], neighbors)
        self.grid = new_grid
        if len(self.history) > WINDOW_HEIGHT // CELL_SIZE:
            self.history.pop(0)  # Remove oldest state to fit window

# Initialize Pygame and automaton
pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, WINDOW_HEIGHT))
pygame.display.set_caption("Three-State Rule 30")
ca = CellularAutomaton()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))  # Clear screen with white
    for t, row in enumerate(ca.history):
        for x, state in enumerate(row):
            pygame.draw.rect(screen, COLORS[state],
                            (x * CELL_SIZE, t * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    ca.evolve()
    pygame.display.flip()
    pygame.time.delay(1000 // FPS)  # Delay in milliseconds for ~10 FPS

pygame.quit()
