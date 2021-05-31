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
    def __init__(self, name, points, color, position, controls, material, mass, drag, tags, jumpForce, dashCooldownTime):
        self.name = name
        self.shape = "poly"
        self.temp = False
        # self.rigidBody = Physics.RigidBody(position, mass, drag)
        # self.sprite = Sprite.Circle(30, color)
        # self.collider = Collider.Circle(self.rigidBody, 30, tags)

        self.rigidBody = Physics.RigidBody(position, material, mass, drag)
        self.sprite = Sprite.Polygon(points, color)
        self.collider = Collider.Polygon(self.rigidBody, points, tags)
        self.direction = np.array([0.0, 0.0])
        self.jumpForce = jumpForce
        self.dashing = False
        self.dashCooldownTime = dashCooldownTime
        self.dashCooldownCurrent = 0
        self.grounded = False
        self.jumps = 0
        self.groundCheck = False
        self.wallGrounded = False
        self.wallJumps = 0
        self.wallGrounded = False
        self.controls = controls
        self.inputs = InputVariables
        self.primaryFire = False
        self.mouseX = 0
        self.mouseY = 0
        self.particles = Particles.ParticlePriciple()
        self.projectiles = Projectiles.ProjectilePriciple()
    

    def input(self, events, mousePos):
        self.mouseX, self.mouseY = (mousePos + Globals.camera.rigidBody.position) / Globals.camera.scale

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
                if event.button == 1:
                    self.primaryFire = True
                    self.projectiles.addProjectile(self.rigidBody.position[0], self.rigidBody.position[1], np.array([-self.rigidBody.position[0] + self.mouseX, -self.rigidBody.position[1] + self.mouseY]), 500.0)
                elif event.button == 4:
                    Globals.camera.updateScale(Globals.camera.scale + 0.1)

                elif event.button == 5:
                   Globals.camera.updateScale(Globals.camera.scale - 0.1)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.primaryFire = False

    
    def movement(self, deltaTime):
        gravity = 800
        force = 1000


        if self.wallGrounded:
            self.groundCheck = False
            if self.wallCheck:
                self.wallJumps = 1
                self.wallCheck = False
        else:
            self.wallCheck = True



        if self.grounded:
            if self.groundCheck:
                self.jumps = 1
                self.groundCheck = False
        else:
            self.groundCheck = True
    


        # Jumping
        if self.direction[1] < 0:
            if self.wallJumps > 0 and self.direction[0] != 0:
                self.wallJumps -= 1
                self.rigidBody.velocity[1] += -math.sqrt((self.jumpForce ** 2) / 2)
                self.rigidBody.velocity[0] = self.direction[0] * -math.sqrt((self.jumpForce ** 2) / 2)

            elif self.jumps > 0:
                self.jumps -= 1
                self.rigidBody.velocity[1] = -self.jumpForce if self.rigidBody.velocity[1] > 0 else self.rigidBody.velocity[1] - self.jumpForce

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
                self.rigidBody.velocity[0] += 500 * self.direction[0]

        else:
            # If not grounded reduce control
            self.rigidBody.acceleration[0] = self.direction[0] * force * 0.4

        # Add gravitational acceleration
        self.rigidBody.acceleration[1] = gravity

        # change velocity from acceleration
        self.rigidBody.velocity += self.rigidBody.acceleration * deltaTime
        

        # Friction
        if(self.collider.noCollisionsDetected > 0):
            for i in range (0, self.collider.noCollisionsDetected):
                
                # Direciton object collides with surface
                reactionVector = self.collider.autoCollisionsDetails[i].reactionVectorObject2
                
                # Bounds to check that velocity is in the direciton of surface
                angle1 = math.atan2(self.collider.autoCollisionsDetails[i].reactionVectorObject2[1], self.collider.autoCollisionsDetails[i].reactionVectorObject2[0]) - math.pi / 2
                angle2 = math.atan2(self.collider.autoCollisionsDetails[i].reactionVectorObject2[1], self.collider.autoCollisionsDetails[i].reactionVectorObject2[0]) + math.pi / 2

                # Angle between velocity and surface
                velocityFloorAngle = math.atan2(reactionVector[0] * self.rigidBody.velocity[1] - reactionVector[1] * self.rigidBody.velocity[0],
                              reactionVector[0] * self.rigidBody.velocity[0] + reactionVector[1] * self.rigidBody.velocity[1])

                # Checks if angle of velocity is between normal force vector angle +/- 90 degrees
                if (angle1 < math.atan2(self.rigidBody.velocity[1], self.rigidBody.velocity[0]) - 2 * math.pi < angle2 or
                    angle1 < math.atan2(self.rigidBody.velocity[1], self.rigidBody.velocity[0])               < angle2 or
                    angle1 < math.atan2(self.rigidBody.velocity[1], self.rigidBody.velocity[0]) + 2 * math.pi < angle2):
                    

                    # Checks which direction the perpendicular vector should be based on velocity direciton
                    if velocityFloorAngle > 0:
                        perpendicularVector = np.array([-self.collider.autoCollisionsDetails[i].reactionVectorObject2[1], self.collider.autoCollisionsDetails[i].reactionVectorObject2[0]])
                
                    elif velocityFloorAngle < 0:
                        perpendicularVector = np.array([self.collider.autoCollisionsDetails[i].reactionVectorObject2[1], -self.collider.autoCollisionsDetails[i].reactionVectorObject2[0]])

                    else:
                        break


                    # Swaps x and y of acceleration vector
                    swappedAcceleration = np.array([self.rigidBody.acceleration[1], self.rigidBody.acceleration[0]])


                    # Projects swapped acceleration vector to surface
                    projectedNormalForce = (np.dot(swappedAcceleration, perpendicularVector) / np.linalg.norm(perpendicularVector) ** 2) * perpendicularVector

                    # Sets direciton of projected vector to velocity
                    if self.rigidBody.velocity[0] < 0:
                        projectedNormalForce[0] = -abs(projectedNormalForce[0])
                    else:
                        projectedNormalForce[0] = abs(projectedNormalForce[0])

                    if self.rigidBody.velocity[1] < 0:
                        projectedNormalForce[1] = -abs(projectedNormalForce[1])
                    else:
                        projectedNormalForce[1] = abs(projectedNormalForce[1])

                    coefficientOfFriction = Globals.friction_Coefficients[self.collider.autoCollisionsDetected[i].rigidBody.material, 
                                                                          self.collider.autoCollisionsDetected[i].collider.autoCollisionsDetected[i].rigidBody.material]

                    # Creates friction vector from projected vector
                    frictionVector = -coefficientOfFriction * projectedNormalForce

                    # If velocity is smaller than friction, set velocity to 0
                    if abs(self.rigidBody.velocity[0]) > abs(frictionVector[0]) * deltaTime:
                        self.rigidBody.velocity[0] = self.rigidBody.velocity[0] + frictionVector[0] * deltaTime
                    else:
                        self.rigidBody.velocity[0] = 0

                    if abs(self.rigidBody.velocity[1]) > abs(frictionVector[1]) * deltaTime:
                        self.rigidBody.velocity[1] = self.rigidBody.velocity[1] + frictionVector[1] * deltaTime
                    else:
                        self.rigidBody.velocity[1] = 0



        # Drag
        self.rigidBody.velocity *= (1.0 - self.rigidBody.drag) ** deltaTime

        # Reduces time to stop
        if abs(self.rigidBody.velocity[0]) < 10 and self.rigidBody.acceleration[0] == 0:
            self.rigidBody.velocity[0] = 0

        if self.rigidBody.type == "dynamic":
            self.rigidBody.previousVelocity = self.rigidBody.velocity

        self.rigidBody.position += self.rigidBody.velocity * deltaTime 



    def extra(self, deltaTime):
        self.projectiles.emit(deltaTime)

        aim = Physics.rayCast(self.rigidBody.position, np.array([-self.rigidBody.position[0] + self.mouseX, -self.rigidBody.position[1] + self.mouseY]), 200, self)

        groundCheck = Physics.PolyCast(self.rigidBody.position + np.array([0, self.collider.mostDownPoint()[1]]), 
                                       np.array([0, 1]), np.array([[-20, -0.5], [20, -0.5], [20, 0.5], [-20, 0.5]]), 1, self)

        wallCheckLeft =  Physics.rayCast(self.rigidBody.position + np.array([self.collider.mostLeftPoint()[0], 
                                         self.collider.mostDownPoint()[1] - 2]), np.array([-1, 0]), 4, self)

        wallCheckRight = Physics.rayCast(self.rigidBody.position + np.array([self.collider.mostRightPoint()[0], 
                                         self.collider.mostDownPoint()[1] - 2]), np.array([1, 0]), 4, self)

        # groundCheck = Physics.PolyCast(self.rigidBody.position + np.array([0, self.collider.radius + 2]), 
        #                                np.array([0, 1]), np.array([[-19, -0.5], [19, -0.5], [19, 0.5], [-19, 0.5]]), 1, self)

        # wallCheckLeft =  Physics.rayCast(self.rigidBody.position + np.array([0, self.collider.radius]), np.array([-1, 0]), 24, self)
        # wallCheckRight = Physics.rayCast(self.rigidBody.position + np.array([0, self.collider.radius]), np.array([1, 0]), 24, self)

        
        Globals.objects.append(Entities.SpriteCircle(self.mouseX, self.mouseY, 5, Physics.Materials.METAL, (200, 200, 200)))

        if aim.collides:
            Globals.objects.append(Entities.SpriteCircle(aim.intercept[0], aim.intercept[1], 5, Physics.Materials.METAL, (0, 0, 255)))
        


        # Check if able to jump
        if groundCheck.collides:
            self.grounded = True
        else: 
            self.grounded = False

        if wallCheckLeft.collides or wallCheckRight.collides:
            self.wallGrounded = True
        else:
            self.wallGrounded = False
    