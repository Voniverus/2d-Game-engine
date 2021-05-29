import numpy as np

import pygame
from pygame.locals import * 

import Physics
import Colors

import Globals

def draw(dis, objects):
    #Clear screen
    dis.fill(Colors.black)
    for obj in objects:
        # Draw all objects
        if obj.shape == "poly":
            pygame.draw.polygon(dis, obj.sprite.color, [(x + obj.rigidBody.position) * Globals.camera.scale - Globals.camera.rigidBody.position for x in obj.sprite.points], 2)

        elif obj.shape == "line":
            pygame.draw.line(dis, obj.color, (obj.start) * Globals.camera.scale - Globals.camera.rigidBody.position, obj.end * Globals.camera.scale - Globals.camera.rigidBody.position)

        elif obj.shape == "circle":
            pygame.draw.circle(dis, obj.sprite.color, (obj.rigidBody.position) * Globals.camera.scale - Globals.camera.rigidBody.position, obj.sprite.radius * Globals.camera.scale, 2)
            
    pygame.display.flip()

    Globals.objects = [obj for obj in Globals.objects if not obj.temp]


def update(gameObjects, players, deltaTime):

    for obj in gameObjects:
        if obj.rigidBody.type != "static":
            obj.movement(deltaTime)

    # Auto collision detection
    for obj in gameObjects:
        if obj.collider.getCollisionType() != "none":
            obj.collider.clearAutoCollisions()

    for i in range(0, len(gameObjects) - 1):
        if True:  # Has a collision type
            for j in range(i + 1, len(gameObjects)):
                if gameObjects[j].collider.getCollisionType() != "none":
                    cDet = Physics.objectsCollide(gameObjects[i], gameObjects[j])
                    if cDet.collides:
                        gameObjects[i].collider.addAutoCollision(gameObjects[j], cDet)
                        gameObjects[j].collider.addAutoCollision(gameObjects[i], cDet.swappedObjects())

                        if gameObjects[i].rigidBody.type != "static":
                            gameObjects[i].collider.reactToCollisions(gameObjects[j], deltaTime)

                        if gameObjects[j].rigidBody.type != "static":
                            gameObjects[j].collider.reactToCollisions(gameObjects[i], deltaTime)
                       
                            
    for player in players:
        player.extra(deltaTime)
