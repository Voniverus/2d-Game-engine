import socket
import _thread as thread
import logging

import numpy as np
import pygame

import Spawner
import Globals
import Game
import objectParser


logging.basicConfig(
    format  = '%(asctime)s %(levelname)-8s %(message)s',
    level   = logging.INFO,
    datefmt = '%Y-%m-%d %H:%M:%S')


SERVER = ""
PORT = 5555

SERVER_IP = socket.gethostbyname(SERVER)


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    socket.bind((SERVER, PORT))

except socket.error as e:
    print(str(e))

socket.listen(2)

print("[SERVER] Waiting for connection.")


running = False

currentId = 0
Globals.init()
Globals.gameObjects = []
playerObjects = []
Globals.gameObjects.extend(Spawner.init())


def run():
    clock = pygame.time.Clock()
    time = 0.

    while running:

        deltaTime = time / 1000.0

        Game.update(Globals.gameObjects, playerObjects, deltaTime)
        
        time = clock.tick(Globals.frameRate)


def threaded_client(connection):
    global currentId, pos, running

    reply = ''

    connection.send(str.encode(str(currentId)))

    currentId += 1

    player = Spawner.createPlayer()

    Globals.gameObjects.append(player)
    playerObjects.append(player)


    while True:
        try:
            data = connection.recv(131072)
            reply = data.decode('utf-8')

            if not data:
                print("No data")
                running = False
                break

            else:
                # print("Recieved: " + reply)

                object = objectParser.parseClientData(reply)

                id = int(object[0])


                playerObjects[id].direction = np.array(object[1])

                playerObjects[id].mouseX = object[1][0]
                playerObjects[id].mouseY = object[1][1]


                if object[3]:
                    playerObjects[id].projectiles.addProjectile(playerObjects[id].rigidBody.position[0], 
                                                            playerObjects[id].rigidBody.position[1], 
                                                            np.array([-playerObjects[id].rigidBody.position[0] + playerObjects[id].mouseX,
                                                                      -playerObjects[id].rigidBody.position[1] + playerObjects[id].mouseY]), 500.0)



                reply = ""
                
                for player in playerObjects:
                    reply += "{}:{}:{}:{}|".format(id, player.rigidBody.position.tolist(), player.collider.points.tolist(), player.sprite.color)


                # print("Sending:  " + reply)

            

            connection.sendall(str.encode(reply))

        except:
            print("Exception")
            break

    print("Connection Closed")
    connection.close()


while True:
    connection, address = socket.accept()
    print("Connected to: ", address)

    thread.start_new_thread(threaded_client, (connection,))
    
    if not running:
        running = True
        thread.start_new_thread(run, ())