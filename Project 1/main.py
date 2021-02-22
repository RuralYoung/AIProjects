import pygame
import sys
import math

# Initialization
pygame.init()

# Creating the windows
surface = pygame.display.set_mode((700, 400))  # X * 20 and [400 - (Y * 20)]
game = False

# distance function all the way up here because everything below requires it
def distance(a, b):
    x1, y1 = a[0], a[1]
    x2, y2 = b[0], b[1]

    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Start and Finish:
start = (20, 340)
finish = (680, 20)

# Rectangle 1 (LL, UL, UR, LR) ([L=Lower U=Upper][L=Left R=Right])
Re1 = (40, 380)
Re2 = (40, 280)
Re3 = (340, 280)
Re4 = (340, 380)

# Pentagon (SW, W, N, E, SE) (Compass Style)
Pe1 = (20, 220)
Pe2 = (0, 120)
Pe3 = (120, 20)
Pe4 = (180, 100)
Pe5 = (140, 240)

# Triangle 1 (LL, U, LR) ([L=Lower U=Upper][L=Left R=Right])
Tr1 = (200, 240)
Tr2 = (240, 100)
Tr3 = (280, 240)

# 4 Point Polygon (LL, UL, UR, LR) ([L=Lower U=Upper][L=Left R=Right])
Po1 = (280, 140)
Po2 = (280, 20)
Po3 = (360, 0)
Po4 = (400, 60)

# Triangle 2 (S, NW, E)
Tr4 = (380, 340)
Tr5 = (360, 200)
Tr6 = (460, 280)

# Rectangle 2 (LL, UL, UR, LR) ([L=Lower U=Upper][L=Left R=Right])
Re5 = (440, 220)
Re6 = (440, 20)
Re7 = (560, 20)
Re8 = (560, 220)

# Hexagon (S, SW, NW, N, NE, SE) (Compass Style)
He1 = (560, 380)
He2 = (500, 360)
He3 = (500, 280)
He4 = (580, 240)
He5 = (620, 280)
He6 = (620, 360)

# Diamond (S, W, N, E) (Compass Style)
Di1 = (640, 240)
Di2 = (580, 60)
Di3 = (620, 20)
Di4 = (680, 80)

