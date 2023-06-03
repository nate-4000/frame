"""
Populates the maps folder with every possible map. If you load a game of frame, your map is sure to be in here.
"""

import numpy as np
from levelgen import get_heightmap
from PIL import Image

def save_heightmap_image(heightmap, save_path):
    normalized_heightmap = []
    
    for i in heightmap:
        whao = []
        for d in i:
            whao.append(int(d / height * 255))
        normalized_heightmap.append(whao)
    
    image = Image.fromarray(np.asarray(normalized_heightmap, dtype=np.uint8))
    image.save(save_path)

width = 32
length = 32
height = 16
scale = 20
octaves = 8
persistence = 0.5
lacunarity = 1.2
seed = 0

while seed <= 2047:
    heightmap = get_heightmap(seed)
    print(seed)
    save_path = 'maps/map%s.png' % seed
    save_heightmap_image(heightmap, save_path)
    seed += 1