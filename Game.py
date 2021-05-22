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

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

player = Player("Player", np.array([[-20, 20], [0, -20], [20, 20]]), Colors.green, np.array([0.0, 0.0]), "arrows", 9, np.array([0.05, 0]), Collider.Tag.PLAYER, 350, 150)

Globals.gameObjects.append(player)
Globals.objects.append(player)

floor = Entities.StaticPoly("floor", np.array([[-150, -15], [150, -15], [150, 15], [-150, 15]]), np.array([0.0, 200.0]), Colors.grey, Collider.Tag.BARRIER)
Globals.gameObjects.append(floor)
Globals.objects.append(floor)


def displayScore(score):
    value = score_font.render("Score: " + str(score), True, Colors.white)
    dis.blit(value, [0, 0])
 

def draw():
    #Clear screen
    dis.fill(Colors.black)
    print("B")
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
            

def displayMessage(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [width / 6, height / 3])


def updatePlayer(player, force, drag, deltaTime):
    gravity = 800

    player.logic(deltaTime, width, height)

    if player.dashCooldownCurrent > 0:
        player.dashCooldownCurrent -= 1


    # Check if grounded
    if(player.grounded):
        player.rigidBody.acceleration[0] = player.direction[0] * force

        # Dashing
        if player.dashing:
            player.dashCooldownCurrent = player.dashCooldownTime
            player.dashing = False
            player.rigidBody.velocity[0] += 2000 * player.direction[0]

    else:
         # If not grounded reduce control
        player.rigidBody.acceleration[0] = player.direction[0] * force * 0.2

    # Add gravitational acceleration
    player.rigidBody.acceleration[1] = gravity
    

    # Jumping
    if player.direction[1] < 0:
        if player.grounded:
            player.grounded = False
            player.wallGrounded = False
            player.rigidBody.velocity[1] += -player.jumpForce

        elif player.wallGrounded and player.direction[0] != 0:
            player.grounded = False
            player.wallGrounded = False
            player.rigidBody.velocity[1] += -math.sqrt((player.jumpForce ** 2) / 2)
            player.rigidBody.velocity[0] = player.direction[0] * -math.sqrt((player.jumpForce ** 2) / 2)


        player.direction[1] = 0


    # change velocity from acceleration
    player.rigidBody.velocity += player.rigidBody.acceleration * deltaTime


    # Drag
    if(player.grounded):
        dragForceMagnitude = player.rigidBody.velocity[0] ** 2 * drag[0]
        player.rigidBody.velocity[0] -= np.sign(player.rigidBody.velocity[0]) * dragForceMagnitude * deltaTime
    else: 
        dragForceMagnitude = player.rigidBody.velocity[0] ** 2 * drag[0] * 0.01
        player.rigidBody.velocity[0] -= np.sign(player.rigidBody.velocity[0]) * dragForceMagnitude * deltaTime


    # Reduces time to stop
    if abs(player.rigidBody.velocity[0]) < 10 and player.rigidBody.acceleration[0] == 0:
        player.rigidBody.velocity[0] = 0

    player.collider.updatePosition(deltaTime)


def update(deltaTime):
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
                            
    # Update
    for obj in Globals.gameObjects:
        if obj == player:
            updatePlayer(obj, 1500, np.array([0.05, 0]), deltaTime)
        
        else:
            obj.collider.updatePosition(deltaTime)

    Globals.camera.updatePosition(player.rigidBody.position[0], player.rigidBody.position[1])


def gameLoop():
    game_over = False
    game_close = False

    time = 0. 

    while not game_over:
        while game_close:
            dis.fill(Colors.black)
            displayMessage("You Lost! Press C: Play Again or Q: Quit", Colors.white)
            pygame.display.update()
 
        player.input(pygame.event.get(), pygame.mouse.get_pos())
        
        deltaTime = time / 1000.0    
        
        update(deltaTime)

        time = clock.tick(30)

        draw()
    
    pygame.quit()
    quit()

 
gameLoop()