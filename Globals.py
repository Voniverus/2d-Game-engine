import pygame

import Collider
import Entities
import numpy as np

def init():
    global objects
    global gameObjects
    global lastUsedID
    global PARTICLE_EVENT
    global tagValues
    global camera

    objects = []
    gameObjects = []
    lastUsedID = 0

    camera = Entities.Camera("main camera", np.array([0, 0]), 600, 400)

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

def getLastUsedID():
    global lastUsedID
    x = lastUsedID
    lastUsedID += 1
    return x
    