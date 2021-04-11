import numpy as np
import math 

def centeroid(df):
    """Calculates the centeroid (center) of an array of multiple coordinates."""
    mean_x = df.x.mean()
    mean_y = df.y.mean()
    return np.array([mean_x, mean_y])

def rotate(vector, degree):
    """Rotates the direction. Degree in 360°. NOT IN USE"""
    theta = np.radians(degree)
    c, s = np.cos(theta), np.sin(theta)
    Rot = np.array(((c, -s), (s, c)))
    return Rot.dot(vector)
    
def get_direction_vector(angle):
    x = np.cos(np.radians(angle))
    y = np.sin((np.radians(angle)))
    return np.array([x, y])
        
        
def get_angle_from_vector(vector):
    x = vector[0]
    y = vector[1]
    rad = math.atan2(y, x)
    return np.degrees(rad) 

def distance(row, x, y, dist):
    return math.sqrt((float(row[0]) - x)**2 + (float(row[1]) - y)**2) < dist
    

def close(df, x, y, dist=1):
    mask = df.apply(distance, axis = "columns", args=(x, y, dist))
    return mask

class Holder:
    def set(self, value):
        self.value = value
        return value
    def get(self):
        return self.value