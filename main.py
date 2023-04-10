import pygame
import math
import gas

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

VOXEL_SIZE = 25

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 512

voxels = gas.get("level.json")
# print(voxels)
pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("frame")

clock = pygame.time.Clock()

def checkCollision(x, y, z, raiseErr=False):
    for voxel in voxels:
        if voxel[0] == x and voxel[1] == y and voxel[2] == z: # lookin for blocks
            if raiseErr:
                raise ValueError
            return voxel[3] # yep thats a block, return its id
    return False # no block :)

def drawVoxel(x, y, z, color):
    iso_x = (x - y) * VOXEL_SIZE / 2
    iso_y = (x + y) * VOXEL_SIZE / 4 - z * VOXEL_SIZE / 2
    hex_radius = VOXEL_SIZE / 2
    hex_center_x = iso_x + hex_radius
    hex_center_y = iso_y + hex_radius / 2
    hex_points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        point_x = hex_center_x + hex_radius * math.cos(angle_rad)
        point_y = hex_center_y + hex_radius * math.sin(angle_rad)
        hex_points.append((point_x, point_y))
    pygame.draw.polygon(screen, color, hex_points)
    pygame.draw.polygon(screen, 0, hex_points, 1)

def renderVoxels(voxels):
    voxels = sorted(voxels, key=lambda v: v[2], reverse=True)
    for voxel in voxels:
        drawVoxel(*voxel)


block_types = {
"natural.dirt": 0x6b4228,
"natural.grass": 0x386b27,
"natural.stone": 0x5a5c59,
"natural.tree#log": 0x302525,
"natural.tree#leaves": 0x0e2909,
"natural.water": 0x00add8,
"natural.sand": 0xd4c08e,
"natural.ice": 0xadd8e6,
"natural.clay": 0xa19035,
"extra.planks": 0xa3753b,
"extra.brick": 0x941403,
"extra.glass": 0x88c6db,
"unlisted.player": 0x0000ff
}
"""
def sortVoxels(voxels):
    results = []
    for voxel1 in voxels:
        x1, y1, z1, id1 = voxel1
        for voxel2 in voxels:
            x2, y2, z2, id2 = voxel2
            if x1 == x2 and y1 == y2 and z1 == z2:
                continue
            killme = (not (x1 >= x2 or x2 >= x1)) and (not (y1 >= y2 or (
"""
player_x = 0
player_y = 0
player_z = 1

debug = False

camera_x = 0
camera_y = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                try:
                    player_y -= 1
                    checkCollision(player_x, player_y, player_z, True)
                except ValueError:
                    player_y += 1
            elif event.key == pygame.K_DOWN:
                try:
                    player_y += 1
                    checkCollision(player_x, player_y, player_z, True)
                except ValueError:
                    player_y -= 1
            elif event.key == pygame.K_LEFT:
                try:
                    player_x -= 1
                    checkCollision(player_x, player_y, player_z, True)
                except ValueError:
                    player_x += 1
            elif event.key == pygame.K_RIGHT:
                try:
                    player_x += 1
                    checkCollision(player_x, player_y, player_z, True)
                except ValueError:
                    player_x -= 1
            elif event.key == pygame.K_LCTRL:
                try:
                    player_z -= 1
                    checkCollision(player_x, player_y, player_z, True)
                except ValueError:
                    player_z += 1
            elif event.key == pygame.K_LSHIFT:
                try:
                    player_z += 1
                    checkCollision(player_x, player_y, player_z, True)
                except ValueError:
                    player_z -= 1
            elif event.key == pygame.K_w:
                camera_y -= 1
            elif event.key == pygame.K_s:
                camera_y += 1
            elif event.key == pygame.K_a:
                camera_x -= 1
            elif event.key == pygame.K_d:
                camera_x += 1
            elif event.key == pygame.K_f:
                print(player_x, player_y, player_z, voxels, sep="\n")
            elif event.key == pygame.K_r:
                voxels = gas.get("level.json") #reloads map
    rvoxels = voxels + [[player_x, player_y, player_z, "unlisted.player"]]
    rvoxels_sorted = sorted(rvoxels, key=lambda v: v[2])
    screen.fill(BLACK)
    if debug:
        pygame.display.flip()
    for voxel in rvoxels_sorted:
        x, y, z, type = voxel
        drawVoxel(x + camera_x, y + camera_y, z, block_types[type])
        if debug:
            pygame.display.flip()
            pygame.time.wait(10)
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
