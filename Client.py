"""Example game client"""

import pygame
import pygame.locals
from twisted.internet import protocol, reactor, endpoints

import numpy as np

import Globals
import Spawner
import Entities
import Network
import objectParser

class Client:
    def __init__(self, w, h):
        pygame.init()
        Globals.init()
        
        self.net = Network.Network()

        self.width = w
        self.height = h
        self.display = pygame.display.set_mode((w, h))
        pygame.display.set_caption('Physics based platformer client')

        self.camera = Entities.Camera("main camera", np.array([0, 0]), 600, 400, 1.0)

        self.playerObjects = []


    def run(self):
        # Spawn objects
        Spawner.init()
        clientPlayer = Spawner.createPlayer()

        print("Connection id: {}".format(self.net.id))

        # Start the actual main loop.
        game_loop_is_running = True
        while game_loop_is_running:
            clientPlayer.input(pygame.event.get(), pygame.mouse.get_pos())


            # Send Network Stuff
            self.playerObjects = self.send_data(clientPlayer)

            self.camera.updatePosition(self.playerObjects[int(self.net.id)][1][0], self.playerObjects[int(self.net.id)][1][1])

            # Draw objects
            self.display.fill((0, 0, 0))

            for obj in Spawner.init():
                pygame.draw.polygon(self.display, obj.sprite.color, [(x + obj.rigidBody.position) * self.camera.scale - self.camera.rigidBody.position for x in obj.sprite.points], 2)


            for player in self.playerObjects:
                pygame.draw.polygon(self.display, player[3], [(player[1] + np.array(x)) * self.camera.scale - self.camera.rigidBody.position for x in player[2]], 2)

            pygame.display.flip()
            
            
        # Clean up.
        pygame.quit()


    def send_data(self, player):
        """Send position to server :return: None"""

        data = "{}:{}:{}:{}".format(self.net.id, player.direction.tolist(), [player.mouseX, player.mouseY], int(player.primaryFire))



        reply = objectParser.parseObject(self.net.send(data))



        return reply

