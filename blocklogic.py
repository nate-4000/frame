import math

def is_offscreen(surface, target_surface, offset=(0, 0)):
    surface_rect = surface.get_rect()
    surface_rect.x += offset[0]
    surface_rect.y += offset[1]
    target_rect = target_surface.get_rect()

    if (surface_rect.right < 0 or
        surface_rect.bottom < 0 or
        surface_rect.left > target_rect.right or
        surface_rect.top > target_rect.bottom):
        return True
    
    return False



def drawVoxel(screen, WINDOW_HEIGHT, WINDOW_WIDTH, VOXEL_SIZE, pygame, gfxdraw, x, y, z, color, offset=(0,0), alpha=False):
    iso_x = (x - y) * VOXEL_SIZE / 2
    iso_y = (x + y) * VOXEL_SIZE / 4 - z * VOXEL_SIZE / 2
    hex_radius = VOXEL_SIZE / 2
    hex_center_x = iso_x + hex_radius
    hex_center_y = iso_y + hex_radius / 2
    hex_points = []
    bad_points = 0
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        point_x = hex_center_x + hex_radius * math.cos(angle_rad)
        point_y = hex_center_y + hex_radius * math.sin(angle_rad)
        hex_points.append((point_x + offset[0], point_y + offset[1]))
    for i in hex_points:
        x, y = i
        if x > WINDOW_WIDTH or x < 0 or y > WINDOW_HEIGHT or y < 0:
            bad_points += 1
    if bad_points >= 6:
        return
    if not alpha:
        pygame.draw.polygon(screen, color, hex_points)
        return gfxdraw.aapolygon(screen, hex_points, (0,0,0))
    else:
        red = (color >> 16) & 0xff
        green = (color >> 8) & 0xff
        blue = color & 0xff
        pygame.draw.polygon(screen, (red, green, blue, 255), hex_points)
        return gfxdraw.aapolygon(screen, hex_points, (0,0,0, 255))

def drawBlit(screen, preblits, VOXEL_SIZE, x, y, z, block, offset=(0,0)):
    iso_x = (x - y) * VOXEL_SIZE / 2
    iso_y = (x + y) * VOXEL_SIZE / 4 - z * VOXEL_SIZE / 2
    iso_x += offset[0]
    iso_y += offset[1]
    if is_offscreen(preblits[block], screen, (iso_x, iso_y)):
        # print("bad blit at %d, %d" % (iso_x, iso_y)) # laggy as fuck when iterating over more than 3 blocks
        return
    screen.blit(preblits[block], (iso_x, iso_y))