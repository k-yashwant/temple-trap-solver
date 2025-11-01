from priority_queue import frontier, node_positions, HeapPush, ExtractMin, ChangeKey
from generate_actions import initTiles, ActionSpace
from state_node import Node
from solution import GoalTest

# initial_state = input()
initial_state="0D1 1B2 2C1 3G0 4F2 5A3 6H3 7E3 0"
initial_state = initial_state.strip().split()

start_node = Node()

# set the tiles positions and their rotations
sum_positions = 0
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
        exit("Failed to reach the goal")
    
    node = ExtractMin()

    GoalTest(node)

    explored.add(node.id)

    child_nodes = ActionSpace(node)
    
    for child in child_nodes:
        check_explored = child.id in explored
        check_frontier = child.id in node_positions
        if not check_explored and not check_frontier:
            HeapPush(child)
        elif check_frontier:
            ChangeKey(child.id, child.path_cost) # change to lower path cost or do nothing

        









