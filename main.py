import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.animation as animation
from random import random, randint, choice
import math
import numpy as np
import pandas as pd

import util

NUMBER_OF_ANTS = 50
TOTAL_FRAMES = 1000
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
    
    def get(self, typ=None, iteration=None, gt=False):
        mask = [True] * len(self.df.index)
        if iteration:
            mask = (self.df["iteration"] == iteration)
        if gt:
             mask = (self.df["iteration"] >= iteration)
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
            mask_close_objects = util.close(self.data.df, ant.getx(), ant.gety())
            df_close_objects = self.data.df[mask_close_objects]
            vls = df_close_objects.type.value_counts()
            num_H = vls.get("H")
            num_F = vls.get("F")
            num_food = vls.get("food")
            num_home = vls.get("home")
            if ant.has_food:
                if num_H:
                    # Go home
                    if util.distance(df_close_objects[df_close_objects["type"]=="H"].iloc[0], ant.getx(), ant.gety(), 0.2):
                        ant.has_food = False
                        ant.angle = (ant.angle + 120) % 360 # turn around 120°
                    else:
                        self.move_ant_to_objects(ant, "H", df_close_objects)
                elif num_home:
                    #follow home trail
                    self.move_ant_to_objects(ant, "home", df_close_objects)
                    self.data.append(ant.x, ant.y, "food", self.iteration)
                else:
                    # wlak random
                    ant.angle= ant.angle + randint(-20,20) % 360
                    self.data.append(ant.x, ant.y, "food", self.iteration)
            else: # Ant has no food
                if num_F:
                    if util.distance(df_close_objects[df_close_objects["type"]=="F"].iloc[0], ant.getx(), ant.gety(), 0.2):
                        ant.has_food = True
                        ant.angle = (ant.angle + 120) % 360 # turn around 120°
                    else:
                        self.move_ant_to_objects(ant, "F", df_close_objects)
                elif num_food:
                    # Follow food Trail
                    self.move_ant_to_objects(ant, "f", df_close_objects)
                    self.data.append(ant.x, ant.y, "home", self.iteration)
                else:
                    # walk random
                    ant.angle= ant.angle + randint(-20,20) % 360
                    self.data.append(ant.x, ant.y, "home", self.iteration)
            ant.forward()
            self.data.append(ant.x, ant.y, "ant", self.iteration)
        if self.iteration % 100 == 0:
            print(f"Frame: {self.iteration}")
        self.iteration += 1
    

    def move_ant_to_objects(self, ant, typ, df_close_objects):
        df = df_close_objects[df_close_objects["type"]==typ]
        center = util.centeroid(df)
        dif_vector = center - ant.get_pos()
        angle_to = util.get_angle_from_vector(dif_vector)
        ant.turn_towards(angle_to)
    
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

    def look_around(self, df):
        pass
            


    def getx(self):
        return self.x
    
    def gety(self):
        return self.y

    def get_pos(self):
        return np.array([self.x, self.y])

    
    def turn_towards(self, angle_to_object):
        self.angle -= (self.angle-angle_to_object) % 360

s = Simulator()
s.data.append(0, 0, "H", 0)
s.data.append(9, 7, "F", 0)
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
    ant_data = s.data.get(typ="ant", iteration=s.iteration-1)
    plt.scatter(ant_data["x"], ant_data["y"], s=10)
    food_data = s.data.get(typ="F")
    plt.scatter(food_data["x"], food_data["y"], s=100)
    home_data = s.data.get(typ="H")
    plt.scatter(home_data["x"], home_data["y"], s=100)



if __name__ == "__main__":
    anim = FuncAnimation(plt.gcf(), animate, frames=TOTAL_FRAMES)
    writer = PillowWriter(fps=FPS) 
    anim.save("ant_simulationPANDAS2.gif", writer=writer)