pathways = {
    # path then shortest path from the current node
    # Rectangle 1
    Re1: [(Re4, distance(Re1, Re4)), (Re2, distance(Re1, Re2)), (Pe1, distance(Re1, Pe1)), (Pe2, distance(Re1, Pe2))],
    Re2: [(Re1, distance(Re2, Re1)), (Re3, distance(Re2, Re3)), (Tr3, distance(Re2, Tr3)), (Tr1, distance(Re2, Tr1)), (Pe5, distance(Re2, Pe5)), (Pe1, distance(Re2, Pe1))],
    Re3: [(Re4, distance(Re3, Re4)), (Tr4, distance(Re3, Tr4)), (Tr5, distance(Re3, Tr5)), (Po1, distance(Re3, Po1)), (Tr2, distance(Re3, Tr2)), (Tr3, distance(Re3, Tr3)), (Tr1, distance(Re3, Tr1)), (Pe5, distance(Re3, Pe5)), (Re2, distance(Re3, Re2))],
    Re4: [(He1, distance(Re4, He1)), (He2, distance(Re4, He2)), (He3, distance(Re4, He3)), (Re8, distance(Re4, Re8)), (Tr4, distance(Re4, Tr4)), (Tr5, distance(Re4, Tr5)), (Re3, distance(Re4, Re3)), (Re1, distance(Re4, Re1))],

    # Pentagon
    Pe1: [(Re1, distance(Pe1, Re1)), (Re2, distance(Pe1, Re2)), (Pe5, distance(Pe1, Pe5)), (Pe2, distance(Pe1, Pe2))],
    Pe2: [(Re1, distance(Pe2, Re1)), (Pe1, distance(Pe2, Pe1)), (Pe3, distance(Pe2, Pe3))],
    Pe3: [(Pe4, distance(Pe3, Pe4)), (Tr2, distance(Pe3, Tr2)), (Po2, distance(Pe3, Po2)), (Pe2, distance(Pe3, Pe2))],
    Pe4: [(Tr1, distance(Pe4, Tr1)), (Tr2, distance(Pe4, Tr2)), (Po2, distance(Pe4, Po2)), (Pe3, distance(Pe4, Pe3)), (Pe5, distance(Pe4, Pe5))],
    Pe5: [(Re3, distance(Pe5, Re3)), (Tr1, distance(Pe5, Tr1)), (Tr2, distance(Pe5, Tr2)), (Pe4, distance(Pe5, Pe4)), (Pe1, distance(Pe5, Pe1)), (Re2, distance(Pe5, Re2))],

    # Triangle 1
    Tr1: [(Re3, distance(Tr1, Re3)), (Tr3, distance(Tr1, Tr3)), (Tr2, distance(Tr1, Tr2)), (Pe4, distance(Tr1, Pe4)), (Pe5, distance(Tr1, Pe5)), (Re2, distance(Tr1, Re2))],
    Tr2: [(Tr3, distance(Tr2, Tr3)), (Po1, distance(Tr2, Po1)), (Po2, distance(Tr2, Po2)), (Pe3, distance(Tr2, Pe3)), (Pe4, distance(Tr2, Pe4)), (Pe5, distance(Tr2, Pe5)), (Tr1, distance(Tr2, Tr1))],
    Tr3: [(Re3, distance(Tr3, Re3)), (Tr5, distance(Tr3, Tr5)), (Po4, distance(Tr3, Po4)), (Po1, distance(Tr3, Po1)), (Tr2, distance(Tr3, Tr2)), (Tr1, distance(Tr3, Tr1)), (Re2, distance(Tr3, Re2))],

    # 4 Point Polygon
    Po1: [(Re3, distance(Po1, Re3)), (Tr4, distance(Po1, Tr4)), (Tr5, distance(Po1, Tr5)), (Re5, distance(Po1, Re5)), (Po4, distance(Po1, Po4)), (Po2, distance(Po1, Po2)), (Tr2, distance(Po1, Tr2)), (Tr3, distance(Po1, Tr3))],
    Po2: [(Po1, distance(Po2, Po1)), (Po3, distance(Po2, Po3)), (Pe3, distance(Po2, Pe3)), (Pe4, distance(Po2, Pe4)), (Tr2, distance(Po2, Tr2))],
    Po3: [(Po4, distance(Po3, Po4)), (Re6, distance(Po3, Re6)), (Re7, distance(Po3, Re7)), (Di3, distance(Po3, Di3)), (Pe3, distance(Po3, Pe3)), (Po2, distance(Po3, Po2)), (finish, distance(Po3, finish))],
    Po4: [(Re5, distance(Po4, Re5)), (Re6, distance(Po4, Re6)), (Po3, distance(Po4, Po3)), (Po1, distance(Po4, Po1)), (Tr3, distance(Po4, Tr3)), (Tr5, distance(Po4, Tr5))],

    # Triangle 2
    Tr4: [(He1, distance(Tr4, He1)), (He2, distance(Tr4, He2)), (He3, distance(Tr4, He3)), (He4, distance(Tr4, He4)), (Re8, distance(Tr4, Re8)), (Tr6, distance(Tr4, Tr6)), (Tr5, distance(Tr4, Tr5)), (Po1, distance(Tr4, Po1)), (Tr2, distance(Tr4, Tr2)), (Re3, distance(Tr4, Re3)), (Re4, distance(Tr4, Re4))],
    Tr5: [(Tr4, distance(Tr5, Tr4)), (Tr6, distance(Tr5, Tr6)), (He3, distance(Tr5, He3)), (Re5, distance(Tr5, Re5)), (Re6, distance(Tr5, Re6)), (Po4, distance(Tr5, Po4)), (Po1, distance(Tr5, Po1)), (Tr3, distance(Tr5, Tr3)), (Re3, distance(Tr5, Re3)), (Re4, distance(Tr5, Re4))],
    Tr6: [(He2, distance(Tr6, He2)), (He3, distance(Tr6, He3)), (He4, distance(Tr6, He4)), (Re8, distance(Tr6, Re8)), (Re5, distance(Tr6, Re5)), (Tr5, distance(Tr6, Tr5)), (Tr4, distance(Tr6, Tr4))],

    # Rectangle 5
    Re5: [(Tr6, distance(Re5, Tr6)), (He2, distance(Re5, He2)), (He3, distance(Re5, He3)), (He4, distance(Re5, He4)), (Re8, distance(Re5, Re8)), (Re6, distance(Re5, Re6)), (Po4, distance(Re5, Po4)), (Po1, distance(Re5, Po1)), (Tr5, distance(Re5, Tr5))],
    Re6: [(Re5, distance(Re6, Re5)), (Re7, distance(Re6, Re7)), (Po3, distance(Re6, Po3)), (Po4, distance(Re6, Po4)), (Tr5, distance(Re6, Tr5))],
    Re7: [(Re8, distance(Re7, Re8)), (He4, distance(Re7, He4)), (He5, distance(Re7, He5)), (Di2, distance(Re7, Di2)), (Di3, distance(Re7, Di3)), (Po3, distance(Re7, Po3)), (Re6, distance(Re7, Re6))],
    Re8: [(He4, distance(Re8, He4)), (Di1, distance(Re8, Di1)), (Di2, distance(Re8, Di2)), (Re7, distance(Re8, Re7)), (Re5, distance(Re8, Re5)), (Tr6, distance(Re8, Tr6)), (Tr4, distance(Re8, Tr4)), (Re4, distance(Re8, Re4)), (He3, distance(Re8, He3))],

    # Hexagon
    He1: [(He6, distance(He1, He6)), (He2, distance(He1, He2)), (Tr4, distance(He1, Tr4)), (Re4, distance(He1, Re4))],
    He2: [(He1, distance(He2, He1)), (He3, distance(He2, He3)), (Re5, distance(He2, Re5)), (Tr6, distance(He2, Tr6)), (Tr4, distance(He2, Tr4)), (Re4, distance(He2, Re4))],
    He3: [(He2, distance(He3, He2)), (He4, distance(He3, He4)), (Re8, distance(He3, Re8)), (Re5, distance(He3, Re5)), (Tr5, distance(He3, Tr5)), (Tr6, distance(He3, Tr6)), (Tr4, distance(He3, Tr4)), (Re4, distance(He3, Re4))],
    He4: [(He5, distance(He4, He5)), (Di1, distance(He4, Di1)), (Di2, distance(He4, Di2)), (Re7, distance(He4, Re7)), (Re8, distance(He4, Re8)), (Re5, distance(He4, Re5)), (Tr6, distance(He4, Tr6)), (He3, distance(He4, He3))],
    He5: [(He6, distance(He5, He6)), (Di1, distance(He5, Di1)), (Di2, distance(He5, Di2)), (Re7, distance(He5, Re7)), (He4, distance(He5, He4))],
    He6: [(Di1, distance(He6, Di1)), (He5, distance(He6, He5)), (He1, distance(He6, He1))],

    # Diamond
    Di1: [(finish, distance(Di1, finish)), (Di4, distance(Di1, Di4)), (Di2, distance(Di1, Di2)), (Re8, distance(Di1, Re8)), (He4, distance(Di1, He4)), (He5, distance(Di1, He5)), (He6, distance(Di1, He5))],
    Di2: [(He4, distance(Di2, He4)), (He5, distance(Di2, He5)), (Di1, distance(Di2, Di1)), (Di3, distance(Di2, Di3)), (Re7, distance(Di2, Re7)), (Re8, distance(Di2, Re8))],
    Di3: [(Di4, distance(Di3, Di4)), (finish, distance(Di3, finish)), (Re7, distance(Di3, Re7)), (Di2, distance(Di3, Di2))],
    Di4: [(finish, distance(Di4, finish)), (Di3, distance(Di4, Di3)), (Di1, distance(Di4, Di1))],

    # Misc.
    start: [(Re1, distance(start, Re1)), (Re2, distance(start, Re2)), (Pe1, distance(start, Pe1)), (Pe2, distance(start, Pe2))]
}

