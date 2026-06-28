#stores the tile pieces

import numpy as np

'''
self.piece can be 'top','ground' and 'stair'


rotateCounterClockwise is used to rotate the direction 90 degrees times 'rotation' clockwise
'''

rotation_matrix = np.array([[0,1],[-1,0]])


class TileA:
    def __init__(self, rotation):
        self.piece = 'top'
        self.letter = 'A'
        self.ground = []
        self.top = [np.array((0,1)),np.array((1,0))]
        
        for i in range(len(self.ground)):
            self.ground[i] = np.dot(np.linalg.matrix_power(rotation_matrix,rotation), self.ground[i])
        for i in range(len(self.top)):
            self.top[i] = np.dot(np.linalg.matrix_power(rotation_matrix,rotation), self.top[i])

class TileB:
    def __init__(self, rotation):
        self.piece = 'top'
        self.letter = 'B'
        self.ground = []
        self.top = [np.array((0,1)),np.array((1,0))]

        for i in range(len(self.ground)):
            self.ground[i] = np.dot(np.linalg.matrix_power(rotation_matrix,rotation), self.ground[i])
        for i in range(len(self.top)):
            self.top[i] = np.dot(np.linalg.matrix_power(rotation_matrix,rotation), self.top[i])

class TileC:
    def __init__(self, rotation):
        self.piece = 'top'
        self.letter = 'C'
        self.ground = []
        self.top = [np.array((-1,0)),np.array((1,0))]

        for i in range(len(self.ground)):
            self.ground[i] = np.dot(np.linalg.matrix_power(rotation_matrix,rotation), self.ground[i])
        for i in range(len(self.top)):
            self.top[i] = np.dot(np.linalg.matrix_power(rotation_matrix,rotation), self.top[i])

class TileD:
    def __init__(self, rotation):
        self.piece = 'stair'
        self.letter = 'D'
        self.ground = [np.array((1,0))]
        self.top = [np.array((-1,0))]

        for i in range(len(self.ground)):
            self.ground[i] = np.dot(np.linalg.matrix_power(rotation_matrix,rotation), self.ground[i])
        for i in range(len(self.top)):
            self.top[i] = np.dot(np.linalg.matrix_power(rotation_matrix,rotation), self.top[i])


class TileE:
    def __init__(self, rotation):
        self.piece = 'stair'
        self.letter = 'E'
        self.ground = [np.array((1,0))]
        self.top = [np.array((-1,0))]

        for i in range(len(self.ground)):
            self.ground[i] = np.dot(np.linalg.matrix_power(rotation_matrix,rotation), self.ground[i])
        for i in range(len(self.top)):
            self.top[i] = np.dot(np.linalg.matrix_power(rotation_matrix,rotation), self.top[i])


class TileF:
    def __init__(self, rotation):
        self.piece = 'ground'
        self.letter = 'F'
        self.ground = [np.array((1,0)),np.array((0,1))]
        self.top = []

        for i in range(len(self.ground)):
            self.ground[i] = np.dot(np.linalg.matrix_power(rotation_matrix,rotation), self.ground[i])
        for i in range(len(self.top)):
            self.top[i] = np.dot(np.linalg.matrix_power(rotation_matrix,rotation), self.top[i])


class TileG:
    def __init__(self, rotation):
        self.piece = 'ground'
        self.letter = 'G'
        self.ground = [np.array((1,0)),np.array((0,1))]
        self.top = []

        for i in range(len(self.ground)):
            self.ground[i] = np.dot(np.linalg.matrix_power(rotation_matrix,rotation), self.ground[i])
        for i in range(len(self.top)):
            self.top[i] = np.dot(np.linalg.matrix_power(rotation_matrix,rotation), self.top[i])


class TileH:
    def __init__(self, rotation):
        self.piece = 'ground'
        self.letter = 'H'
        self.ground = [np.array((1,0)),np.array((0,1))]
        self.top = []

        for i in range(len(self.ground)):
            self.ground[i] = np.dot(np.linalg.matrix_power(rotation_matrix,rotation), self.ground[i])
        for i in range(len(self.top)):
            self.top[i] = np.dot(np.linalg.matrix_power(rotation_matrix,rotation), self.top[i])

class Empty:
    def __init__(self, rotation):
        self.piece = 'empty'
        self.letter = 'empty'
        self.ground = []
        self.top = []


tiles_map_template= {'A':TileA, 'B':TileB, 'C':TileC, 'D':TileD, 'E':TileE, 'F':TileF, 'G':TileG, 'H':TileH, 'empty':Empty(None)}


