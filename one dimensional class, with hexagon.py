import math

class grid:
    """Base class for cellular automata grids"""
    def __init__(self, cells, state):
        """Initialize grid with given number of cells and states"""
        self.cells = cells          # Total number of cells in the grid
        self.states = list(range(0, state))  # List of possible states (0 to state-1)
        self.num_states = state      # Number of possible states per cell


class one_dimensional(grid):
    """1-dimensional cellular automaton with circular boundary conditions"""
    def __init__(self, cells, state):
        """Initialize 1D grid with specified size and number of states"""
        super().__init__(cells, state)
        self.grid = [0] * cells      # Initialize all cells to 0
        self.history = []            # Stores previous states of the grid
    
    def get_neighbors(self, index):
        """Get the left, center, and right neighbors of a cell using modular arithmetic
        to handle circular boundary conditions"""
        left = self.grid[(index - 1) % self.cells]   # Left neighbor (wraps around)
        center = self.grid[index]                     # Current cell
        right = self.grid[(index + 1) % self.cells]   # Right neighbor (wraps around)
        return left, center, right
    
    def evolve(self):
        """Update the grid state according to the rule:
        New cell state = sum of neighbor values modulo number of states"""
        self.history.append(self.grid.copy())  # Save current state to history
        new_grid = [0] * self.cells            # Initialize new grid
        
        for i in range(self.cells):
            left, center, right = self.get_neighbors(i)
            neighbor_sum = left + center + right
            new_grid[i] = neighbor_sum % self.num_states  # Apply rule
        
        self.grid = new_grid  # Replace old grid with new state


class hexagonal_grid(grid):
    """Hexagonal grid cellular automaton (2D) with Conway's Game of Life-like rules"""
    def __init__(self, radius, state=2):
        """Initialize hexagonal grid with given radius and states (default 2 states)"""
        # Calculate total cells in hex grid: 1 + 3*r*(r+1)
        cells = 1 + 3 * radius * (radius + 1)
        super().__init__(cells, state)
        self.radius = radius          # Radius of the hex grid
        self.positions = []           # Stores (x,y) coordinates of each cell
        self.grid = [0] * cells       # Initialize all cells to 0
        self._create_hex_positions()   # Generate hexagonal coordinate system
    
    def _create_hex_positions(self):
        """Generate axial coordinates for all cells in the hexagonal grid"""
        # Center cell at (0,0)
        self.positions.append((0, 0))
        
        # Generate rings outward from center
        for ring in range(1, self.radius + 1):
            # Hex grid has 6 sides
            for side in range(6):
                # Generate cells along each side
                for step in range(ring):
                    # Calculate coordinates based on which side we're on
                    if side == 0:
                        x, y = ring - step, step
                    elif side == 1:
                        x, y = -step, ring
                    elif side == 2:
                        x, y = -ring, ring - step
                    elif side == 3:
                        x, y = -ring + step, -step
                    elif side == 4:
                        x, y = step, -ring
                    else:
                        x, y = ring, -ring + step
                    
                    # Add position if we haven't reached total cell count
                    if len(self.positions) < self.cells:
                        self.positions.append((x, y))
    
    def get_neighbors(self, index):
        """Get indices of all 6 neighboring cells for a given cell index"""
        if index >= len(self.positions):
            return []  # Invalid index returns empty list
        
        x, y = self.positions[index]
        # Hex grid neighbors in axial coordinates
        neighbor_offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
        neighbor_indices = []
        
        # Check each possible neighbor position
        for dx, dy in neighbor_offsets:
            neighbor_pos = (x + dx, y + dy)
            try:
                # Find index of neighbor if it exists in our grid
                neighbor_index = self.positions.index(neighbor_pos)
                neighbor_indices.append(neighbor_index)
            except ValueError:
                continue  # Skip if neighbor position doesn't exist
        
        return neighbor_indices
    
    def evolve(self):
        """Update grid state using Conway's Game of Life rules adapted for hex grid:
        - Live cell (1) survives with 2-3 live neighbors
        - Dead cell (0) becomes alive with exactly 3 live neighbors"""
        new_grid = [0] * self.cells  # Initialize new grid
        
        for i in range(self.cells):
            neighbors = self.get_neighbors(i)
            alive_neighbors = sum(1 for n in neighbors if self.grid[n] == 1)
            is_alive = self.grid[i] == 1
            
            # Apply Game of Life rules
            if is_alive:
                new_grid[i] = 1 if alive_neighbors in [2, 3] else 0
            else:
                new_grid[i] = 1 if alive_neighbors == 3 else 0
        
        self.grid = new_grid  # Replace old grid with new state

