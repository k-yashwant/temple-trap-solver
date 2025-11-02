from priority_queue import frontier, node_positions, HeapPush, ExtractMin, ChangeKey
from generate_actions import initTiles, ActionSpace
from state_node import Node
from solution import GoalTest


def search(initial_state):
    initial_state = initial_state.strip().split()


    # set the tiles positions and their rotations
    sum_positions = 0

    start_node = Node()
    for i in range(8):
        start_node.state[int(initial_state[i][0])] = initial_state[i][1]
        sum_positions += int(initial_state[i][0])
        initTiles(initial_state[i])
    start_node.empty=36-sum_positions
    start_node.state[start_node.empty] = 'empty'


    #set player position
    start_node.state[-2] = int(initial_state[-1])

    start_node.update_id()

    explored = set()
    HeapPush(start_node)




    while True:
        if len(frontier) == 0:
            # return None, None
            exit("Failed to reach goal")
        
        node = ExtractMin()

        actions, path_cost = GoalTest(node)
        if actions is not None:
            return actions, path_cost
            # exit()
            pass
            # return actions, path_cost

        explored.add(node.id)

        child_nodes = ActionSpace(node)
        
        for child in child_nodes:
            check_explored = child.id in explored
            check_frontier = child.id in node_positions
            if not check_explored and not check_frontier:
                HeapPush(child)
            elif check_frontier:
                ChangeKey(child.id, child.path_cost) # change to lower path cost or do nothing

# search(initial_state="0C0 1D0 2G2 3B1 5H3 6A0 7E0 8F2 8")