def shapes():
    # Rectangle 1
    pygame.draw.polygon(surface, black, [Re1, Re2, Re3, Re4], 1)

    # Pentagon
    pygame.draw.polygon(surface, black, [Pe1, Pe2, Pe3, Pe4, Pe5], 1)

    # Triangle 1
    pygame.draw.polygon(surface, black, [Tr1, Tr2, Tr3], 1)

    # 4 Point Polygon
    pygame.draw.polygon(surface, black, [Po1, Po2, Po3, Po4], 1)

    # Triangle 2
    pygame.draw.polygon(surface, black, [Tr4, Tr5, Tr6], 1)

    # Rectangle 2
    pygame.draw.polygon(surface, black, [Re5, Re6, Re7, Re8], 1)

    # Hexagon
    pygame.draw.polygon(surface, black, [He1, He2, He3, He4, He5, He6], 1)

    # Diamond
    pygame.draw.polygon(surface, black, [Di1, Di2, Di3, Di4], 1)


def f(node, start, finish):
    return distance(start, node) + distance(node, finish)


def astar(start, finish):
    # format should be fcost and gcost
    open = {start: (distance(start, finish), 0)}
    closed = {}
    path = {start: start}
    fastestRoute = []

    while open:
        # finds the lowest G cost
        current = min(open, key=lambda key: open[key][0])
        (fcurrent, gcurrent) = open[current]

        # Used this to troubleshoot/know which node we're evaluating
        print(f"\nCurrent is now: {current}")
        print(f"F: {fcurrent} and G: {gcurrent}\n")

        # checks to se if we are at the final node
        if current == finish:
            print("We have reached the goal!")

            while path[current] != current:
                fastestRoute.append(current)
                current = path[current]

            # reverse and then re-add the start
            fastestRoute = fastestRoute[::-1]
            fastestRoute.insert(0, start)

            return fastestRoute

        # checks the "neighbors" of each current node (the potential candidates)
        for neighbor in pathways[current]:
            # neighbor has (node, distance/weight)
            # I did this for my sake of sanity
            neighborNode = neighbor[0]
            neighborWeight = neighbor[1]
            tempNeighborGCost = gcurrent + neighborWeight

            # since there isn't anything in either open or closed, we add it into open
            if neighborNode not in open and neighborNode not in closed:
                # neighbor gets added into open with (Fcost(Gcost+Hcost), Gcost)
                print("Node does not appear in open or closed, adding to open")
                open[neighborNode] = (tempNeighborGCost + distance(neighborNode, finish), tempNeighborGCost)
                path[neighborNode] = current

            # This code is ugly but essentially it checks to see if there is a lower G cost and then
            # adds it back into the open if there is one found.
            else:
                try:
                    if neighborNode in open:
                        neighborGcost = open[neighbor][1]
                        print("Neighbor was found in open!")
                        # open -> neighbor node -> y(gcost)
                        if neighborGcost > tempNeighborGCost:
                            print("The new Gcost is cheaper, editing open/path")
                            del open[neighborNode]
                            open[neighborNode] = (tempNeighborGCost + distance(neighborNode, finish), tempNeighborGCost)
                            path[neighborNode] = current

                except KeyError:
                    print("Catched! not in open")

                try:
                    if neighborNode in closed:
                        neighborGcost = open[neighbor][1]
                        print("Neighbor was found in closed!")
                        if neighborGcost > tempNeighborGCost:
                            print("The new Gcost is cheaper, adding to open/path")
                            del closed[neighborNode]
                            open[neighborNode] = (tempNeighborGCost + distance(neighborNode, finish), tempNeighborGCost)
                            path[neighborNode] = current

                except KeyError:
                    print("Catched! not in closed!")
        # closes out anything that we've already exhausted
        del open[current]
        closed[current] = (fcurrent, gcurrent)
    # If it doesn't find anything, Return an error.
    print("Error")
    return False

# I always used this variable for test the entire time and I want it to stay :)
test = astar(start, finish)
print(f"The Fastest Route is {test}")


# running the actual PyGame
while game is False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    surface.fill(white)
    shapes()
    for x in range(len(test)-1):
        pygame.draw.line(surface, red, test[x], test[x+1], 3)

    pygame.display.update()