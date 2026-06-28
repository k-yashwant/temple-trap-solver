from priority_queue import frontier, node_positions, HeapPush, ExtractMin, ChangeKey
from generate_actions import initTiles, ActionSpace
from tiles import tiles_map_template
from state_node import Node
from solution import GoalTest


search_stats = {
    'nodes_expanded': 0,
    'max_frontier_size': 0
}

def manhattan_distance(node):
    p = node.player_position()
    r = p // 3
    c = p % 3
    return r + c

def search(initial_state, algorithm='ucs', max_nodes = None):
    frontier.clear()
    node_positions.clear()
    search_stats['nodes_expanded'] = 0
    search_stats['max_frontier_size'] = 0

    initial_state = initial_state.strip().split()

    # set the tiles positions and their rotations
    sum_positions = 0

    tiles_map = {}
    tiles_map.update(tiles_map_template)
    start_node = Node()
    for i in range(8):
        start_node.state[int(initial_state[i][0])] = initial_state[i][1]
        sum_positions += int(initial_state[i][0])
        initTiles(initial_state[i], tiles_map=tiles_map)
    start_node.empty=36-sum_positions
    start_node.state[start_node.empty] = 'empty'

    #set player position
    start_node.state[-2] = int(initial_state[-1])

    start_node.update_id()

    if algorithm == 'astar':
        start_node.priority = start_node.path_cost + manhattan_distance(start_node)
    else:
        start_node.priority = start_node.path_cost

    explored = set()
    HeapPush(start_node)
    search_stats['max_frontier_size'] = max(search_stats['max_frontier_size'], len(frontier))

    while True:
        if len(frontier) == 0:
            return None, None
        
        node = ExtractMin()
        search_stats['nodes_expanded'] += 1


        actions, path_cost = GoalTest(node, tiles_map)
        if actions is not None:
            return actions, path_cost

        explored.add(node.id)

        child_nodes = ActionSpace(node, tiles_map)
        
        for child in child_nodes:
            check_explored = child.id in explored
            check_frontier = child.id in node_positions
            if not check_explored and not check_frontier:
                if algorithm == 'astar':
                    child.priority = child.path_cost + manhattan_distance(child)
                else:
                    child.priority = child.path_cost
                HeapPush(child)
                search_stats['max_frontier_size'] = max(search_stats['max_frontier_size'], len(frontier))
            elif check_frontier:
                ChangeKey(child.id, child.path_cost)

# search(initial_state="0C0 1D0 2G2 3B1 5H3 6A0 7E0 8F2 8")









