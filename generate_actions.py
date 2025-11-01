from tiles import tiles_map
import numpy as np
from state_node import Node

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

LEFT = np.array((-1,0))
RIGHT = np.array((1,0))
UP = np.array((0,1))
DOWN = np.array((0,-1))

def moveEmpty(node, pos, child_nodes):
    player_position = node.player_position()
    new_node=Node()
    new_node.state = list(node.state)

    if pos not in {0, 3, 6} and player_position != pos-1:
        temp=new_node.state[pos-1]
        new_node.state[pos-1] = new_node.state[pos]
        new_node.state[pos] = temp

        new_node.update_id()
        new_node.empty=pos-1
        new_node.parent = node
        new_node.prev_action = (new_node.state[pos], 'Right')
        new_node.path_cost = node.path_cost + 1
        child_nodes.append(new_node)
    
    new_node=Node()
    new_node.state = list(node.state)

    if pos not in {2, 5, 8} and player_position != pos+1:
        temp=new_node.state[pos+1]
        new_node.state[pos+1] = new_node.state[pos]
        new_node.state[pos] = temp

        new_node.update_id()
        new_node.empty=pos+1
        new_node.parent = node
        new_node.prev_action = (new_node.state[pos], 'Left')
        new_node.path_cost = node.path_cost + 1
        child_nodes.append(new_node)

    new_node=Node()
    new_node.state = list(node.state)
  
    if pos not in {0, 1, 2} and player_position != pos-3:
        temp=new_node.state[pos-3]
        new_node.state[pos-3] = new_node.state[pos]
        new_node.state[pos] = temp

        new_node.update_id()
        new_node.empty=pos-3
        new_node.parent = node
        new_node.prev_action = (new_node.state[pos], 'Down')
        new_node.path_cost = node.path_cost + 1

        child_nodes.append(new_node)

    new_node=Node()
    new_node.state = list(node.state)
  
    if pos not in {6, 7, 8} and player_position != pos+3:
        temp=new_node.state[pos+3]
        new_node.state[pos+3] = new_node.state[pos]
        new_node.state[pos] = temp

        new_node.update_id()
        new_node.empty=pos+3
        new_node.parent = node
        new_node.prev_action = (new_node.state[pos], 'Up')
        new_node.path_cost = node.path_cost + 1
        child_nodes.append(new_node)

def movePlayerLeft(node, level, dir=LEFT):
    if node.player_position() not in {0, 3, 6}:
        current_tile = tiles_map[node.state[node.player_position()]]
        next_tile = tiles_map[node.state[node.player_position() - 1]]

        if level == 'ground':
            if any(np.array_equal(dir, x) for x in current_tile.ground):
                for dir2 in next_tile.ground:
                    if all(dir + dir2 == np.array((0,0))):
                        new_node=Node()
                        new_node.state = list(node.state)
                        new_node.empty = node.empty
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
                        new_node=Node()
                        new_node.state = list(node.state)
                        new_node.empty = node.empty
                        new_node.state[-2] = node.player_position() - 1
                        new_node.update_id()
                        new_node.parent = node
                        new_node.prev_action = ('Player', 'Left')
                        new_node.path_cost = node.path_cost + 1
                        return new_node
            return None
    else:
        return None

def movePlayerRight(node, level, dir=RIGHT):
    if node.player_position() not in {2, 5, 8}:
        current_tile = tiles_map[node.state[node.player_position()]]
        next_tile = tiles_map[node.state[node.player_position() + 1]]

        if level == 'ground':
            if any(np.array_equal(dir, x) for x in current_tile.ground):
                for dir2 in next_tile.ground:
                    if all(dir + dir2 == np.array((0,0))):
                        new_node=Node()
                        new_node.state = list(node.state)
                        new_node.empty = node.empty
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
                        new_node=Node()
                        new_node.state = list(node.state)
                        new_node.empty = node.empty
                        new_node.state[-2] = node.player_position() + 1
                        new_node.update_id()
                        new_node.parent = node
                        new_node.prev_action = ('Player', 'Right')
                        new_node.path_cost = node.path_cost + 1
                        return new_node
            return None
    else:
        return None

def movePlayerUp(node, level, dir=UP):
    if node.player_position() not in {0, 1, 2}:
        current_tile = tiles_map[node.state[node.player_position()]]
        next_tile = tiles_map[node.state[node.player_position() - 3]]

        if level == 'ground':
            if any(np.array_equal(dir, x) for x in current_tile.ground):
                for dir2 in next_tile.ground:
                    if all(dir + dir2 == np.array((0,0))):
                        new_node=Node()
                        new_node.state = list(node.state)
                        new_node.empty = node.empty
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
                        new_node=Node()
                        new_node.state = list(node.state)
                        new_node.empty = node.empty
                        new_node.state[-2] = node.player_position() - 3
                        new_node.update_id()
                        new_node.parent = node
                        new_node.prev_action = ('Player', 'Up')
                        new_node.path_cost = node.path_cost + 1
                        return new_node
            return None
    else:
        return None

def movePlayerDown(node, level, dir=DOWN):
    if node.player_position() not in {6, 7, 8}:
        current_tile = tiles_map[node.state[node.player_position()]]
        next_tile = tiles_map[node.state[node.player_position() + 3]]

        if level == 'ground':
            if any(np.array_equal(dir, x) for x in current_tile.ground):
                for dir2 in next_tile.ground:
                    if all(dir + dir2 == np.array((0,0))):
                        new_node=Node()
                        new_node.state = list(node.state)
                        new_node.empty = node.empty
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
                        new_node=Node()
                        new_node.state = list(node.state)
                        new_node.empty = node.empty
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
        new_node=Node()
        new_node.state = list(node.state)
        new_node.empty = node.empty
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
        moveEmpty(node, node.empty, child_nodes)
        
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
        child_nodes.append(change_level)
    
    return child_nodes


            
        
    
    