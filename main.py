import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.animation as animation
from random import random, randint, choice
import math
import numpy as np
import pandas as pd

import util

NUMBER_OF_ANTS = 10
TOTAL_FRAMES = 50
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
            self.ants.append(Ant())
    
    def step(self):
        if len(self.ants) < NUMBER_OF_ANTS:
            self.create_new_ant()
        for ant in self.ants:
            ant.forward()
            if ant.pos[0] > 20 or ant.pos[0] < -10 or ant.pos[1] > 20 or ant.pos[1] < -10:
                self.ants.remove(ant) # Kill ants that are to far away
                continue
            if not ant.has_food:
                if any(util.close(self.data.get(typ="F"), ant.getx(), ant.gety(), dist=0.2)):
                    ant.has_food = True
                    ant.angle = (ant.angle + 120) % 360 # turn around 120°
                
                elif any(h.set(util.close(self.data.get(typ="F"), ant.getx(), ant.gety(), dist=1.4))):
                    center = util.centeroid(self.data.get()[h.get()])
                    direction_vector = center - ant.pos
                    angle = util.get_angle_from_vector(direction_vector)
                    ant.turn_towards(angle)
                    self.data.append(ant.pos[0], ant.pos[1], "home", self.iteration)

                elif any(h.set(util.close(self.data.get(typ="food"), ant.getx(), ant.gety()))): 
                    center = util.centeroid(self.data.get()[h.get()])
                    direction_vector = center - ant.pos
                    angle = util.get_angle_from_vector(direction_vector)
                    ant.turn_towards(angle)
                    self.data.append(ant.pos[0], ant.pos[1], "home", self.iteration)
                    
                else:
                    ant.angle+=randint(-20,20)
                    self.data.append(ant.pos[0], ant.pos[1], "home", self.iteration)
                    
            else:
                if any(util.close(self.data.get(typ="H"), ant.getx(), ant.gety(), dist=0.2)):
                    ant.has_food = False
                    ant.angle = (ant.angle + 120) % 360 # turn around 120°
                
                elif any(h.set(util.close(self.data.get(typ="H"), ant.getx(), ant.gety(), dist=1.4))):
                    center = util.centeroid(self.data.get()[h.get()])
                    direction_vector = center - ant.pos
                    angle = util.get_angle_from_vector(direction_vector)
                    ant.turn_towards(angle)
                    self.data.append(ant.pos[0], ant.pos[1], "food", self.iteration)

                elif any(h.set(util.close(self.data.get(typ="home"), ant.getx(), ant.gety()))): 
                    center = util.centeroid(self.data.get()[h.get()])
                    direction_vector = center - ant.pos
                    angle = util.get_angle_from_vector(direction_vector)
                    ant.turn_towards(angle)

                    self.data.append(ant.pos[0], ant.pos[1], "food", self.iteration)
                    
                else:
                    ant.angle+=randint(-20,20)
                    self.data.append(ant.pos[0], ant.pos[1], "home", self.iteration)
        self.data.append(ant.pos[0], ant.pos[1], "ant", self.iteration)
        self.iteration += 1
    
    
class Ant:
    def __init__(self):
        self.pos = np.array([0,0])
        self.angle = choice([-45, 0, 45, 90])
        self.speed = 0.05
        self.has_food = False
    
    def forward(self):
        self.pos = np.add(self.pos, util.get_direction_vector(self.angle)*self.speed)
    
    def getx(self):
        return self.pos[0]
    
    def gety(self):
        return self.pos[1]
    
    


    
    def turn_towards(self, angle_to_object):
        self.angle -= (self.angle-angle_to_object)
        

s = Simulator()
s.data.append(0, 0, "H", None)
s.data.append(9, 7, "F", None)
plt.scatter([],[])

def animate(some):
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
