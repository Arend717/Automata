import math

class grid:
    def __init__(self, cells, state):
        self.cells = cells
        self.states = list(range(0, state))
        self.num_states = state

class one_dimensional(grid):
    def __init__(self, cells, state):
        super().__init__(cells, state)
        self.grid = [0] * cells
        self.history = []
    
    def get_neighbors(self, index):
        left = self.grid[(index - 1) % self.cells]
        center = self.grid[index]
        right = self.grid[(index + 1) % self.cells]
        return left, center, right
    
    def evolve(self):
        self.history.append(self.grid.copy())
        new_grid = [0] * self.cells
        
        for i in range(self.cells):
            left, center, right = self.get_neighbors(i)
            neighbor_sum = left + center + right
            new_grid[i] = neighbor_sum % self.num_states
        
        self.grid = new_grid


class hexagonal_grid(grid):
    def __init__(self, radius, state=2):
        cells = 1 + 3 * radius * (radius + 1)
        super().__init__(cells, state)
        self.radius = radius
        self.positions = []
        self.grid = [0] * cells
        self._create_hex_positions()
    
    def _create_hex_positions(self):
        self.positions.append((0, 0))
        
        for ring in range(1, self.radius + 1):
            for side in range(6):
                for step in range(ring):
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
                    
                    if len(self.positions) < self.cells:
                        self.positions.append((x, y))
    
    def get_neighbors(self, index):
        if index >= len(self.positions):
            return []
        
        x, y = self.positions[index]
        neighbor_offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
        neighbor_indices = []
        
        for dx, dy in neighbor_offsets:
            neighbor_pos = (x + dx, y + dy)
            try:
                neighbor_index = self.positions.index(neighbor_pos)
                neighbor_indices.append(neighbor_index)
            except ValueError:
                continue
        
        return neighbor_indices
    
    def evolve(self):
        new_grid = [0] * self.cells
        
        for i in range(self.cells):
            neighbors = self.get_neighbors(i)
            alive_neighbors = sum(1 for n in neighbors if self.grid[n] == 1)
            is_alive = self.grid[i] == 1
            
            if is_alive:
                new_grid[i] = 1 if alive_neighbors in [2, 3] else 0
            else:
                new_grid[i] = 1 if alive_neighbors == 3 else 0
        
        self.grid = new_grid

class one_dimensional_4states(grid):
    """1D cellular automaton with 4 states (0-3)"""
    def __init__(self, cells):
        super().__init__(cells, state=4)  # Fixed 4 states
        self.grid = [0] * cells
        self.history = []
    
    def get_neighbors(self, index):
        """Get left and right neighbors"""
        left = self.grid[(index - 1) % self.cells]
        center = self.grid[index]
        right = self.grid[(index + 1) % self.cells]
        return left, center, right
    
    def evolve(self):
        """Evolution rule: sum of neighbors modulo 4"""
        self.history.append(self.grid.copy())
        new_grid = [0] * self.cells
        
        for i in range(self.cells):
            left, center, right = self.get_neighbors(i)
            neighbor_sum = left + center + right
            new_grid[i] = neighbor_sum % 4  # mod 4 for 4 states
        
        self.grid = new_grid
