# File: two_dimensional.py

from grid import Grid
        
'''
The TwoDimensional grid is derived from the general grid which means 
that all functions in the general grid can also be used by the TwoDimensional grid
Altough to differentiate between derived grids, all derived grids shall have their own
interpretation of functions where needed.
In this case the init function which will always run when a new instance of this class is created
Has a function neighbors_2d inside in which all the neighbors coordinates based on the coordinates of a cell
are returned. 
In this function those neighbors are based on the Moore neighborhood with 8 neighbors
'''
class TwoDimensional(Grid):
    def __init__(self, shape, rule_func, boundary='wrapped'):
        def neighbors_2d(cell_position):
            y, x = cell_position
            return [(y + dy, x + dx)
                    for dy in (-1, 0, 1)
                    for dx in (-1, 0, 1)
                    if not (dy == 0  and dx ==0)]
        # This refers to the parent class Grid, and is needed to intialize shared logic from Grid
        super().__init__(shape, neighbors_2d, boundary)
        self._rule_func = rule_func
    
    '''
    The rule function is declared here but there is no implementation yet,
    this is because a rule will change based on a specific rule set
    '''
    def rule(self, cell_position, state, neighbor_states):
        return self._rule_func(cell_position, state, neighbor_states)
