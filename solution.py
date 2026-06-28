#Print the solution
from generate_actions import LEFT
import numpy as np

def TrackSolution(node):
    states = []
    path_cost = node.path_cost + 1
    while True:
        prev_action = node.prev_action
        states.append(tuple(node.state[:-1]))
        if node.prev_action == 'level_change':
            node = node.parent
        if node.parent == None:
            break
        node=node.parent
    
    states.reverse()
    
    final_state = list(states[-1])
    final_state[-1] = -1
    final_state = tuple(final_state)
    states.append(final_state)
    
    return states, path_cost

def GoalTest(node, tiles_map):
    if node.player_level() == 1 and node.player_position() == 0 and any(np.array_equal(LEFT, x) for x in tiles_map[node.state[node.player_position()]].top):
        return TrackSolution(node)
    else:
        return None,  None