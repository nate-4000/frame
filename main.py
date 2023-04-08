from multiprocessing import Value
import pygame
import math
import gas

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

VOXEL_SIZE = 50

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 512

voxels = gas.get("level.json")
# print(voxels)
pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("frame")

clock = pygame.time.Clock()

def checkCollision(x, y, z, raiseErr=False):
    for voxel in voxels:
        if voxel[0] == x and voxel[1] == y and voxel[2] == z: # lookin for blocks
            if raiseErr:
                raise ValueError
            return True # yep thats a block
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

def renderVoxels(voxels):
    voxels = sorted(voxels, key=lambda v: v[2], reverse=True)
    for voxel in voxels:
        drawVoxel(*voxel)


block_types = {
"default.dirt": 0x6b4228,
"default.grass": 0x386b27,
"default.stone": 0x5a5c59,
"default.tree#log": 0x302525,
"default.tree#leaves": 0x0e2909,
"default.water": 0x00add8,
"unlisted.player": 0x0000ff
}

player_x = 0
player_y = 0
player_z = 1
player_c = 0x0000FF

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
    
    rvoxels = voxels + [[player_x, player_y, player_z, "unlisted.player"]]
    rvoxels_sorted = sorted(rvoxels, key=lambda v: v[2])
    screen.fill(BLACK)
    if debug:
        pygame.display.flip()
    for voxel in rvoxels_sorted:
        x, y, z, color = voxel
        drawVoxel(x + camera_x, y + camera_y, z, block_types[color])
        if debug:
            pygame.display.flip()
            pygame.time.wait(1)
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
