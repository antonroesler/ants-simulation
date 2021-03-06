import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
import matplotlib.animation as animation
from random import random, randint, choice
import math
import numpy as np
from quadtree import Point, Rectangle, Circle, QuadTree
import util

NUMBER_OF_ANTS = 90
TOTAL_FRAMES = 1750
FPS = 30
TRAILS = True

SIGHT = 2

AREA = Rectangle(15, 15, 12, 12)

TRAIL_FREQ = 3
FOOD_DIST_DECR = 0.1

QUADTREE_CAPACITY = 4


class Simulator:
    def __init__(self):
        self.ants = []
        self.food = Circle(19,18,0.2)
        self.home = Circle(10,10,0.2)
        self.home_trail = QuadTree(AREA, capacity=QUADTREE_CAPACITY)
        self.food_trail = QuadTree(AREA, capacity=QUADTREE_CAPACITY)
        self.iteration = -1

    def create_new_ant(self, n=1):
        for _ in range(n):
            self.ants.append(Ant())

    def step(self):
        self.iteration += 1
        for ant in self.ants:
            ant.forward()
            if ant.x > 25 or ant.x < 5 or ant.y > 25 or ant.y < 5:
                self.ants.remove(ant) # Kill ants that are to far away.
                continue
            if not ant.has_food:
                if self.food.contains(ant): # Ant has reached the food source.
                    ant.has_food = True
                    ant.angle = (ant.angle + 180) % 360 # turn around
                elif ant.in_sight(self.food):
                    # Ant turn towards food source
                    ant.turn_towards(self.food.center(), strength=1)


                else:
                    sight = Circle(ant.x, ant.y, SIGHT)
                    food_trail_in_sight = self.food_trail.query_circle(sight)
                    if len(food_trail_in_sight)>0:
                        centroid = util.centroid(food_trail_in_sight)
                        ant.turn_towards(centroid, is_food=True)
                    else:
                        ant.angle+=randint(-20,20)
                if self.iteration % TRAIL_FREQ == 0:
                    self.home_trail.insert(ant.point())

            else:
                if self.home.contains(ant):
                    ant.has_food = False
                    ant.angle = 45
                elif ant.in_sight(self.home):
                    ant.turn_towards(self.home.center(), strength=1)
                    #if self.iteration % TRAIL_FREQ == 0:
                        #self.food_trail.insert(ant.point())

                else:
                    sight = Circle(ant.x, ant.y, SIGHT)
                    home_trail_in_sight = self.home_trail.query_circle(sight)
                    if len(home_trail_in_sight)>0:
                        centroid = util.centroid(home_trail_in_sight)
                        ant.turn_towards(centroid)
                    else:
                        ant.angle+=randint(-20,20)
                    if self.iteration % TRAIL_FREQ == 0:
                        self.food_trail.insert(ant.point())


    def get_ant_pos(self):
        xs = []
        ys = []
        for ant in self.ants:
            xs.append(ant.x)
            ys.append(ant.y)
        return xs, ys


class Ant(Point):
    def __init__(self):
        super().__init__(10,10)
        self.angle = 45
        self.speed = .05
        self.has_food = False
        self.food_vectors = []

    def forward(self):
        x, y = self.get_direction_vector()
        self.x += x*self.speed
        self.y += y*self.speed

    def get_direction_vector(self):
        x = np.cos(np.radians(self.angle))
        y = np.sin((np.radians(self.angle)))
        return x, y

    def reach_object(self, objects):
        for object_pos in objects:
            vector_to_object = object_pos - self.pos
            if np.sqrt(vector_to_object.dot(vector_to_object)) < 0.2:
                return True
        return False

    def in_sight(self, obj, mult=1):
        """Returns True if an Point or Circle object is within sight of the ant."""
        sight = Circle(self.x, self.y, SIGHT*mult)
        if isinstance(obj, Circle):
            return sight.intersects(obj)
        elif isinstance(obj, Point):
            return sight.contains(obj)
        else:
            raise TypeError(f"obj is of type {type(obj).__name__}, but must be of type Point or Circle")

    def turn_towards(self, point:Point, strength=0.5, is_food=False):
        if not isinstance(point, Point):
            raise TypeError(f"point is of type {type(point).__name__}, but must be of type Point")
        dir_x = point.x - self.x
        dir_y = point.y - self.y
        angle_to_object = util.get_angle_from_vector([dir_x, dir_y])
        if is_food:
            if self.food_vectors:
                vec = [(self.get_food_vector()[0]*2 + dir_x)/3, (self.get_food_vector()[0]*2 + dir_y)/3]
                angle_to_object = util.get_angle_from_vector(vec)
            self.food_vectors.append([dir_x, dir_y])
        if not (160 < abs(angle_to_object-self.angle) < 200): # To not get stuck, the ant should not make strong turns.
            random_factor = choice([random()/4,0])
            self.angle -= (self.angle-angle_to_object)*strength*random_factor
            self.angle = self.angle%360

    def point(self):
        """Returns the ant's position as a Point."""
        return Point(self.x, self.y)

    def get_food_vector(self):
        x = 0
        y = 0
        for v in self.food_vectors:
            x += v[0]
            y += v[1]
        return x/len(self.food_vectors), y/len(self.food_vectors)


s = Simulator()
plt.scatter([],[])

def animate(some):
    if len(s.ants) < NUMBER_OF_ANTS:
        s.create_new_ant()
    plt.cla()
    s.step()
    if TRAILS:
        htx, hty = util.points_to_corr(s.home_trail.all)
        ftx, fty = util.points_to_corr(s.food_trail.all)
        plt.scatter(htx, hty, alpha=0.05, s=2, c="r")
        plt.scatter(ftx, fty, alpha=0.1, s=2, c="green")
    x,y = s.get_ant_pos()
    plt.xlim([9, 21])
    plt.ylim([9, 21])
    plt.scatter(x, y, s=3, c="black")
    plt.scatter(s.food.x, s.food.y, s=50, c="forestgreen")
    plt.scatter(s.home.x, s.home.y, s=50, c="darkorange")
    if s.iteration % 50 ==0:
        print(f"Iteration: {s.iteration}")

anim = FuncAnimation(plt.gcf(), animate, frames=TOTAL_FRAMES)
#writer = PillowWriter(fps=FPS)
writer2= FFMpegWriter(fps=FPS)
anim.save("ant_simulation004.mp4", writer=writer2)
