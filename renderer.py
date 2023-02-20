from math import cos, sin
from numba import njit
import numpy as np
from pyglet.math import Vec2

import utils


class Renderer:
    def __init__(self, screen_width, screen_height, color_channels):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color_channels = color_channels

    def create_samples(self, camera):
        """
        Create all samples from the terrain needed for the renderer at once.

        Args:
            camera (Camera):  The camera from where to render

        Returns:
            ndarray: Array of 2D samples for independent position/rotation
        """
        num_samples = camera.z_far * self.screen_width
        arr = np.zeros([num_samples, 2])
        for i in range(self.screen_width):
            current_angle = camera.fov * (i / self.screen_width)
            direction = Vec2(cos(current_angle), sin(current_angle))
            for j in range(camera.z_far):
                arr[j + camera.z_far * i] = direction * j
        return arr

    def render_terrain(self, terrain, camera):
        """
        Render the terrain in a numpy array of pixels
        Args:
            terrain (Terrain): The terrain that will be rendered
            camera (Camera): The camera from where to render
        Returns:
            ndarray: Array of computed pixels
        """
        arr = np.zeros(
            [
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
                current_pos = direction * distance + Vec2(
                    camera.position.x, camera.position.z
                )
                s, t = utils.wrap_repeat_coords(
                    int(current_pos.x), int(current_pos.y), w, h
                )
                height = terrain.height_map[t, s]
                # Project the world height into window
                proj_dist = j
                proj_height = (height - camera.position[1]) / proj_dist
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
                    arr[max_projected_height:(proj_height + 1), i] = color
                    max_projected_height = proj_height
        return arr

    def render_from_samples(self, samples, terrain, camera):
        # Translate to camera position
        samples = samples + camera.topdown_to_array()
        # Rotate to camera angle
        theta = camera.theta
        rot_mat = np.array([
            [cos(theta), -sin(theta)], [sin(theta), cos(theta)]
        ])
        samples = np.dot(rot_mat, samples)
        # Use horizon
        # Wrap to texture
        h, w = terrain.height_map.shape
        size = min(h, w)
        samples = np.where(samples >= size, samples - size, samples)
        samples = np.where(samples < 0, samples + size, samples)
        # Get height
        for sample in samples:
            pass
        # Project

        # Order by z
        # Render
        arr = np.zeros(
            [self.screen_height, self.screen_width, self.color_channels],
            dtype=np.uint8
        )
        return arr


def render(screen, terrain, camera):
    render_terrain_jit(
        screen, terrain.height_map, terrain.color_map, camera.position,
        camera.theta, camera.z_far, camera.fov, camera.aperture,
        camera.topdown
    )


@njit
def render_terrain_jit(
    screen, height_map, color_map, position, theta, z_far, fov, aperture,
    cam_topdown
):
    screen_height, screen_width, _ = screen.shape
    h, w = height_map.shape
    # size = min(h, w)
    # # Camera z_far cannot be greater than texture size!
    # if z_far >= size:
    #     z_far = size - 1
    for i in range(screen_width):
        current_angle_portion = fov * (i / screen_width)
        local_angle = -fov / 2 + current_angle_portion
        current_angle = theta + local_angle
        ray_length = z_far / cos(local_angle)
        direction = np.array([cos(current_angle), sin(current_angle)])
        # The distance between each sample along the ray
        ray_delta = ray_length / z_far
        max_projected_height = 0
        for j in range(1, int(z_far)):
            distance = j * ray_delta
            current_pos = direction * distance + cam_topdown
            s, t = utils.wrap_repeat_coords(
                int(current_pos[0]), int(current_pos[1]), w, h
            )
            height = height_map[t, s]
            # Project the world height into window
            proj_dist = j
            proj_height = (height - position[1]) / proj_dist
            # Project window height into screen height
            proj_height = min(max(proj_height, -aperture), aperture)
            proj_height = int(
                (
                        proj_height / (2 * aperture) + 0.5
                ) * (screen_height - 1)
            )
            if proj_height > max_projected_height:
                color = color_map[t, s]
                # Paint pixels from last max to new height
                screen[max_projected_height:(proj_height + 1), i] = color
                max_projected_height = proj_height
