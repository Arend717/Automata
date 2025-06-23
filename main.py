from two_dimensional import TwoDimensional
from gol_rule import gol_rule

import math

#-> these lines were in conflict with Grid system and not used. Did not want to remove them so # 
#class grid:
 #   def __init__(self, cells, state):
  #      self.cells = cells
   #     self.states = [range(0, state - 1)]


#class one_dimensional(grid):
 #   def __init__(self, cells, state):
  #      super().__init__(self, cells, state)
        
'''
This dummy rule is only here as an example to show what kind of rules can be implemented
In essence the rule has the following inputs:
Cell_position, state, neighbor_states
And the output should be a integer for the state of the cell
'''
def dummy_rule(cell_position, state, neighbor_states):
    return (state + 1) % 2  # toggles between 0 and 1
                            # Does not use the cell_position or neighbor_states in the calculation


# A Twodimensional cellular automata is created with a grid of 5 by 5.
# This is an instance of the two_dimensional class
# The gol rule is given as input
# The cellular automata has 2 states
# The cellular automata has fixed boundaries
ca = TwoDimensional((5,5), gol_rule, 2, boundary='fixed')
# A cell in the grid with coordinates 2,2 is put at 1
ca.cells[2, 2] = 1
# Initial state is being printed
print("Initial state: ", ca.cells)
# Evolve function is called on the cellular automata
ca.evolve()
# End state is being printed
print("\nAfter one evolution step:", ca.cells)