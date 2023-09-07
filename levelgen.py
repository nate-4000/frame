"""
thanks to chatgpt for writing this (even though sometimes the level generates sideways)
"""
import noise
import json
import time
import numpy as np

# Dimensions of the level
width = 32
length = 32
height = 16 # anything larger than this and i get segfaults

# Generate the heightmap using pnoise2
scale = 20
octaves = 8
persistence = 0.5
lacunarity = 1.2

def get_heightmap(seed):
    noise_values = np.zeros((2*width, 2*length))
    for x in range(-width, width):
        for y in range(-length, length):
            noise_values[x+width,y+length] = noise.pnoise2(x/scale, y/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=width, repeaty=length, base=seed)
    heightmap = np.floor((noise_values+1)/2 * height).astype(int)
    return heightmap.tolist()


# Generate the level based on the heightmap
def generate_level(seed):
    level = []
    print("heightmap gen")
    heightmap = get_heightmap(seed) # <------- segfault here 
    print("starting gen")
    for x in range(-width+width, width+width):
        for y in range(-length+length, length+length):
            for z in range(height):
                if z < heightmap[x][y]:
                    if z == heightmap[x][y] - 1:
                        level.append([x-(width//2), y-(length//2), z, "natural.grass"])
                    else:
                        level.append([x-(width//2), y-(length//2), z, "natural.dirt"])
    return level


def dump():
    level_data = generate_level(int(time.time()) % 2048)
    with open("level.json", "w") as of:
        json.dump(level_data, of)
