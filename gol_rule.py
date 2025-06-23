# File: gol_rule.py
# Contains Game of Life rule function (logic only)

def gol_rule(cell_position, state, neighbor_states):
    """
    Conway's Game of Life logic.
    :param cell_position: (row, col) - Not used here
    :param state: current cell state (0 or 1)
    :param neighbor_states: list of states of all neighboring cells
    :return: new state (0 or 1)
    """
    alive_neighbors = sum(neighbor_states)

    if state == 1:
        return 1 if 2 <= alive_neighbors <= 3 else 0
    else:
        return 1 if alive_neighbors == 3 else 0
