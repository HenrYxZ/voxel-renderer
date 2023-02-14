from math import cos, sin
import numpy as np
from pyglet.math import Vec2

import utils


class Renderer:
    def __init__(self, screen_width, screen_height, color_channels):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color_channels = color_channels

    def render_terrain(self, terrain, camera):
        """
        Render the terrain in a numpy array of pixels

        Args:
            terrain (Terrain): The terrain that will be rendered
            camera (Camera): The camera from where to render

        Returns:
            ndarray: Array of computed pixels
        """
        arr = np.zeros([
            self.screen_height, self.screen_width, self.color_channels],
            dtype=np.uint8
        )
        h, w = terrain.height_map.shape
        for i in range(self.screen_width):
            current_angle_portion = camera.fov * (i / self.screen_width)
            local_angle = -camera.fov / 2 + current_angle_portion
            current_angle = camera.theta + local_angle
            ray_length = camera.z_far / cos(local_angle)
            direction = Vec2(cos(current_angle), sin(current_angle))
            # The distance between each sample along the ray
            ray_delta = ray_length / camera.z_far
            max_projected_height = 0
            for j in range(1, int(camera.z_far)):
                distance = j * ray_delta
                current_pos = direction * distance
                s, t = utils.wrap_repeat_coords(
                    int(current_pos.x), int(current_pos.y), w, h
                )
                height = terrain.height_map[t, s]
                # Project the world height into window
                proj_dist = j
                proj_height = (height - camera.position.y) / proj_dist
                # Project window height into screen height
                proj_height = np.clip(
                    proj_height, -camera.aperture, camera.aperture
                )
                proj_height = int(
                    (
                        proj_height / (2 * camera.aperture) + 0.5
                    ) * (self.screen_height - 1)
                )
                if proj_height > max_projected_height:
                    color = terrain.color_map[t, s]
                    # Paint pixels from last max to new height
                    arr[max_projected_height:(proj_height+1), i] = color
                    max_projected_height = proj_height
        return arr
