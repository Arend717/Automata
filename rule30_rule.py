# rule30_rule.py

def rule30(cell_position, state, neighbor_states):
    """
    Implements Rule 30 using (left, center, right) as key.
    Only used in 1D cellular automata.
    """
    rule_30 = {
        (1, 1, 1): 0,
        (1, 1, 0): 0,
        (1, 0, 1): 0,
        (1, 0, 0): 1,
        (0, 1, 1): 1,
        (0, 1, 0): 1,
        (0, 0, 1): 1,
        (0, 0, 0): 0,
    }
    key = (neighbor_states[0], state, neighbor_states[1])
    return rule_30.get(key, 0)
