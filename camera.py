from math import sin, cos, pi, radians
from pyglet.math import Vec3


from constants import *


class Camera:
    def __init__(
        self, position=Vec3(512.0, 100.0, 512.0), phi=pi/2, theta=pi/2, z_far=300,
        fov=90, focus_distance=1, aperture=1
    ):
        """
        Initialize a camera

        Args:
            position (Vec3): The position in 3D space
            phi (float): Angle of the camera in the x-axis given in rads
            theta (float): Angle of the camera in the y-axis given in rads
            up (Vec3): Up vector in 3D space
            z_far (float): Limit to where how far the camera can see in the
                terrain in camera coordinates
            fov (float): Field of view given in degrees
            focus_distance (float): Distance from the camera to the projection
                window.
            aperture (float): Half of the height of the viewing window in world
                size.
        """
        self.position = position
        self.phi = phi
        self.theta = theta
        self.up = Vec3(0.0, 1.0, 0.0)
        self.z_far = z_far
        self.fov = radians(fov)
        self.focus_distance = focus_distance
        self.aperture = aperture
        # The idea on having this values as attributes is to eventually be able
        # to change speed by applying a force for example
        self.speed = SPEED
        self.strife_speed = STRIFE_SPEED
        self.turn_speed = TURN_SPEED

    @property
    def direction(self):
        return Vec3(
            sin(-self.phi) * cos(self.theta),
            cos(-self.phi),
            -sin(-self.phi) * sin(self.theta)
        )

    @property
    def right(self):
        return self.up.cross(self.direction).normalize()
