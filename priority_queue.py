#Contains all functions required for the "frontier" priority queue suitable for working with state node


'''
class node:
    id
    path_cost
    priority            #in A* search
'''

frontier = []
node_positions = {}

def getPriority(x, frontier=frontier):
    node = frontier[x]
    if hasattr(node, 'priority'):
        return node.priority
    return node.path_cost

def parent(x):
    return (x-1)//2

def left(x):
    return 2*x+1

def right(x):
    return 2*x+2

def MinHeapify(x, frontier=frontier, node_positions=node_positions):
    """Sift Down Operation"""
    if len(frontier) > 0:
        lowest = x

        if (left(x) < len(frontier) and getPriority(left(x), frontier) < getPriority((lowest), frontier)):
            lowest=left(x)
            
        if right(x) < len(frontier) and getPriority(right(x), frontier) < getPriority(lowest, frontier):
            lowest=right(x)
        
        if lowest != x:
            frontier[x], frontier[lowest] = frontier[lowest], frontier[x]
            node_positions[frontier[x].id] = x

            node_positions[frontier[lowest].id] = lowest

            MinHeapify(lowest, frontier, node_positions)

def MinheapifyParent(x, frontier, node_positions):
    """Sift-Up operation"""
    while x > 0:
        p = parent(x)
        if getPriority(p, frontier) > getPriority(x, frontier):

            frontier[x], frontier[p] = frontier[p], frontier[x]
            
            node_positions[frontier[x].id] = x
            node_positions[frontier[p].id] = p
            
            # Move up the tree
            x = p
        else:
            break # Heap property is satisfied


def HeapPush(node, frontier=frontier, node_positions=node_positions):
    frontier.append(node)
    node_positions[node.id] = len(frontier)-1
    MinheapifyParent(len(frontier)-1, frontier, node_positions)
    return

def ExtractMin(frontier=frontier, node_positions=node_positions):
    if len(frontier)==0:
        return None
    
    min = frontier[0]

    frontier[0] = frontier[-1]
    node_positions[frontier[0].id] = 0

    del frontier[-1]
    del node_positions[min.id]

    MinHeapify(0, frontier, node_positions)

    pass
    return min


def ChangeKey(id, path_cost, frontier=frontier, node_positions=node_positions):
    pos = node_positions[id]

    if frontier[pos].path_cost < path_cost:
        return None
    else:
        cost_diff = frontier[pos].path_cost - path_cost   
        frontier[pos].path_cost = path_cost
        if(hasattr(frontier[pos], 'priority')):
            frontier[pos].priority -= cost_diff
        
    #New path_cost should always be less than or equal

    MinheapifyParent(pos, frontier, node_positions)
    pass
