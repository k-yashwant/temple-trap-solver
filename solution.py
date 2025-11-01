#Print the solution
from generate_actions import left_dir
from tiles import tiles_map
import numpy as np

actions = [('Player', 'Left')]

def PrintSolution(node, actions=actions):
    path_cost = node.path_cost + 1
    while True:
        actions.append(node.prev_action)
        if node.parent == None:
            break
        node=node.parent
    
    for i in range(len(actions)-2, -1, -1):
        pass
        print(actions[i], end=" " )
    
    print()
    print("Path_cost:", path_cost)
    exit()

def GoalTest(node):
    if node.player_level() == 1 and node.player_position() == 0 and any(np.array_equal(left_dir, x) for x in tiles_map[node.state[node.player_position()]].top):
        PrintSolution(node)
    else:
        return None