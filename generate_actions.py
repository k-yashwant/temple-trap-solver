from copy import deepcopy
from tiles import tiles_map
import numpy as np

def initTiles(init_code, tiles_map=tiles_map):
    tiles_map[init_code[1]] = tiles_map[init_code[1]](int(init_code[2]))


# to generate a list of child nodes from a given node.

'''
possible actions
    moving tiles:
        - empty space can be moved left, right, up and down
        - empty space cannot exchange places with a tile having same position as the player

    moving player:
        - moving player withing ground level
        - if player is in a 'stair' tile, then its level can be interchanged between top and ground
        - if the player is in top level, the next possible actions cannot include movement of empty space,
            movement of player is only allowed
'''

left_dir = np.array((-1,0))
right_dir = np.array((1,0))
up_dir = np.array((0,1))
down_dir = np.array((0,-1))

def moveEmptyLeft(node, pos):
    new_node=deepcopy(node)

    if pos not in {0, 3, 6} and node.player_position() != pos-1:
        temp=new_node.state[pos-1]
        new_node.state[pos-1] = new_node.state[pos]
        new_node.state[pos] = temp

        new_node.update_id()
        new_node.empty=pos-1
        new_node.parent = node
        new_node.prev_action = (new_node.state[pos], 'Right')
        new_node.path_cost = node.path_cost + 1

        return new_node
    else:
        return None
    
def moveEmptyRight(node, pos):
    new_node=deepcopy(node)

    if pos not in {2, 5, 8} and node.player_position() != pos+1:
        temp=new_node.state[pos+1]
        new_node.state[pos+1] = new_node.state[pos]
        new_node.state[pos] = temp

        new_node.update_id()
        new_node.empty=pos+1
        new_node.parent = node
        new_node.prev_action = (new_node.state[pos], 'Left')
        new_node.path_cost = node.path_cost + 1

        return new_node
    else:
        return None

def moveEmptyUp(node, pos):
    new_node=deepcopy(node)
  
    if pos not in {0, 1, 2} and node.player_position() != pos-3:
        temp=new_node.state[pos-3]
        new_node.state[pos-3] = new_node.state[pos]
        new_node.state[pos] = temp

        new_node.update_id()
        new_node.empty=pos-3
        new_node.parent = node
        new_node.prev_action = (new_node.state[pos], 'Down')
        new_node.path_cost = node.path_cost + 1

        return new_node
    else:
        return None   

def moveEmptyDown(node, pos):
    new_node=deepcopy(node)
  
    if pos not in {6, 7, 8} and node.player_position() != pos+3:
        temp=new_node.state[pos+3]
        new_node.state[pos+3] = new_node.state[pos]
        new_node.state[pos] = temp

        new_node.update_id()
        new_node.empty=pos+3
        new_node.parent = node
        new_node.prev_action = (new_node.state[pos], 'Up')
        new_node.path_cost = node.path_cost + 1
        
        return new_node
    else:
        return None           

def movePlayerLeft(node, level, dir=left_dir):
    if node.player_position() not in {0, 3, 6}:
        current_tile = tiles_map[node.state[node.player_position()]]
        next_tile = tiles_map[node.state[node.player_position() - 1]]

        if level == 'ground':
            if any(np.array_equal(dir, x) for x in current_tile.ground):
                for dir2 in next_tile.ground:
                    if all(dir + dir2 == np.array((0,0))):
                        new_node = deepcopy(node)
                        new_node.state[-2] = node.player_position() - 1
                        new_node.update_id()
                        new_node.parent = node
                        new_node.prev_action = ('Player', 'Left')
                        new_node.path_cost = node.path_cost + 1
                        return new_node
            return None
        elif level == 'top':
            if any(np.array_equal(dir, x) for x in current_tile.top):
                for dir2 in next_tile.top:
                    if all(dir + dir2 == np.array((0,0))):
                        new_node = deepcopy(node)
                        new_node.state[-2] = node.player_position() - 1
                        new_node.update_id()
                        new_node.parent = node
                        new_node.prev_action = ('Player', 'Left')
                        new_node.path_cost = node.path_cost + 1
                        return new_node
            return None
    else:
        return None

