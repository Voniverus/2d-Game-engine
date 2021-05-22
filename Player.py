import pygame
import numpy as np
from dataclasses import dataclass

import Physics
import Sprite
import Collider
import Globals
import Entities
import Particles
import Projectiles

@dataclass
class InputVariables():
    left: int
    right: int
    up: int
    mousePos: np.ndarray
    particleTrigger: bool

    def getHorizontal(self):
        return self.right - self.left

class Player:
    def __init__(self, name, points, color, position, controls, mass, drag, tags, jumpForce, dashCooldownTime):
        self.name = name
        self.shape = "poly"
        self.temp = False
        # self.rigidBody = Physics.RigidBody(position, mass, drag)
        # self.sprite = Sprite.Circle(30, color)
        # self.collider = Collider.Circle(self.rigidBody, 30, tags)

        self.rigidBody = Physics.RigidBody(position, mass, drag)
        self.sprite = Sprite.Polygon(points, color)
        self.collider = Collider.Polygon(self.rigidBody, points, tags)
        self.direction = np.array([0.0, 0.0])
        self.jumpForce = jumpForce
        self.dashing = False
        self.dashCooldownTime = dashCooldownTime
        self.dashCooldownCurrent = 0
        self.grounded = False
        self.playerGrounded = False
        self.wallGrounded = False
        self.controls = controls
        self.inputs = InputVariables
        self.mouseX = 0
        self.mouseY = 0
        self.particles = Particles.ParticlePriciple()
        self.projectiles = Projectiles.ProjectilePriciple()
    

    def input(self, events, mousePos):
        self.mouseX, self.mouseY = mousePos + Globals.camera.rigidBody.position

        for event in events:
            if event.type == pygame.QUIT:
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.direction[0] -= 1
                elif event.key == pygame.K_d:
                    self.direction[0] += 1
                elif event.key == pygame.K_w:
                    self.direction[1] -= 1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.direction[0] += 1
                elif event.key == pygame.K_d:
                    self.direction[0] -= 1
                elif event.key == pygame.K_w:
                    self.direction[1] = (self.direction[1] + 1) if self.direction[1] != 0 else 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.projectiles.addProjectile(self.rigidBody.position[0], self.rigidBody.position[1], np.array([-self.rigidBody.position[0] + self.mouseX, -self.rigidBody.position[1] + self.mouseY]), 500.0)

    
    def logic(self, deltaTime, width, height):
        # Check for wall jump
        if(self.rigidBody.position[0] <= 5 and self.rigidBody.velocity[0] < 0) or (self.rigidBody.position[0] >= width - 15 and self.rigidBody.velocity[0] > 0):
            self.wallGrounded = True
        else: 
            self.wallGrounded = False


        aim = Physics.rayCast(self.rigidBody.position, np.array([-self.rigidBody.position[0] + self.mouseX, -self.rigidBody.position[1] + self.mouseY]), 200, self)

        groundCheck = Physics.PolyCast(self.rigidBody.position + np.array([0, self.collider.mostDownPoint()[1] + 2]), 
                                       np.array([0, 1]), np.array([[-19, -0.5], [19, -0.5], [19, 0.5], [-19, 0.5]]), 1, self)

        wallCheckLeft =  Physics.rayCast(self.rigidBody.position + np.array([self.collider.mostLeftPoint()[0], 0]), np.array([-1, 0]), 24, self)
        wallCheckRight = Physics.rayCast(self.rigidBody.position + np.array([self.collider.mostRightPoint()[0], 0]), np.array([1, 0]), 24, self)

        # groundCheck = Physics.PolyCast(self.rigidBody.position + np.array([0, self.collider.radius + 2]), 
        #                                np.array([0, 1]), np.array([[-19, -0.5], [19, -0.5], [19, 0.5], [-19, 0.5]]), 1, self)

        # wallCheckLeft =  Physics.rayCast(self.rigidBody.position + np.array([0, self.collider.radius]), np.array([-1, 0]), 24, self)
        # wallCheckRight = Physics.rayCast(self.rigidBody.position + np.array([0, self.collider.radius]), np.array([1, 0]), 24, self)

        
        Globals.objects.append(Entities.SpriteCircle(self.mouseX, self.mouseY, 5, (200, 200, 200)))

        if aim.collides:
            Globals.objects.append(Entities.SpriteCircle(aim.intercept[0], aim.intercept[1], 5, (0, 0, 255)))
        
        # Check if able to jump
        if(self.rigidBody.position[1] >= height - self.collider.mostDownPoint()[1]) or groundCheck.collides:
            self.grounded = True
        else: 
            self.grounded = False

        if(self.rigidBody.position[0] >= width - self.collider.mostRightPoint()[0] or self.rigidBody.position[0] <= -self.collider.mostLeftPoint()[0] or 
           wallCheckLeft.collides or wallCheckRight.collides) and not self.grounded:
            self.wallGrounded = True
        else:
            self.wallGrounded = False


        # # Check if able to jump
        # if(self.rigidBody.position[1] >= height - self.collider.radius) or groundCheck.collides:
        #     self.grounded = True
        # else: 
        #     self.grounded = False

        # if(self.rigidBody.position[0] >= width + self.collider.radius or self.rigidBody.position[0] <= +self.collider.radius or 
        #    wallCheckLeft.collides or wallCheckRight.collides) and not self.grounded:
        #     self.wallGrounded = True
        # else:
        #     self.wallGrounded = False



        self.projectiles.emit(deltaTime)


    