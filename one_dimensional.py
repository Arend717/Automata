# File: one_dimensional.py

from grid import Grid

'''
The OneDimensional grid is derived from the general grid which means 
that all functions in the general grid can also be used by the OneDimensional grid
Altough to differentiate between derived grids, all derived grids shall have their own
interpretation of functions where needed.
In this case the init method which will always run when a new instance of this class is created
Has a function neighbors_1d inside in which all the neighbors coordinates based on the coordinates of a cell
are returned. 
'''
class OneDimensional(Grid):
    def __init__(self, shape, rule_func, n_states = 2, boundary='wrapped'):
        def neighbors_1d(cell_position):
            return [cell_position[0] - 1, cell_position[0] + 1]
        
        # This refers to the parent class Grid, and is needed to intialize shared logic from Grid
        super().__init__(shape, n_states, neighbors_1d, boundary)
        self._rule_func = rule_func

    '''
    The rule function is declared here but there is no implementation yet,
    this is because a rule will change based on a specific rule set
    '''
    def rule(self, cell_position, state, neighbor_states):
        return self._rule_func(cell_position, state, neighbor_states)
