import math

class grid:
    def __init__(self, cells, state):
        self.cells = cells
        self.states = [range(0, state - 1)]


class one_dimensional(grid):
    def __init__(self, cells, state):
        super().__init__(self, cells, state)
        

        
class two_dimensional(grid):
    def __init__(self, cells, state):
        super().__init__(cells, state)
        rows = cols = int(math.sqrt(cells))
        self.grid = [[0] * cols for _ in range(rows)]

class cell():
    def __init__(self, state = 0, coordinates):
        self.state = state
    
    def is_alive(self) -> bool:
        return self.state == 1 
    
    def set_alive(self):
        self.state = 1
    
    def set_dead(self):
        self.state = 0
    
    def toggle(self):
        self.state = 1 - self.state

        

Automata = two_dimensional(15, 2)