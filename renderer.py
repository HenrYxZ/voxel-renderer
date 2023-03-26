from math import cos, sin
from numba import njit
import numpy as np


import utils


def render(
    screen_width, screen_height, color_channels, terrain, camera
):
    return render_terrain_jit(
        screen_width, screen_height, color_channels, terrain.height_map,
        terrain.color_map, camera.position, camera.theta, camera.z_far,
        camera.fov, camera.proj_dist, camera.proj_height, camera.topdown,
        camera.horizon
    )


@njit(fastmath=True)
def render_terrain_jit(
    screen_width, screen_height, color_channels, height_map,
    color_map, position, theta, z_far,
    fov, proj_dist, proj_height, cam_topdown, horizon
):
    # Clear screen
    screen = np.ones(
        (screen_height, screen_width, color_channels), dtype=np.uint8
    )
    bg_color = np.array([154, 192, 238], dtype=np.uint8)
    screen = screen * bg_color

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
            proj_h = (height - position[1]) * proj_dist / j
            # Project window height into screen height
            proj_h = (proj_h / proj_height) * screen_height
            proj_h += horizon
            proj_h = int(min(max(proj_h, 0), screen_height - 1))
            if proj_h > max_projected_height:
                color = color_map[t, s]
                # For far away pixels add fog by interpolating with background
                fog_start = 0.8 * z_far    # start fog at 80% of z_far
                if j > fog_start:
                    a = color.astype(np.float64) / 255.0
                    b = bg_color.astype(np.float64) / 255.0
                    t = (j - fog_start) / (z_far - fog_start)
                    interp_col = utils.lerp(a, b, t) * 255.0
                    color = interp_col.astype(np.uint8)
                # Paint pixels from last max to new height
                screen[max_projected_height:(proj_h + 1), i] = color
                max_projected_height = proj_h
    return screen
