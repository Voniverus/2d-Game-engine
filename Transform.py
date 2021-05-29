import numpy as np


def translationMatrix(deltaX, deltaY):
    return np.array([[1,      0,      deltaX], 
                     [0,      1,      deltaY],
                     [0,      0,      1     ]])

def scaleMatrix(scaleX, scaleY):
    return np.array([[scaleX, 0,      0], 
                     [0,      scaleY, 0],
                     [0,      0,      1]])

def translatePoint(pos, delta):
    v = np.matmul(translationMatrix(delta[0], delta[1]), np.array([pos[0], pos[1], 1]))
    return np.array([v[0], v[1]])

def scalePoint(pos, scale):
    v = np.matmul(scaleMatrix(scale, scale), np.array([pos[0], pos[1], 1]))
    return np.array([v[0], v[1]])