def movePlayerRight(node, level, dir=right_dir):
    if node.player_position() not in {2, 5, 8}:
        current_tile = tiles_map[node.state[node.player_position()]]
        next_tile = tiles_map[node.state[node.player_position() + 1]]

        if level == 'ground':
            if any(np.array_equal(dir, x) for x in current_tile.ground):
                for dir2 in next_tile.ground:
                    if all(dir + dir2 == np.array((0,0))):
                        new_node = deepcopy(node)
                        new_node.state[-2] = node.player_position() + 1
                        new_node.update_id()
                        new_node.parent = node
                        new_node.prev_action = ('Player', 'Right')
                        new_node.path_cost = node.path_cost + 1
                        return new_node
            return None
        elif level == 'top':
            if any(np.array_equal(dir, x) for x in current_tile.top):
                for dir2 in next_tile.top:
                    if all(dir + dir2 == np.array((0,0))):
                        new_node = deepcopy(node)
                        new_node.state[-2] = node.player_position() + 1
                        new_node.update_id()
                        new_node.parent = node
                        new_node.prev_action = ('Player', 'Right')
                        new_node.path_cost = node.path_cost + 1
                        return new_node
            return None
    else:
        return None

def movePlayerUp(node, level, dir=up_dir):
    if node.player_position() not in {0, 1, 2}:
        current_tile = tiles_map[node.state[node.player_position()]]
        next_tile = tiles_map[node.state[node.player_position() - 3]]

        if level == 'ground':
            if any(np.array_equal(dir, x) for x in current_tile.ground):
                for dir2 in next_tile.ground:
                    if all(dir + dir2 == np.array((0,0))):
                        new_node = deepcopy(node)
                        new_node.state[-2] = node.player_position() - 3
                        new_node.update_id()
                        new_node.parent = node
                        new_node.prev_action = ('Player', 'Up')
                        new_node.path_cost = node.path_cost + 1
                        return new_node
            return None
        elif level == 'top':
            if any(np.array_equal(dir, x) for x in current_tile.top):
                for dir2 in next_tile.top:
                    if all(dir + dir2 == np.array((0,0))):
                        new_node = deepcopy(node)
                        new_node.state[-2] = node.player_position() - 3
                        new_node.update_id()
                        new_node.parent = node
                        new_node.prev_action = ('Player', 'Up')
                        new_node.path_cost = node.path_cost + 1
                        return new_node
            return None
    else:
        return None

def movePlayerDown(node, level, dir=down_dir):
    if node.player_position() not in {6, 7, 8}:
        current_tile = tiles_map[node.state[node.player_position()]]
        next_tile = tiles_map[node.state[node.player_position() + 3]]

        if level == 'ground':
            if any(np.array_equal(dir, x) for x in current_tile.ground):
                for dir2 in next_tile.ground:
                    if all(dir + dir2 == np.array((0,0))):
                        new_node = deepcopy(node)
                        new_node.state[-2] = node.player_position() + 3
                        new_node.update_id()
                        new_node.parent = node
                        new_node.prev_action = ('Player', 'Down')
                        new_node.path_cost = node.path_cost + 1
                        return new_node
            return None
        elif level == 'top':
            if any(np.array_equal(dir, x) for x in current_tile.top):
                for dir2 in next_tile.top:
                    if all(dir + dir2 == np.array((0,0))):
                        new_node = deepcopy(node)
                        new_node.state[-2] = node.player_position() + 3
                        new_node.update_id()
                        new_node.parent = node
                        new_node.prev_action = ('Player', 'Down')
                        new_node.path_cost = node.path_cost + 1
                        return new_node
            return None
    else:
        return None

def changePlayerLevel(node):
    if tiles_map[node.state[node.player_position()]].piece == 'stair':
        new_node = deepcopy(node)
        new_node.state[-1] = (new_node.state[-1] + 1) % 2
        new_node.parent = node
        new_node.prev_action = 'level_change'
        new_node.update_id()
        new_node.path_cost = node.path_cost
        return new_node
    else:
        return None

def ActionSpace(node):
    child_nodes = []

    # when player is on ground level
    if node.player_level() == 0:
        #generate nodes by moving empty block
        move_empty = [moveEmptyLeft, moveEmptyRight, moveEmptyUp, moveEmptyDown]

        for function in move_empty:
            child_node = function(node, node.empty)
            if child_node != None:
                child_nodes.append(child_node)
        
        #move the player within ground level
        move_player = [movePlayerLeft, movePlayerRight, movePlayerUp, movePlayerDown]

        for function in move_player:
            child_node = function(node, 'ground')
            if child_node != None:
                child_nodes.append(child_node)

    #when player is on top level
    elif node.player_level() == 1:
        move_player = [movePlayerLeft, movePlayerRight, movePlayerUp, movePlayerDown]

        for function in move_player:
            child_node = function(node, 'top')
            if child_node != None:
                child_nodes.append(child_node)
                
    #if player is on a stair, its level can be changed from ground to top
    change_level = changePlayerLevel(node)
    if change_level != None:
        change_level.player_level
        child_nodes.append(change_level)
    
    return child_nodes


            
        
    
    