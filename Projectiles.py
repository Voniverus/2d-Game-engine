import math
import random

import numpy as np

import Globals
import Entities
import Collider


class ProjectilePriciple:
    def __init__(self):
        self.projectiles = []

    def emit(self, deltaTime):
        if self.projectiles:
            self.deleteProjectile()
            for projectile in self.projectiles:
                projectile.base.rigidBody.position += projectile.base.rigidBody.velocity * deltaTime


    def addProjectile(self, x, y, direction, speed):
        projectile = Projectile(np.array([x, y]), direction, speed, 5, (random.uniform(255, 255), random.uniform(255, 255), random.uniform(255, 255)))
        self.projectiles.append(projectile)
        Globals.objects.append(projectile.base)
        Globals.gameObjects.append(projectile.base)

    def deleteProjectile(self):
        projectilesCopy = [projectile for projectile in self.projectiles if(True)]
        for projectile in self.projectiles:
            if projectile not in projectilesCopy:
                Globals.objects.remove(projectile.base)
                Globals.gameObjects.remove(projectile.base)

        self.projectiles = projectilesCopy
    

class Projectile:
    def __init__(self, position, direction, speed, radius, color):
        self.shape = "circle"
        self.temp = False
        # self.base = Entities.DynamicPoly()
        self.base = Entities.DynamicCircle("Bullet", position, radius, color, 10, np.array([0.005, 0.005]), Collider.Tag.PLAYER_PROJECTILE)
        direction /= np.linalg.norm(direction)
        self.direction = direction / np.linalg.norm(direction)
        self.speed = speed
        self.base.rigidBody.velocity = direction * speed

        
        
        