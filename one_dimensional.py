class grid:
    def __init__(self, cells, state):
        self.cells = cells  # number of cells 
        self.states = list(range(0, state))
        self.num_states = state


class one_dimensional(grid):
    def __init__(self, cells, state, rule_func):
        super().__init__(cells, state)
        self.grid = [0] * cells  # current state of cells 
        self.history = []        # last generation 
        self.rule_func = rule_func  
    
    def get_neighbors(self, index):
        # neighbors: left, center, right with wrap-around (ring)
        left = self.grid[(index - 1) % self.cells]
        center = self.grid[index]
        right = self.grid[(index + 1) % self.cells]
        return (left, center, right)
    
    def evolve(self):
        # add current generation to history 
        self.history.append(self.grid.copy())
        
        new_grid = [0] * self.cells
        
        for i in range(self.cells):
            neighbors = self.get_neighbors(i)
            new_grid[i] = self.rule_func(i, self.grid[i], neighbors)
        
        self.grid = new_grid
