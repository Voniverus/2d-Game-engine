import numpy as np

import Entities
import Globals
import Physics
import Colors
import Collider
from Player import Player


def createPlayer():
    player = Player("Player", np.array([[-20, 20], [0, -20], [20, 20]]), Colors.green, np.array([0.0, 0.0]), "arrows", 
                Physics.Materials.PLAYER, 10.0, np.array([0.05, 0]), Collider.Tag.PLAYER, 350, 150)

    return player

def init():
    floor = Entities.StaticPoly("floor", np.array([[-150, -15], [150, -15], [150, 15], [-150, 15]]), np.array([0.0, 200.0]), 
                                Physics.Materials.METAL, Colors.grey, Collider.Tag.BARRIER)
   


    wallLeft = Entities.StaticPoly("wall left", np.array([[-15, -150], [0, -150], [30, 150], [-15, 150]]), np.array([-240.0, 200.0]), 
                                Physics.Materials.METAL, Colors.grey, Collider.Tag.BARRIER)



    wallRight = Entities.StaticPoly("wall right", np.array([[-0, -150], [15, -150], [15, 150], [-30, 150]]), np.array([240.0, 200.0]), 
                                Physics.Materials.METAL, Colors.grey, Collider.Tag.BARRIER)
                                
    return [floor, wallLeft, wallRight]