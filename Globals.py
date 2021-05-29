import pygame

import numpy as np

import Collider
import Entities
import Physics


def init():
    global objects
    global gameObjects
    global lastUsedID
    global PARTICLE_EVENT
    global tagValues
    global camera
    global frameRate

    global friction_Coefficients

    frameRate = 300

    objects = []
    gameObjects = []
    lastUsedID = 0

    camera = Entities.Camera("main camera", np.array([0, 0]), 600, 400, 1.0)

    PARTICLE_EVENT = pygame.USEREVENT + 1
    tagValues = {          Collider.Tag.BARRIER: (Collider.Tag.BARRIER, 
                                                  Collider.Tag.PLAYER, 
                                                  Collider.Tag.ENEMY, 
                                                  Collider.Tag.PLAYER_PROJECTILE,
                                                  Collider.Tag.ENEMY_PROJECTILE), 

                            Collider.Tag.PLAYER: (Collider.Tag.BARRIER, 
                                                  Collider.Tag.PLAYER, 
                                                  Collider.Tag.ENEMY, 
                                                  Collider.Tag.ENEMY_PROJECTILE), 
                                        
                             Collider.Tag.ENEMY: (Collider.Tag.BARRIER, 
                                                  Collider.Tag.PLAYER, 
                                                  Collider.Tag.ENEMY, 
                                                  Collider.Tag.PLAYER_PROJECTILE), 

                 Collider.Tag.PLAYER_PROJECTILE: (Collider.Tag.BARRIER, 
                                                  Collider.Tag.PLAYER, 
                                                  Collider.Tag.ENEMY, 
                                                  Collider.Tag.ENEMY_PROJECTILE,
                                                  Collider.Tag.PLAYER_PROJECTILE), 

                  Collider.Tag.ENEMY_PROJECTILE: (Collider.Tag.BARRIER, 
                                                  Collider.Tag.PLAYER, 
                                                  Collider.Tag.ENEMY, 
                                                  Collider.Tag.PLAYER_PROJECTILE)}

    friction_Coefficients = {}
    friction_Coefficients[Physics.Materials.PLAYER, Physics.Materials.METAL]  = 0.4 
    friction_Coefficients[Physics.Materials.PLAYER, Physics.Materials.ICE]    = 0.01
    friction_Coefficients[Physics.Materials.PLAYER, Physics.Materials.GLUE]   = 0.99

    friction_Coefficients[Physics.Materials.METAL,  Physics.Materials.PLAYER] = 0.4 
    friction_Coefficients[Physics.Materials.ICE,    Physics.Materials.PLAYER] = 0.01
    friction_Coefficients[Physics.Materials.GLUE,   Physics.Materials.PLAYER] = 0.99

def getLastUsedID():
    global lastUsedID
    x = lastUsedID
    lastUsedID += 1
    return x
    