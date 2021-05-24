import numpy as np

import pygame
from pygame.locals import *

import time
import random
import math 

import Physics
import Entities
import Colors
from Player import Player 
import Collider

import Globals

Globals.init()
pygame.init()

width = 600
height = 400
 
dis = pygame.display.set_mode((width, height))

pygame.display.set_caption('Physics based platformer')
 
clock = pygame.time.Clock()


player = Player("Player", np.array([[-20, 20], [0, -20], [20, 20]]), Colors.green, np.array([0.0, 0.0]), "arrows", 10.0, np.array([0.05, 0]), Collider.Tag.PLAYER, 350, 150)

Globals.gameObjects.append(player)
Globals.objects.append(player)

floor = Entities.StaticPoly("floor", np.array([[-150, -15], [150, -15], [150, 15], [-150, 15]]), np.array([0.0, 200.0]), Colors.grey, Collider.Tag.BARRIER)
Globals.gameObjects.append(floor)
Globals.objects.append(floor)



def draw():
    #Clear screen
    dis.fill(Colors.black)
    for obj in Globals.objects:
        # Draw all objects
        if obj.shape == "poly":
            pygame.draw.polygon(dis, obj.sprite.color, [x + obj.rigidBody.position - Globals.camera.rigidBody.position for x in obj.sprite.points], 2)

        elif obj.shape == "line":
            pygame.draw.line(dis, obj.color, obj.start - Globals.camera.rigidBody.position, obj.end - Globals.camera.rigidBody.position)

        elif obj.shape == "circle":
            pygame.draw.circle(dis, obj.sprite.color, obj.rigidBody.position - Globals.camera.rigidBody.position, obj.sprite.radius, 2)
            
    pygame.display.flip()

    Globals.objects = [obj for obj in Globals.objects if not obj.temp]


def update(deltaTime):
    for obj in Globals.gameObjects:
        if obj == player:
            obj.movement(deltaTime)

    # Auto collision detection
    if True:    # Auto collision on
        for obj in Globals.gameObjects:
            if obj.collider.getCollisionType() != "none":
                obj.collider.clearAutoCollisions()

        for i in range(0, len(Globals.gameObjects) - 1):
            if True:  # Has a collision type
                for j in range(i + 1, len(Globals.gameObjects)):
                    if Globals.gameObjects[j].collider.getCollisionType() != "none":
                        cDet = Physics.objectsCollide(Globals.gameObjects[i], Globals.gameObjects[j])
                        if cDet.collides:
                            Globals.gameObjects[i].collider.addAutoCollision(Globals.gameObjects[j], cDet)
                            Globals.gameObjects[j].collider.addAutoCollision(Globals.gameObjects[i], cDet.swappedObjects())

                            if Globals.gameObjects[i].rigidBody.type != "static":
                                Globals.gameObjects[i].collider.reactToCollisions(Globals.gameObjects[j], deltaTime)

                            if Globals.gameObjects[j].rigidBody.type != "static":
                                Globals.gameObjects[j].collider.reactToCollisions(Globals.gameObjects[i], deltaTime)
                            
    player.extra(deltaTime)

    Globals.camera.updatePosition(player.rigidBody.position[0], player.rigidBody.position[1])


def gameLoop():
    game_over = False
    game_close = False

    time = 0. 

    while not game_over:
        while game_close:
            dis.fill(Colors.black)
            pygame.display.update()
 
        player.input(pygame.event.get(), pygame.mouse.get_pos())
        
        deltaTime = time / 1000.0

        update(deltaTime)

        time = clock.tick(Globals.frameRate)

        draw()
    
    pygame.quit()
    quit()

 
gameLoop()