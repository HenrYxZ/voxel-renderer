from math import cos, sin
from numba import njit
import numpy as np


import utils


def render(screen_width, screen_height, color_channels, terrain, camera):
    return render_terrain_jit(
        screen_width, screen_height, color_channels, terrain.height_map,
        terrain.color_map, camera.position, camera.theta, camera.z_far,
        camera.fov, camera.window_height, camera.topdown, camera.horizon
    )


@njit(fastmath=True)
def render_terrain_jit(
    screen_width, screen_height, color_channels, height_map,
    color_map, position, theta, z_far,
    fov, window_height, cam_topdown, horizon
):
    # Clear screen
    screen = np.zeros(
        (screen_height, screen_width, color_channels), dtype=np.uint8
    )
    screen[::] = np.array((36, 36, 56), dtype=np.uint8)
    h, w = height_map.shape
    size = min(h, w)
    # # Camera z_far cannot be greater than texture size!
    if z_far >= size:
        z_far = size - 1
    for i in range(screen_width):
        current_angle_portion = fov * (i / screen_width)
        local_angle = -fov / 2 + current_angle_portion
        current_angle = theta + local_angle
        direction = np.array([cos(current_angle), sin(current_angle)])
        # The distance between each sample along the ray
        max_projected_height = 0
        for j in range(1, int(z_far)):
            current_pos = direction * j + cam_topdown
            s, t = utils.wrap_repeat_coords(
                int(current_pos[0]), int(current_pos[1]), w, h
            )
            height = height_map[t, s]
            # Project the world height into window
            proj_dist = j
            proj_height = (height - position[1]) / proj_dist
            # Project window height into screen height
            proj_height = int(
                (proj_height / window_height + 0.5) * (screen_height - 1)
            )
            proj_height += horizon
            proj_height = int(min(max(proj_height, 0), screen_height - 1))
            if proj_height > max_projected_height:
                color = color_map[t, s]
                # Paint pixels from last max to new height
                screen[max_projected_height:(proj_height + 1), i] = color
                max_projected_height = proj_height
    return screen
