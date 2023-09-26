import pygame
import pygame.gfxdraw as gfxdraw
import math
import gas
import levelgen #map a day keeps the boring debugging away
import time
import blocklogic
levelgen.dump()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

VOXEL_SIZE = 15
CAMERA_ROTATION = 0

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 512

voxels = gas.get("level.json")
# print(voxels)
pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("frame")

clock = pygame.time.Clock()

def checkCollision(x, y, z, raiseErr=False, careAboutDensity=False):
    for voxel in voxels:
        if voxel[0] == x and voxel[1] == y and voxel[2] == z: # lookin for blocks
            if raiseErr:
                raise ValueError
            if careAboutDensity and "dense" in block_types[voxel[3]]:
                if block_types[voxel[3]]["dense"] == False: # different if so that i dont get any KeyErrors
                    continue
            return voxel[3] # yep thats a block, return its id
    return False # no block :)

def use(dir):
    global voxels #cause we gonna be doing things with it
    if dir == "up": # # TODO: make a function for this
        useblock = checkCollision(player_x, player_y - 1, player_z)
        usepos = (player_x, player_y - 1, player_z)
    elif dir == "down":
        useblock = checkCollision(player_x, player_y + 1, player_z)
        usepos = (player_x, player_y + 1, player_z)
    elif dir == "left":
        useblock = checkCollision(player_x - 1, player_y, player_z)
        usepos = player_x - 1, player_y, player_z
    elif dir == "right":
        useblock = checkCollision(player_x - 1, player_y, player_z)
        usepos = (player_x - 1, player_y, player_z)
    if not useblock:
        return
    if useblock == "functional.door#closed":
        for i, door in enumerate(voxels): # find that door
            x, y, z = usepos
            if door[0] == x and door[1] == y and door[2] == z and door[3] == "functional.door#closed":
                # found it
                doorpos = i
        x, y, z = usepos
        voxels[doorpos] = [x, y, z, "functional.door#open"]
    elif useblock == "functional.door#open":
        for i, door in enumerate(voxels): # find that door
            x, y, z = usepos
            if door[0] == x and door[1] == y and door[2] == z and door[3] == "functional.door#open":
                # found it
                doorpos = i
        x, y, z = usepos
        voxels[doorpos] = [x, y, z, "functional.door#closed"]

block_types = {
"natural.dirt": {"color": 0x6b4228},
"natural.grass": {"color": 0x386b27},
"natural.stone": {"color": 0x5a5c59},
"natural.tree#log": {"color": 0x302525},
"natural.tree#leaves": {"color": 0x0e2909},
"natural.water": {"color": 0x00add8},
"natural.sand": {"color": 0xd4c08e},
"natural.ice": {"color": 0xadd8e6},
"natural.clay": {"color": 0xa19035},
"extra.planks": {"color": 0xa3753b},
"extra.brick": {"color": 0x941403},
"extra.glass": {"color": 0x88c6db},
"functional.door#closed": {"color": 0x632c0c},
"functional.door#open": {"color": 0x632c0c, "dense": False},
"unlisted.player": {"color": 0x0000ff, "dense": False}
}

player_x = 0
player_y = 0
player_z = 1

debug = False

camera_x = 0
camera_y = 0
seed = int(time.time()) % 2048

running = True
font = pygame.font.Font(None, 12)
    
