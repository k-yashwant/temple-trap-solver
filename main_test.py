from priority_queue import frontier, node_positions, HeapPush, ExtractMin, ChangeKey
from generate_actions import initTiles, ActionSpace
from state_node import Node
from solution import GoalTest
import time

heappush_time = 0
actionspace_time = 0
ExtractMin_time = 0
ChangeKey_time = 0
check_explored_frontier_time = 0

# initial_state = input()
initial_state="0B2 1C0 3F1 4E0 5A0 6G1 7H0 8D3 4"
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
    
    s=time.time()
    node = ExtractMin()
    t=time.time()
    ExtractMin_time+=(t-s)

    GoalTest(node)

    explored.add(node.id)

    s=time.time()
    child_nodes = ActionSpace(node)
    t=time.time()
    actionspace_time+=(t-s)

    for child in child_nodes:
        s=time.time()
        check_explored = child.id in explored
        check_frontier = child.id in node_positions
        t=time.time()
        check_explored_frontier_time+=(t-s)
        if not check_explored and not check_frontier:
            s=time.time()
            HeapPush(child)
            t=time.time()
            heappush_time+=(t-s)
        elif check_frontier:
            s=time.time()
            ChangeKey(child.id, child.path_cost) # change to lower path cost or do nothing
            t=time.time()
            ChangeKey_time+=(t-s)
        

pass







