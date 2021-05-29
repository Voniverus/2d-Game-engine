import numpy as np

import Physics
import Sprite
import Collider
import Globals


class Camera:
    def __init__(self, name, position, width, height, scale):
        self.name = name
        self.id = Globals.getLastUsedID()
        
        self.rigidBody = Physics.RigidBodyStatic(position - np.array([width / 2.0, height / 2.0]), Physics.Materials.PLAYER)

        self.width = width
        self.height = height
        self.scale = scale


    def updatePosition(self, x, y):
        self.rigidBody.position[0] = x * self.scale - self.width / 2.0 
        self.rigidBody.position[1] = y * self.scale - self.height / 2.0 

    def updateScale(self, scale):
        self.scale = scale
        
        

class StaticPoly:
    def __init__(self, name, points, position, material, color, tags):
        self.name = name
        self.shape = "poly"
        self.temp = False
        self.id = Globals.getLastUsedID()

        self.rigidBody = Physics.RigidBodyStatic(position, material)
        self.collider = Collider.Polygon(self.rigidBody, points, tags)
        self.sprite = Sprite.Polygon(points, color)

class DynamicPoly:
    def __init__(self, name, points, position, material, color, mass, drag, tags):
        self.name = name
        self.shape = "poly"
        self.temp = False
        self.id = Globals.getLastUsedID()
        
        self.rigidBody = Physics.RigidBody(position, material, mass, drag)
        self.collider = Collider.Polygon(self.rigidBody, points, tags)
        self.sprite = Sprite.Polygon(points, color)

    def movement(self, deltaTime):
        self.rigidBody.previousVelocity = self.rigidBody.velocity
        self.rigidBody.position += self.rigidBody.velocity * deltaTime 
        
class StaticCircle:
    def __init__(self, name, x, y, radius, material, color, tags):
        self.name = name
        self.shape = "circle"
        self.temp = False
        self.id = Globals.getLastUsedID()

        self.rigidBody = Physics.RigidBodyStatic(np.array([x, y]), material)
        self.collider = Collider.Circle(self.rigidBody, radius, tags)
        self.sprite = Sprite.Circle(radius, color)
        self.color = color

class DynamicCircle:
    def __init__(self, name, position, radius, material, color, mass, drag, tags):
        self.name = name
        self.shape = "circle"
        self.temp = False
        self.id = Globals.getLastUsedID()
        
        self.rigidBody = Physics.RigidBody(position, material, mass, drag)
        self.collider = Collider.Circle(self.rigidBody, radius, tags)
        self.sprite = Sprite.Circle(radius, color)
        self.color = color

    def movement(self, deltaTime):
        self.rigidBody.previousVelocity = self.rigidBody.velocity
        self.rigidBody.position += self.rigidBody.velocity * deltaTime 

class CollisionPoly:
    def __init__(self, position, points, material, tags):
        self.shape = "poly"

        self.rigidBody = Physics.RigidBodyStatic(position, material)
        self.collider = Collider.Polygon(self.rigidBody, points, tags)

    

class CollisionCircle:
    def __init__(self, x, y, radius, material, tags):
        self.shape = "circle"

        self.rigidBody = Physics.RigidBodyStatic(np.array([x, y]), material)
        self.collider = Collider.Circle(self.rigidBody, radius, tags)
        self.radius = radius


class CollisionLine:
    def __init__(self, x1, y1, x2, y2, material):
        self.shape = "line"

        self.rigidBody = Physics.RigidBodyStatic(np.array([x2 - x1, y2 - y1]), material)
        self.start = np.array([x1, y1])
        self.end = np.array([x2, y2])

class SpritePoly:
    def __init__(self, position, points, material, color):
        self.shape = "poly"
        self.temp = True

        self.rigidBody = Physics.RigidBodyStatic(position, material)
        self.sprite = Sprite.Polygon(points, color)

class SpriteCircle:
    def __init__(self, x, y, radius, material, color):
        self.shape = "circle"
        self.temp = True

        self.rigidBody = Physics.RigidBodyStatic(np.array([x, y]), material)
        self.sprite = Sprite.Circle(radius, color)
        self.radius = radius


class SpriteLine:
    def __init__(self, x1, y1, x2, y2, material, color):
        self.shape = "line"
        self.temp = True

        self.rigidBody = Physics.RigidBodyStatic(np.array([x2 - x1, y2 - y1]), material)
        self.start = np.array([x1, y1])
        self.end = np.array([x2, y2])
        self.color = color