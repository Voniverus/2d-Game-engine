import math
import random

import numpy as np

import Globals
import Physics
import Sprite



class ParticlePriciple:
    def __init__(self):
        self.particles = []

    def emit(self, deltaTime):
        if self.particles:
            self.deleteParticles()
            for particle in self.particles:
                particle.rigidBody.position += particle.direction * particle.speed * deltaTime

    def addParticle(self, x, y, direction, force):
        particle = Particle(np.array([x, y]), direction, force, 5, (random.uniform(255, 255), random.uniform(255, 255), random.uniform(255, 255)))
        self.particles.append(particle)
        Globals.objects.append(particle)

    def deleteParticles(self):
        particlesCopy = [particle for particle in self.particles if(0 <= particle.rigidBody.position[0] <= 600 and 0 <= particle.rigidBody.position[1] <= 400)]
        for particle in self.particles:
            if particle not in particlesCopy:
                Globals.objects.remove(particle)

        self.particles = particlesCopy
    

class Particle:
    def __init__(self, position, direction, speed, radius, color):
        self.shape = "circle"
        self.temp = False

        self.rigidBody = Physics.RigidBodyStatic(position)
        self.direction = direction / np.linalg.norm(direction)
        self.speed = speed
        self.sprite = Sprite.Circle(position, radius, color)

        
        
        