import numpy as np

import Physics
import Sprite
import Collider
import Globals


class Camera:
    def __init__(self, name, position, width, height):
        self.name = name
        self.id = Globals.getLastUsedID()
        
        self.rigidBody = Physics.RigidBodyStatic(position - np.array([width / 2.0, height / 2.0]))

        self.width = width
        self.height = height


    def updatePosition(self, x, y):
        self.rigidBody.position[0] = x - self.width / 2.0
        self.rigidBody.position[1] = y - self.height / 2.0

        
        

class StaticPoly:
    def __init__(self, name, points, position, color, tags):
        self.name = name
        self.shape = "poly"
        self.temp = False
        self.id = Globals.getLastUsedID()

        self.rigidBody = Physics.RigidBodyStatic(position)
        self.collider = Collider.Polygon(self.rigidBody, points, tags)
        self.sprite = Sprite.Polygon(points, color)

class DynamicPoly:
    def __init__(self, name, points, position, color, mass, drag, tags):
        self.name = name
        self.shape = "poly"
        self.temp = False
        self.id = Globals.getLastUsedID()
        
        self.rigidBody = Physics.RigidBody(position, mass, drag)
        self.collider = Collider.Polygon(self.rigidBody, points, tags)
        self.sprite = Sprite.Polygon(points, color)
        
class StaticCircle:
    def __init__(self, name, x, y, radius, color, tags):
        self.name = name
        self.shape = "circle"
        self.temp = False
        self.id = Globals.getLastUsedID()

        self.rigidBody = Physics.RigidBodyStatic(np.array([x, y]))
        self.collider = Collider.Circle(self.rigidBody, radius, tags)
        self.sprite = Sprite.Circle(radius, color)
        self.color = color

class DynamicCircle:
    def __init__(self, name, position, radius, color, mass, drag, tags):
        self.name = name
        self.shape = "circle"
        self.temp = False
        self.id = Globals.getLastUsedID()
        
        self.rigidBody = Physics.RigidBody(position, mass, drag)
        self.collider = Collider.Circle(self.rigidBody, radius, tags)
        self.sprite = Sprite.Circle(radius, color)
        self.color = color

class CollisionPoly:
    def __init__(self, position, points, tags):
        self.shape = "poly"

        self.rigidBody = Physics.RigidBodyStatic(position)
        self.collider = Collider.Polygon(self.rigidBody, points, tags)

class CollisionCircle:
    def __init__(self, x, y, radius, tags):
        self.shape = "circle"

        self.rigidBody = Physics.RigidBodyStatic(np.array([x, y]))
        self.collider = Collider.Circle(self.rigidBody, radius, tags)
        self.radius = radius


class CollisionLine:
    def __init__(self, x1, y1, x2, y2, color):
        self.shape = "line"

        self.rigidBody = Physics.RigidBodyStatic(np.array([x2 - x1, y2 - y1]))
        self.start = np.array([x1, y1])
        self.end = np.array([x2, y2])

class SpritePoly:
    def __init__(self, position, points, color):
        self.shape = "poly"
        self.temp = True

        self.rigidBody = Physics.RigidBodyStatic(position)
        self.sprite = Sprite.Polygon(points, color)

class SpriteCircle:
    def __init__(self, x, y, radius, color):
        self.shape = "circle"
        self.temp = True

        self.rigidBody = Physics.RigidBodyStatic(np.array([x, y]))
        self.sprite = Sprite.Circle(radius, color)
        self.radius = radius


class SpriteLine:
    def __init__(self, x1, y1, x2, y2, color):
        self.shape = "line"
        self.temp = True

        self.rigidBody = Physics.RigidBodyStatic(np.array([x2 - x1, y2 - y1]))
        self.start = np.array([x1, y1])
        self.end = np.array([x2, y2])
        self.color = color