import pygame
import math
import gas

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

VOXEL_SIZE = 50

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 512

voxels = gas.get("level.json")

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Voxel Renderer")

clock = pygame.time.Clock()

def draw_voxel(x, y, z, color):
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

def render_voxels(voxels):
    screen.fill(BLACK)
    voxels_sorted = sorted(voxels, key=lambda voxel: voxel[2], reverse=True)
    for voxel in voxels_sorted:
        x, y, z, color = voxel
        draw_voxel(x, y, z, color)

player_x = 3
player_y = 3
player_z = 1
player_c = 0x0000FF

camera_x = 0
camera_y = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_y -= 1
            elif event.key == pygame.K_DOWN:
                player_y += 1
            elif event.key == pygame.K_LEFT:
                player_x -= 1
            elif event.key == pygame.K_RIGHT:
                player_x += 1
            elif event.key == pygame.K_LCTRL:
                player_z -= 1
            elif event.key == pygame.K_LSHIFT:
                player_z += 1
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
    rvoxels = voxels
    rvoxels_sorted = sorted(rvoxels, key=lambda voxel: voxel[2], reverse=True)
    screen.fill(BLACK)
    for voxel in rvoxels_sorted:
        x, y, z, color = voxel
        if z < player_z:
            draw_voxel(x + camera_x, y + camera_y, z, color)
            draw_voxel(player_x + camera_x, player_y + camera_y, player_z, player_c)
        elif z > player_z:
            draw_voxel(player_x + camera_x, player_y + camera_y, player_z, player_c)
            draw_voxel(x + camera_x, y + camera_y, z, color)
        else:
                if y < player_y:
                    draw_voxel(x + camera_x, y + camera_y, z, color)
                    draw_voxel(player_x + camera_x, player_y + camera_y, player_z, player_c)
                elif y > player_y:
                    draw_voxel(player_x + camera_x, player_y + camera_y, player_z, player_c)
                    draw_voxel(x + camera_x, y + camera_y, z, color)
                else:
                    if z < player_z:
                        draw_voxel(x + camera_x, y + camera_y, z, color)
                        draw_voxel(player_x + camera_x, player_y + camera_y, player_z, player_c)
                    elif z > player_z:
                        draw_voxel(player_x + camera_x, player_y + camera_y, player_z, player_c)
                        draw_voxel(x + camera_x, y + camera_y, z, color)
                    else:
                        draw_voxel(player_x + camera_x, player_y + camera_y, player_z, player_c)
    
    pygame.display.flip()
    
    clock.tick(60)
    
pygame.quit()
