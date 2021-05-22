from dataclasses import dataclass
import math

import pygame
import numpy as np

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
                elif event.key == pygame.K_SPACE:
                    self.dashing = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.direction[0] += 1
                elif event.key == pygame.K_d:
                    self.direction[0] -= 1
                elif event.key == pygame.K_w:
                    self.direction[1] = (self.direction[1] + 1) if self.direction[1] != 0 else 0
                elif event.key == pygame.K_SPACE:
                    self.dashing = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.projectiles.addProjectile(self.rigidBody.position[0], self.rigidBody.position[1], np.array([-self.rigidBody.position[0] + self.mouseX, -self.rigidBody.position[1] + self.mouseY]), 500.0)

    
    def movement(self, deltaTime):
        gravity = 800
        force = 1500

        # Jumping
        if self.direction[1] < 0:
            if self.grounded:
                self.grounded = False
                self.wallGrounded = False
                self.rigidBody.velocity[1] += -self.jumpForce

            elif self.wallGrounded and self.direction[0] != 0:
                self.grounded = False
                self.wallGrounded = False
                self.rigidBody.velocity[1] += -math.sqrt((self.jumpForce ** 2) / 2)
                self.rigidBody.velocity[0] = self.direction[0] * -math.sqrt((self.jumpForce ** 2) / 2)


            self.direction[1] = 0

        if self.dashCooldownCurrent > 0:
            self.dashCooldownCurrent -= 1

        # Check if grounded
        if(self.grounded):
            self.rigidBody.acceleration[0] = self.direction[0] * force

            # Dashing
            if self.dashing:
                self.dashCooldownCurrent = self.dashCooldownTime
                self.dashing = False
                print(self.rigidBody.velocity[0])
                self.rigidBody.velocity[0] += 1000 * 1
                print(self.rigidBody.velocity[0])
                print()

        else:
            # If not grounded reduce control
            self.rigidBody.acceleration[0] = self.direction[0] * force * 0.2

        # Add gravitational acceleration
        self.rigidBody.acceleration[1] = gravity

        # change velocity from acceleration
        self.rigidBody.velocity += self.rigidBody.acceleration * deltaTime

        # Drag
        if(self.grounded):
            dragForceMagnitude = self.rigidBody.velocity[0] ** 2 * self.rigidBody.drag[0]
            self.rigidBody.velocity[0] -= np.sign(self.rigidBody.velocity[0]) * dragForceMagnitude * deltaTime
        else: 
            dragForceMagnitude = self.rigidBody.velocity[0] ** 2 * self.rigidBody.drag[0] * 0.01
            self.rigidBody.velocity[0] -= np.sign(self.rigidBody.velocity[0]) * dragForceMagnitude * deltaTime

        # Reduces time to stop
        if abs(self.rigidBody.velocity[0]) < 10 and self.rigidBody.acceleration[0] == 0:
            self.rigidBody.velocity[0] = 0

        if self.rigidBody.type == "dynamic":
            self.rigidBody.previousVelocity = self.rigidBody.velocity

        self.rigidBody.position += self.rigidBody.velocity * deltaTime 


    def extra(self, deltaTime):
        self.projectiles.emit(deltaTime)

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
        if groundCheck.collides:
            self.grounded = True
        else: 
            self.grounded = False

        if (wallCheckLeft.collides or wallCheckRight.collides) and not self.grounded:
            self.wallGrounded = True
        else:
            self.wallGrounded = False
    