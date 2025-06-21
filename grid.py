import numpy as np
from abc import ABC, abstractmethod

'''
The Grid ABC class is a generic class which can only be used by derived classes
There can not be a instance created directly from this class since it is an ABC class
The generic grid class can be used for:
Any dimensional grid
Any number of states
Any amount of neighbors
Boundary wrapped or fixed
'''
class Grid(ABC):
    def __init__(self, size, n_states, neighbors, boundary='wrapped'):
        self.n_states = n_states
        self.neighbors = neighbors
        self.boundary = boundary
        
        # Fill cells of 1d if size is int otherwise create 2 or more dimensional grid
        # Grid is filled with zeros of type int
        if isinstance(size, int):
            self.shape = (size,)
            self.cells = np.zeros(size, dtype=int)
        else:
            self.shape = size
            self.cells = np.zeros(size, dtype=int)

    '''
    Count neighbors function with as input the coordinates of a cell
    Uses the neighbors function which can be declared by every subclass of this class
    if statement chooses between wrapped and fixed grid edges and returns wrapped or dead neighbors
    '''
    def _count_neighbors(self, cell_coord):
        # Retrieve neighbors of the cell
        neighbors = self.neighbors(cell_coord)

        # Wrap neighbors arround grid edges
        if self.boundary == 'wrapped':
            wrapped_neighbors = []
            for neighbor_pos in neighbors:
                if isinstance(neighbor_pos, tuple):
                     wrapped = tuple((coord % dim_size) for coord, dim_size in zip(neighbor_pos, self.shape))
                else:
                    wrapped = neighbor_pos % self.shape[0]
                wrapped_neighbors.append(wrapped)
            return wrapped_neighbors
        
        # Dead neighbors arround grid edges
        elif self.boundary == 'fixed':
            dead_neighbors = []
            for neighbor_pos in neighbors:
                if isinstance(neighbor_pos, tuple):
                     if all(0 <= coord < dim_size for coord, dim_size in zip(neighbor_pos, self.shape)):
                         dead_neighbors.append(neighbor_pos)
                else:
                    if 0 <= neighbor_pos < self.shape[0]:
                        dead_neighbors.append(neighbor_pos)
            return dead_neighbors
        else:
            raise ValueError("Unkown boundary condition: ", self.boundary)

    '''
    The Abstractmethod needs to be in every subclass of this class
    The function rule has to be in every subclass and will be defined there
    '''
    @abstractmethod
    def rule(self, cell, state, neighbor_states):
        pass

    '''
    In the evolve function the original grid is copied to new_cells and filled with zeros
    And then for all cells in the original grid a nditer type all_cells is created
    This nditer type can be used to iterate over every cell(coordinates)
    With the count neighbors function and rule function for every cell the new state can be calculated
    Every cell state will be saved in the new_cells grid, 
    and afterwards this new_cells grid will be saved to self.cells
    '''
    def evolve(self):
        new_cells = np.zeros_like(self.cells)
        all_cells = np.nditer(self.cells, flags = ['multi_index'])
        for cell in all_cells:
            cell_position = all_cells.multi_index
            current_state = self.cells[cell_position]
            neighbors = self._count_neighbors(cell_position)
            neighbor_states = [self.cells[neighbor_pos] for neighbor_pos in neighbors]
            new_cells[cell_position] = self.rule(cell_position, current_state, neighbor_states)
        self.cells = new_cells