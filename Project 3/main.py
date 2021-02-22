# Rural Jay Young III
# Implementation of ARA* in a tile-based structure
# Utilizing the video provided by: https://youtu.be/3UxnelT9aCo

import pygame as pg
import sys
import random
import math
import time

import settings
from settings import *
from sprites import *

# stuff to measure how long it runs

class Game:
    knownWalls = []
    wallBlocks = []
    tempFastestRoute = []
    fastestRoute = []
    visited = []
    width = 0
    height = 0
    

    def __init__(self, size):
        pg.init()
        eightSize = size * 4 #to account for the 8 bit
        self.height = eightSize
        self.width = eightSize
        self.screen = pg.display.set_mode((self.height, self.width))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(400, 100)
        self.load_data()
        self.wallBlocks = [(0, 0), (size-1, size-1)]

    def load_data(self):
        pass

    def new(self, size, obstacle):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.player = Player(self, 0, 0)
        self.finish = Finish(self, size-1, size-1)
        obstacle = obstacle * .01
        obstacle = (size * size) * obstacle


        for x in range(int(obstacle)):
            randx, randy = random.randint(0, size-1), random.randint(0, size-1)
            if (randx, randy) not in self.wallBlocks: # and (randx, randy) not in self.knownWalls:
                Wall(self, randx, randy)
                self.knownWalls.append((randx, randy))
            #else:
            #    while (randx, randy) in self.wallBlocks or (randx, randy) in self.knownWalls:
            #        randx, randy = random.randint(0, size - 1), random.randint(0, size - 1)
            #        if (randx, randy) == (0, 0) or (randx, randy) == (size-1, size-1):
            #            break
            #    Wall(self, randx, randy)
            #    self.knownWalls.append((randx, randy))

    def run(self, size):
        # game loop - set self.playing = False to end the game
        self.playing = True

        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            for x in self.fastestRoute:
                Path(self, x[0], x[1])
            Player(self, 0, 0)
            Finish(self, size-1, size-1)
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, self.width, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, self.height))
        for y in range(0, self.height, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (self.width, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    def distance(self, a, b):
        x1, y1 = a[0], a[1]
        x2, y2 = b[0], b[1]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def wallCheck(self, x, y): # POTENTIAL ERROR SPOT
        if (x, y) in self.knownWalls:
            return True
        else:
            return False

    def getNeighbors(self, currentx, currenty, size):
        neighbors = []

        # Initially did Elif's ubut this won't work
        #Checking Above
        if currenty+1 <= size-1 and not self.wallCheck(currentx, currenty+1):
            neighbors.append((currentx, currenty+1))

        #Checking Below
        if currenty-1 >= 0 and not self.wallCheck(currentx, currenty-1):
            neighbors.append((currentx, currenty-1))

        #Checking Right
        if currentx+1 <= size-1 and not self.wallCheck(currentx+1, currenty):
            neighbors.append((currentx+1, currenty))

        #Checking Left
        if currentx-1 >= 0 and not self.wallCheck(currentx-1, currenty):
            neighbors.append((currentx-1, currenty))

        return neighbors

    def astar(self, weight, size):
        # format should be fcost and gcost
        open = {(0, 0): (self.distance((0, 0), (size-1, size-1)), 0)}
        closed = {}
        path = {(0, 0): (0, 0)}
        fastestRoute = []
        sizeX = size-1
        sizeY = size-1

        while open:
            # finds the lowest G cost
            current = min(open, key=lambda key: open[key][0])
            (fcurrent, gcurrent) = open[current]
            currentx, currenty = current[0], current[1]



            # checks to se if we are at the final node
            if current == (sizeX, sizeY):
                print(f"We have reached the goal with a gcost of {gcurrent}!")

                while path[current] != current:
                    fastestRoute.append(current)
                    current = path[current]

                # reverse and then re-add the start
                fastestRoute = fastestRoute[::-1]
                fastestRoute.insert(0, (0, 0))

                self.tempFastestRoute = fastestRoute
                self.visited = closed
                return gcurrent

            pathways = self.getNeighbors(currentx, currenty, size)
            for neighbor in pathways:

                tempNeighborGCost = gcurrent + (self.distance(current, neighbor))

                if neighbor not in open and neighbor not in closed:
                    # Neighbor gets added into open with (fcost(gcost+Hcost), Gcost)
                    open[neighbor] = (tempNeighborGCost + (weight * self.distance(neighbor, (sizeX, sizeY))), tempNeighborGCost)
                    path[neighbor] = current

                else:
                    try:
                        if neighbor in open:
                            neighborGcost = open[neighbor][1]
                            if neighborGcost > tempNeighborGCost:
                                del open[neighbor]
                                open[neighbor] = (
                                tempNeighborGCost + (weight * self.distance(neighbor, (sizeX, sizeY))), tempNeighborGCost)
                                path[neighbor] = current
                    except:
                        pass

                    try:
                        if neighbor in closed:
                            neighborGcost = open[neighbor][1]
                            if neighborGcost > tempNeighborGCost:
                                del open[neighbor]
                                open[neighbor] = (
                                    tempNeighborGCost + (weight * self.distance(neighbor, (sizeX, sizeY))), tempNeighborGCost)
                                path[neighbor] = current
                    except KeyError:
                        pass

            del open[current]
            closed[current] = (fcurrent, gcurrent)
        # If it doesn't find anything, Return an error.
        print("Error: Could not find path")
        return math.inf

    def arastar(self, weight, size):
        currentPathCost = math.inf
        counter = 1
        while weight >= 2:

            print(f"\nAttempting AStar with inflation of x{weight}")
            astarTime = time.time()
            tempPathCost = self.astar(weight, size)
            print(f"Run time for run {counter}: %s" % (time.time() - astarTime))

            if tempPathCost < currentPathCost:
                currentPathCost = tempPathCost
                print("ARASTAR Has found a new path")
                self.fastestRoute = self.tempFastestRoute

            weight = weight - 1
            counter += 1


print("WARNING! Any map size exceeding 200 will experience a slowdown! Please be patient!")
obstacle = int(input("Please choose what percentage of the screen you would like to be obstacles? (Just input a number, no '%'): "))
while obstacle > 100:
    obstacle = int(input("Error, percentage exceeds 100%, please input a lower percentage: "))
size = int(input("please input the size of the map: "))


# create the game object
weight = 5
g = Game(size)
g.show_start_screen()


while True:
    g.new(size, obstacle)
    startTime = time.time()
    g.arastar(weight, size)
    print("\nRun time for entire ARASTAR: %s" % (time.time() - startTime))
    g.run(size)



























