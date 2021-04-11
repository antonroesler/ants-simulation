def centeroid(arr):
    """Calculates the centeroid (center) of an array of multiple coordinates."""
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return sum_x/length, sum_y/length

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
    

def close(df, x, sum_y, distance=1):
    mask = df.apply(distance, axis = "columns", args=(x, y, distance))
    print(df[mask])