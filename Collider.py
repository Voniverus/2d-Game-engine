import enum

import numpy as np

import Entities
import Globals
import Physics

class Tag(enum.Enum):
    BARRIER           = 1
    PLAYER            = 2
    ENEMY             = 3
    PLAYER_PROJECTILE = 4
    ENEMY_PROJECTILE  = 5


class Polygon:
    def __init__(self, rigidBody, points, tag):
        self.rigidBody = rigidBody
        self.collisionType = "poly"
        self.points = points
        self.tag = tag
        self.noCollisionsDetected = 0
        self.autoCollisionsDetected = []
        self.autoCollisionsDetails = []

    def getCollisionPoints(self):
        return self.points
        

    def getWidth(self):
        width = 0.0
        for point1 in self.points:
            for point2 in self.points:
                if abs(point2[0] - point1[0]) > width:
                    width = abs(point2[0] - point1[0])

        return width

    def getHeight(self):
        height = 0.0
        for point1 in self.points:
            for point2 in self.points:
                if abs(point2[1] - point1[1]) > height:
                    height = abs(point2[1] - point1[1])

        return height

    def mostLeftPoint(self):
        mostLeft = np.array([float('inf'), 0])
        for point in self.points:
            if point[0] < mostLeft[0]:
                mostLeft = point

        return mostLeft

    def mostRightPoint(self):
        mostRight = np.array([float('-inf'), 0])
        for point in self.points:
            if point[0] > mostRight[0]:
                mostRight = point

        return mostRight

    def mostUpPoint(self):
        mostUp = np.array([0, float('inf')])
        for point in self.points:
            if point[1] < mostUp[1]:
                mostUp = point

        return mostUp

    def mostDownPoint(self):
        mostDown = np.array([0, float('-inf')])
        for point in self.points:
            if point[1] > mostDown[1]:
                mostDown = point

        return mostDown

    def getCollisionCircleRadius(self):
        radius = 0.0
        for point in self.points:
            if np.linalg.norm(point) > radius:
                radius = np.linalg.norm(point)

        return radius

    def addAutoCollision(self, gameObj, cDet):
        self.autoCollisionsDetected.append(gameObj)
        self.autoCollisionsDetails.append(cDet)
        self.noCollisionsDetected += 1


    def clearAutoCollisions(self):
        self.autoCollisionsDetected.clear()
        self.autoCollisionsDetails.clear()
        self.noCollisionsDetected = 0


    def getCollisionType(self):
        return self.collisionType


    def reactToCollisions(self, other, deltaTime):
        for i in range (0, self.noCollisionsDetected):
            
            centerAx = np.array([-self.autoCollisionsDetails[i].collisionPointObject1[0], -self.autoCollisionsDetails[i].collisionPointObject1[1]])

            # Globals.objects.append(Entities.Circle(self.rigidBody.position[0] + self.autoCollisionsDetails[i].collisionPointObject1[0], 
            #                                     self.rigidBody.position[1] + self.autoCollisionsDetails[i].collisionPointObject1[1], 5, (60, 60, 255)))

            # Globals.objects.append(Entities.Line(self.rigidBody.position[0] + self.autoCollisionsDetails[i].collisionPointObject1[0],
            #                                   self.rigidBody.position[1] + self.autoCollisionsDetails[i].collisionPointObject1[1],
            #                                   self.rigidBody.position[0] + self.autoCollisionsDetails[i].collisionPointObject1[0] + self.autoCollisionsDetails[i].reactionVectorObject1[0], 
            #                                   self.rigidBody.position[1] + self.autoCollisionsDetails[i].collisionPointObject1[1] + self.autoCollisionsDetails[i].reactionVectorObject1[1], (200, 30, 30)))

            reactionVector = self.autoCollisionsDetails[i].reactionVectorObject1 / np.linalg.norm(self.autoCollisionsDetails[i].reactionVectorObject1)

            
            self.rigidBody.position += self.autoCollisionsDetails[i].reactionVectorObject1

            if other.rigidBody.type == "static":
                self.rigidBody.velocity = self.rigidBody.velocity - 1 * (np.dot(self.rigidBody.velocity, reactionVector)) * reactionVector

            elif other.rigidBody.type == "dynamic":            
                self.rigidBody.velocity = (((self.rigidBody.mass * self.rigidBody.previousVelocity) + 
                                            (other.rigidBody.mass * other.rigidBody.previousVelocity) + 
                                            (other.rigidBody.mass * 0.8 * (other.rigidBody.previousVelocity - self.rigidBody.previousVelocity))) / 
                                            (self.rigidBody.mass + other.rigidBody.mass))

