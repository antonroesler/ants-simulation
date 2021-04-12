import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.animation as animation
from random import random, randint, choice
import math
import numpy as np
import pandas as pd

import util

NUMBER_OF_ANTS = 50
TOTAL_FRAMES = 100
FPS = 30
TRAILS = True

DATA_STRUCTURE = {"x":[], "y":[], "type":[], "iteration":[]}

h = util.Holder()

class DataStore:
    def __init__(self):
        self.df = pd.DataFrame(DATA_STRUCTURE)
        self.df["iteration"] = self.df["iteration"].astype("int")
        self.df["type"] = self.df["type"].astype("category")
    
    def append(self, x, y, typ, iteration):
        self.df = self.df.append({"x":x, "y":y, "type":typ, "iteration":iteration}, ignore_index=True)
    
    def get(self, typ=None, iteration=None):
        mask = [True] * len(self.df.index)
        if iteration:
            mask = (self.df["iteration"] == iteration) 
        if typ:
            mask = (self.df["type"] == typ) & mask
        return self.df[mask]


class Simulator:
    def __init__(self):
        self.ants = []
        self.data = DataStore()
        self.iteration = 0
    
    def create_new_ant(self, n=1):
        for _ in range(n):
            ant = Ant()
            self.ants.append(ant)
            self.data.append(ant.getx(), ant.gety(), "ant", self.iteration)
    
    def step(self):
        for ant in self.ants:
            if ant.x > 12 or ant.x < -2 or ant.y > 12 or ant.y < -2:
                self.ants.remove(ant) # Kill ants that are to far away
                continue
            if not ant.has_food:
                if any(util.close(self.data.get(typ="F"), ant.getx(), ant.gety(), dist=0.2)):
                    ant.has_food = True
                    ant.angle = (ant.angle + 120) % 360 # turn around 120°
                
                elif any(util.close(self.data.get(typ="F"), ant.getx(), ant.gety(), dist=1.4)):

                    center = util.centeroid(self.data.get()[util.close(self.data.get(typ="F"), ant.getx(), ant.gety(), dist=1.4)])
                    direction_vector = center - ant.get_pos()
                    angle = util.get_angle_from_vector(direction_vector)
                    ant.turn_towards(angle)
                    self.data.append(ant.x, ant.y, "home", self.iteration)

                elif True in util.close(self.data.get(typ="food"), ant.getx(), ant.gety()):
                    center = util.centeroid(self.data.get()[util.close(self.data.get(typ="food"), ant.getx(), ant.gety())])
                    direction_vector = center - ant.get_pos()
                    angle = util.get_angle_from_vector(direction_vector)
                    ant.turn_towards(angle)
                    self.data.append(ant.x, ant.y, "home", self.iteration)
                    
                else:
                    ant.angle+=randint(-20,20)
                    self.data.append(ant.x, ant.y, "home", self.iteration)
                    
            else:
                if any(util.close(self.data.get(typ="H"), ant.getx(), ant.gety(), dist=0.2)):
                    ant.has_food = False
                    ant.angle = (ant.angle + 120) % 360 # turn around 120°
                
                elif any(util.close(self.data.get(typ="H"), ant.getx(), ant.gety(), dist=1.4)):
                    center = util.centeroid(self.data.get()[util.close(self.data.get(typ="H"), ant.getx(), ant.gety(), dist=1.4)])
                    direction_vector = center - ant.get_pos()
                    angle = util.get_angle_from_vector(direction_vector)
                    ant.turn_towards(angle)
                    self.data.append(ant.x, ant.y, "food", self.iteration)

                elif any(util.close(self.data.get(typ="home"), ant.getx(), ant.gety())):
                    center = util.centeroid(self.data.get()[util.close(self.data.get(typ="home"), ant.getx(), ant.gety())])
                    direction_vector = center - ant.get_pos()
                    angle = util.get_angle_from_vector(direction_vector)
                    ant.turn_towards(angle)

                    self.data.append(ant.x, ant.y, "food", self.iteration)
                    
                else:
                    ant.angle+=randint(-20,20)
                    self.data.append(ant.x, ant.y, "home", self.iteration)
            ant.forward()
            self.data.append(ant.x, ant.y, "ant", self.iteration)
        self.iteration += 1
    
    
class Ant:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 45
        self.speed = 0.05
        self.has_food = False
    
    def forward(self):
        current_pos = self.get_pos()
        direction_vector = util.get_direction_vector(self.angle)
        new_pos = np.add(current_pos, direction_vector*self.speed)
        self.x = new_pos[0]
        self.y = new_pos[1]


    def getx(self):
        return self.x
    
    def gety(self):
        return self.y

    def get_pos(self):
        return np.array([self.x, self.y])

    
    def turn_towards(self, angle_to_object):
        self.angle -= (self.angle-angle_to_object)

s = Simulator()
s.data.append(0, 0, "H", 0)
s.data.append(9, 7, "F", 0)
s.ants.append(Ant())
s.create_new_ant()
plt.scatter([],[])

def animate(some):
    if len(s.ants) < NUMBER_OF_ANTS:
            s.ants.append(Ant())
    plt.cla()
    plt.xlim([-1, 10])
    plt.ylim([-1, 10])
    s.step()
    if TRAILS:
        home_trail = s.data.get(typ="home")
        plt.scatter(home_trail["x"], home_trail["y"], alpha=0.1, s=4, c="r")
        food_trail = s.data.get(typ="food")
        plt.scatter(food_trail["x"], food_trail["y"], alpha=0.1, s=4, c="y")
    ant_data = s.data.get(typ="ant", iteration=s.iteration)
    plt.scatter(ant_data["x"], ant_data["y"], s=10)
    food_data = s.data.get(typ="F")
    plt.scatter(food_data["x"], food_data["y"], s=100)
    home_data = s.data.get(typ="H")
    plt.scatter(home_data["x"], home_data["y"], s=100)




anim = FuncAnimation(plt.gcf(), animate, frames=TOTAL_FRAMES)
writer = PillowWriter(fps=FPS) 
anim.save("ant_simulationPANDAS1.gif", writer=writer)
