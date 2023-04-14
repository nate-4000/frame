"""
thanks to chatgpt for writing this (even though sometimes the level generates sideways)
"""
import noise
import json
import time

# Dimensions of the level
width = 24
length = 24
height = 16 # anything larger than this and i get segfaults

# Generate the heightmap using pnoise2
scale = 20
octaves = 6
persistence = 0.4
lacunarity = 1.3

def get_heightmap(seed):
    heightmap = [[0 for y in range(-length, length)] for x in range(-width,width)]
    for x in range(-width, width):
        for y in range(-length, length):
            heightmap[x][y] = int((noise.pnoise2(x/scale, y/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=width, repeaty=length, base=seed)+1)/2 * height)
            print(heightmap[x][y])
    return heightmap

# Generate the level based on the heightmap
def generate_level(seed):
    level = []
    print("heightmap gen")
    heightmap = get_heightmap(seed) # <------- segfault here 
    print("starting gen")
    for x in range(-width, width):
        for y in range(-length, length):
            for z in range(height):
                if z < heightmap[x][y]:
                    if z == heightmap[x][y] - 1:
                        level.append([x, y, z, "natural.grass"])
                        print(x,y,z,"grass")
                    else:
                        level.append([x, y, z, "natural.dirt"])
                        print(x,y,z,"dirt")
    return level



level_data = generate_level(int(time.time()) % 2048)
with open("level.json", "w") as of:
    json.dump(level_data, of)