preblits = {} # the optimization that only saved 1 fps
for key, value in block_types.items():
    preblits[key] = pygame.Surface((VOXEL_SIZE * 3, VOXEL_SIZE * 2), pygame.SRCALPHA)
    blocklogic.drawVoxel(preblits[key], VOXEL_SIZE * 3, VOXEL_SIZE * 2, VOXEL_SIZE, pygame, gfxdraw, 0, 0, 0, value["color"], (VOXEL_SIZE * 3 // 2, VOXEL_SIZE), alpha=True)

# this made me want to install github copilot
def movePlayer(direction: int):
    global player_x, player_y, player_z
    if direction == 0:
        try:
            player_y -= 1
            checkCollision(player_x, player_y, player_z, True, True)
        except ValueError:
            player_y += 1
    elif direction == 2:
        try:
            player_y += 1
            checkCollision(player_x, player_y, player_z, True, True)
        except ValueError:
            player_y -= 1
    elif direction == 1:
        try:
            player_x -= 1
            checkCollision(player_x, player_y, player_z, True, True)
        except ValueError:
            player_x += 1
    elif direction == 3:
        try:
            player_x += 1
            checkCollision(player_x, player_y, player_z, True, True)
        except ValueError:
            player_x -= 1
    elif direction == 4:
        try:
            player_z -= 1
            checkCollision(player_x, player_y, player_z, True, True)
        except ValueError:
            player_z += 1
    elif direction == 5:
        try:
            player_z += 1
            checkCollision(player_x, player_y, player_z, True, True)
        except ValueError:
            player_z -= 1


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # woohoo less terrible looking code!!
            if event.key == pygame.K_w: # TODO: fix it going the other direction on odd camera rotations
                movePlayer((0 + CAMERA_ROTATION) % 4)
            elif event.key == pygame.K_s:
                movePlayer((2 + CAMERA_ROTATION) % 4) 
            elif event.key == pygame.K_a:
                movePlayer((1 + CAMERA_ROTATION) % 4)
            elif event.key == pygame.K_d:
                movePlayer((3 + CAMERA_ROTATION) % 4)
            elif event.key == pygame.K_LCTRL:
                movePlayer(4)
            elif event.key == pygame.K_LSHIFT:
                movePlayer(5)
            elif event.key == pygame.K_f:
                print(player_x, player_y, player_z, voxels, camera_x, camera_y, sep="\n")
            elif event.key == pygame.K_r:
                voxels = gas.get("level.json") #reloads map
            elif event.key == pygame.K_q:
                # remake level
                levelgen.dump()
            elif event.key == pygame.K_UP:
                use("up")
            elif event.key == pygame.K_DOWN:
                use("down")
            elif event.key == pygame.K_LEFT:
                use("left")
            elif event.key == pygame.K_RIGHT:
                use("right")
            elif event.key == pygame.K_l:
                CAMERA_ROTATION = (CAMERA_ROTATION + 1) % 4
    
    # BEFORE ANYTHING HAPPENS check if inside ground, then force out if stuck
    if checkCollision(player_x, player_y, player_z):
        player_z += 1

    
    WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
    center_x = WINDOW_WIDTH // 2
    center_y = WINDOW_HEIGHT // 2
    camera_x = center_x 
    camera_y = center_y
    
    rvoxels = voxels + [[player_x, player_y, player_z, "unlisted.player"]]
    #what the heck is this? put the diff in a function
    if CAMERA_ROTATION == 0:
        rvoxels_sorted = sorted(rvoxels, key=lambda v: v[0] + v[1] + v[2])
    elif CAMERA_ROTATION == 1:
        rvoxels_sorted = sorted(rvoxels, key=lambda v: v[1] - v[0] + v[2])
    elif CAMERA_ROTATION == 2:
        rvoxels_sorted = sorted(rvoxels, key=lambda v: -v[0] - v[1] + v[2])
    elif CAMERA_ROTATION == 3:
        rvoxels_sorted = sorted(rvoxels, key=lambda v: -v[1] + v[0] + v[2])
    screen.fill(BLACK)
    if debug:
        pygame.display.flip()
    for voxel in rvoxels_sorted:
        x, y, z, type = voxel
        if CAMERA_ROTATION == 0:
            blocklogic.drawBlit(screen, preblits, VOXEL_SIZE, x - player_x, y - player_y, z - player_z, type, (camera_x - (VOXEL_SIZE * 3 // 2), camera_y - VOXEL_SIZE))
        elif CAMERA_ROTATION == 1:
            blocklogic.drawBlit(screen, preblits, VOXEL_SIZE, y - player_y, -x + player_x, z - player_z, type, (camera_x - (VOXEL_SIZE * 3 // 2), camera_y - VOXEL_SIZE))
        elif CAMERA_ROTATION == 2:
            blocklogic.drawBlit(screen, preblits, VOXEL_SIZE, -x + player_x, -y + player_y, z - player_z, type, (camera_x - (VOXEL_SIZE * 3 // 2), camera_y - VOXEL_SIZE))
        elif CAMERA_ROTATION == 3:
            blocklogic.drawBlit(screen, preblits, VOXEL_SIZE, -y + player_y, x - player_x, z - player_z, type, (camera_x - (VOXEL_SIZE * 3 // 2), camera_y - VOXEL_SIZE))
        if debug:
            pygame.display.flip()
    fps = clock.get_fps()
    fpstext = font.render("fps: %.2f" % fps, True, 0x777777)
    seedtext = font.render("seed: %d" % seed, True, 0x777777)
    screen.blit(fpstext, (10, 10))
    screen.blit(seedtext,(10, 30))
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