class Circle:
    def __init__(self, rigidBody, radius, tag):
        self.rigidBody = rigidBody
        self.collisionType = "circle"
        self.radius = radius
        self.tag = tag
        self.noCollisionsDetected = 0
        self.autoCollisionsDetected = []
        self.autoCollisionsDetails = []
        

    def getDiameter(self):
        return self.radius * 2

    def getCollisionCircleRadius(self):
        return self.radius

    def addAutoCollision(self, gameObj, cDet):
        self.autoCollisionsDetected.append(gameObj)
        self.autoCollisionsDetails.append(cDet)
        self.noCollisionsDetected += 1


    def clearAutoCollisions(self):
        self.autoCollisionsDetected.clear()
        self.autoCollisionsDetails.clear()
        self.noCollisionsDetected = 0


    def getCollisionType(self):
        return self.collisionType


    def reactToCollisions(self, other, deltaTime):
        for i in range (0, self.noCollisionsDetected):
            Globals.objects.append(Entities.SpriteCircle(self.rigidBody.position[0] + self.autoCollisionsDetails[i].collisionPointObject1[0], 
                                                         self.rigidBody.position[1] + self.autoCollisionsDetails[i].collisionPointObject1[1],
                                                         5, Physics.Materials.METAL, (60, 60, 255)))

            Globals.objects.append(Entities.SpriteLine(self.rigidBody.position[0] + self.autoCollisionsDetails[i].collisionPointObject1[0],
                                                       self.rigidBody.position[1] + self.autoCollisionsDetails[i].collisionPointObject1[1],
                                                       self.rigidBody.position[0] + self.autoCollisionsDetails[i].collisionPointObject1[0] + self.autoCollisionsDetails[i].reactionVectorObject1[0], 
                                                       self.rigidBody.position[1] + self.autoCollisionsDetails[i].collisionPointObject1[1] + self.autoCollisionsDetails[i].reactionVectorObject1[1], 
                                                       Physics.Materials.METAL, (200, 30, 30)))


            Globals.objects.append(Entities.SpriteCircle(other.rigidBody.position[0] + self.autoCollisionsDetails[i].collisionPointObject2[0], 
                                                         other.rigidBody.position[1] + self.autoCollisionsDetails[i].collisionPointObject2[1], 
                                                         5, Physics.Materials.METAL, (60, 60, 255)))

            Globals.objects.append(Entities.SpriteLine(other.rigidBody.position[0] + self.autoCollisionsDetails[i].collisionPointObject2[0],
                                                       other.rigidBody.position[1] + self.autoCollisionsDetails[i].collisionPointObject2[1],
                                                       other.rigidBody.position[0] + self.autoCollisionsDetails[i].collisionPointObject2[0] + self.autoCollisionsDetails[i].reactionVectorObject2[0], 
                                                       other.rigidBody.position[1] + self.autoCollisionsDetails[i].collisionPointObject2[1] + self.autoCollisionsDetails[i].reactionVectorObject2[1], 
                                                       Physics.Materials.METAL, (200, 30, 30)))

            reactionVector = self.autoCollisionsDetails[i].reactionVectorObject1 / np.linalg.norm(self.autoCollisionsDetails[i].reactionVectorObject1)

            
            self.rigidBody.position += self.autoCollisionsDetails[i].reactionVectorObject1

            if other.rigidBody.type == "static":
                self.rigidBody.velocity = self.rigidBody.velocity - 1.5 * (np.dot(self.rigidBody.velocity, reactionVector)) * reactionVector


            elif other.rigidBody.type == "dynamic":            
                self.rigidBody.velocity = (((self.rigidBody.mass * self.rigidBody.previousVelocity) + 
                                            (other.rigidBody.mass * other.rigidBody.previousVelocity) + 
                                            (other.rigidBody.mass * 0.8 * (other.rigidBody.previousVelocity - self.rigidBody.previousVelocity))) / 
                                            (self.rigidBody.mass + other.rigidBody.mass))