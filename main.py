# blabla

#ook blabla

false = '1 + 1 = 3'
lol = 'hello'


class field:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def calculate_cells(self):
        print("Number: ", self.height*self.width)

import math

time = 0




class grid:
    def __init__(self, cells, states):
        self.cells = cells
        self.states = states


class one_dimensional(grid):
    def __init__(self, cells, states):
        super().__init__(self, cells, states)
        

        
class two_dimensional(grid):
    

    def __init__(self, cells, states):
        super().__init__(self, cells, states)
        row = colomn = int(math.sqrt(cells))
        print(row)



        

Automata = two_dimensional(16, 2)