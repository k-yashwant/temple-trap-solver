class Node:
    def __init__(self):
        self.state = ['A','B','C','D','E','F','G','H','Empty',6,0]
        self.id = tuple(self.state)
        self.empty=8
        self.prev_action = None
        self.parent = None
        self.path_cost = 0

    def player_position(self):
        return self.state[-2]
    def update_id(self):
        self.id = tuple(self.state)
    def player_level(self):
        return self.state[-1]

