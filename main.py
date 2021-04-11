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
TRAIL_FREQUENCY = 4

DATA_STRUCTURE = {"x":[], "y":[], "type":[], "iteration":[]}

class DataStore:
    def __init__(self):
        self.df = pd.DataFrame(DATA_STRUCTURE)
        self.df["iteration"] = self.df["iteration"].astype("int")
        self.df["type"] = self.df["type"].astype("category")
    
    def append(self, x, y, typ, iteration):
        self.df.append({"x":x, "y":y, "type":typ, "iteration":iteration}, ignore_index=True)
    
    def get(self, typ=None, iteration=None):
        mask = [True] * len(self.df.index)
        if iteration:
            mask = (self.df["iteration"] == iteration) 
        if typ:
            mask = (self.df["type"] == "ant") & mask
        return self.df[mask]


class Simulator:
    def __init__(self):
        self.food = [[9, 7]]
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
                if any(util.close(self.food, ant.getx(), ant.gety(), distance=0.2)): # food muss ein eigener df werden
                    ant.has_food = True
                    ant.angle = (ant.angle + 120) % 360 # turn around 120°
                elif util.close(self.data.get(typ="food"): 
                    self.data.append(ant.pos[0], ant.pos[1], "home", self.iteration)
                    
                else:
                    if ant.in_sight(self.data.get(typ="food"), turn=True):
                        ant.forward() 
                    else:
                        ant.angle+=randint(-20,20)
                    self.data.append(ant.pos[0], ant.pos[1], "home", self.iteration)
                    
            else:
                if ant.reach_object(self.home):
                    ant.has_food = False
                    ant.angle = (ant.angle + 120) % 360 # turn around 120°
                elif ant.in_sight(self.home, turn=True):
                    self.data.append(ant.pos[0], ant.pos[1], "food", self.iteration)
                else:
                    ant.in_sight(self.home_trail, turn=True)
                    self.data.append(ant.pos[0], ant.pos[1], "food", self.iteration)
        self.data.append(ant.pos[0], ant.pos[1], "ant", self.iteration)
        self.iteration += 1
    
    
class Ant:
    def __init__(self):
        self.pos = np.array([0,0])
        self.angle = choice([-45, 0, 45, 90])
        self.speed = 0.05
        self.has_food = False
    
    def forward(self):
        self.pos = np.add(self.pos, self.get_direction_vector()*self.speed)
    
    def getx(self):
        return self.pos[0]
    
    def gety(self):
        return self.pos[1]
    
    


    
    def turn_towards(self, angle_to_object):
        self.angle -= (self.angle-angle_to_object)
        

s = Simulator()
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
    fx, fy = s.food[0]
    plt.scatter(fx, fy, s=100)
    plt.scatter(0, 0, s=100)

anim = FuncAnimation(plt.gcf(), animate, frames=TOTAL_FRAMES)
writer = PillowWriter(fps=FPS) 
anim.save("ant_simulation8.gif", writer=writer)
