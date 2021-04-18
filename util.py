from typing import List
from quadtree import Point, Rectangle
import math
import numpy as np
from datetime import datetime

def get_angle_from_vector(vector):
    """Retruns the angle of a vector in degrees. (Angle to the x-axis.)"""
    x = vector[0]
    y = vector[1]
    rad = math.atan2(y, x)
    return np.degrees(rad) 




def centroid(points:List[Point]):
    """Calculates the centroid (center) of an array of multiple coordinates."""
    mean_x = sum(p.x for p in points)/len(points)
    mean_y = sum(p.y for p in points)/len(points)
    return Point(mean_x, mean_y)


def points_to_corr(points:List[Point]):
    """Truns a list of Point objects into two lists: xs and ys, to plot the result."""
    xs = []
    ys = []
    for point in points:
        xs.append(point.x)
        ys.append(point.y)
    return xs, ys


class Timer:
    def __init__(self, name):
        self.start = datetime.now()
        self.name = name
    
    def end(self):
        print(f"{self.name}: {(datetime.now() - self.start).seconds}")
    

if __name__ == "__main__":
    r = Rectangle(5, 5, 10, 10)
    for p in r.corners():
        print(f"{p.x}, {p.y}")
    
    print("--")
    c = centroid(r.corners())
    print(f"{c.x}, {c.y}")
