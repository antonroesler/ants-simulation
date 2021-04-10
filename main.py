import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.animation as animation
from random import random, randint, choice
import math
import numpy as np

class Simulator:
    def __init__(self):
        self.ants = []
        self.food = [[9, 7]]
        self.home = [0, 0]
        self.home_trail= []
        self.food_trail= [[9, 7]]
    
    def create_new_ant(self, n=1):
        for _ in range(n):
            self.ants.append(Ant())
    
    def step(self):
        """
        if len(self.home_trail) > 30000:
            self.home_trail = self.home_trail[-30000:]
        if len(self.food_trail) > 30000:
            self.food_trail = self.food_trail[-30000:]
        """
        for ant in self.ants:
            ant.forward()
       
        for ant in self.ants:
            if ant.pos[0] > 20 or ant.pos[0] < -10 or ant.pos[1] > 20 or ant.pos[1] < -10:
                self.ants.remove(ant) # Kill ants that are to far away
                continue
            if not ant.has_food:
                if ant.reach_object(self.food):
                    ant.has_food = True
                    ant.angle = (ant.angle + 120) % 360 # turn around 120°
                elif ant.in_sight(self.food, turn=True, strong=1.5): 
                    self.home_trail.append(ant.pos)
                    
                else:
                    if ant.in_sight(self.food_trail, turn=True):
                        ant.forward() 
                    else:
                        ant.angle+=randint(-20,20)
                    self.home_trail.append(ant.pos)
                    
            else:
                if ant.reach_object(self.home):
                    ant.has_food = False
                    ant.angle = (ant.angle + 120) % 360 # turn around 120°
                elif ant.in_sight(self.home, turn=True):
                    self.food_trail.append(ant.pos)
                else:
                    ant.in_sight(self.home_trail, turn=True)
                    self.food_trail.append(ant.pos)
    
    def get_ant_pos(self):
        xs = []
        ys = []
        for ant in self.ants:
            x,y = ant.pos
            xs.append(x)
            ys.append(y)
        return xs, ys
    
    
class Ant:
    def __init__(self):
        self.pos = np.array([0,0])
        self.angle = choice([-45, 0, 45, 90])
        self.speed = 0.05
        self.has_food = False
    
    def forward(self):
        self.pos = np.add(self.pos, self.get_direction_vector()*self.speed)
    
    def get_direction_vector(self):
        x = np.cos(np.radians(self.angle))
        y = np.sin((np.radians(self.angle)))
        return np.array([x, y])
        
        
    def get_angle_from_vector(self, vector):
        x = vector[0]
        y = vector[1]
        rad = math.atan2(y, x)
        return np.degrees(rad) 
    
    def reach_object(self, objects):
        for object_pos in objects:
            vector_to_object = object_pos - self.pos
            if np.sqrt(vector_to_object.dot(vector_to_object)) < 0.2:
                return True
        return False
    
    def in_sight(self, objects, turn=False, strong=1):
        for object_pos in objects:
            vector_to_object = object_pos - self.pos
            angle_to_object = self.get_angle_from_vector(vector_to_object)
            distance = np.sqrt(vector_to_object.dot(vector_to_object))
            if abs(self.angle - angle_to_object) <= 45/distance and distance < 1*strong:
                if turn:
                    self.turn_towards(angle_to_object)
                return True
        return False
    
    def turn_towards(self, angle_to_object):
        self.angle -= (self.angle-angle_to_object)
        
    def rotate(self, vector, degree):
        """Rotates the direction. Degree in 360°. NOT IN USE"""
        theta = np.radians(degree)
        c, s = np.cos(theta), np.sin(theta)
        Rot = np.array(((c, -s), (s, c)))
        return Rot.dot(vector)

s = Simulator()
s.create_new_ant(n=100)

plt.scatter([],[])

def animate(some):
    plt.cla()
    s.step()
    x,y = s.get_ant_pos()
    plt.xlim([-1, 10])
    plt.ylim([-1, 10])
    plt.scatter(x, y)
    fx, fy = s.food[0]
    plt.scatter(fx, fy, s=100)
    plt.scatter(0, 0, s=100)
    htx, hty = np.transpose(np.array(s.home_trail))
    plt.scatter(htx, hty, alpha=0.05, s=4, c="r")
    ftx, fty = np.transpose(np.array(s.food_trail))
    plt.scatter(ftx, fty, alpha=0.1, s=4, c="y")

anim = FuncAnimation(plt.gcf(), animate, frames=1000)
writer = PillowWriter(fps=50) 
anim.save("ant_simulation.gif", writer=writer)
