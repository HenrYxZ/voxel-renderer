from math import sin, cos, pi, radians
import numpy as np


from constants import *


class Camera:
    def __init__(
        self,
        position=np.array([512.0, 88.0, 512.0]),
        up=np.array([0.0, 1.0, 0.0]),
        theta=pi/2, z_far=800, fov=90.0, proj_dist=1.0, proj_height=0.35,
        horizon=HORIZON
    ):
        """
        Initialize a camera

        Args:
            position (ndarray): The position in 3D space
            up (ndarray): Unit vector representing the up direction in 3D space
            theta (float): Angle of the camera in the y-axis given in rads
            z_far (float): Limit to where how far the camera can see in the
                terrain in camera coordinates. z_far CANNOT be greater than the
                texture size
            fov (float): Field of view given in degrees
            proj_dist (float): Distance to the projection window
            proj_height (float): Height of the viewing projection window in
                world's units
            horizon (float): Offset height in pixels at which that scrolls the
                projected image up or down
        """
        self.position = position
        self.up = up
        self.theta = theta
        self.z_far = z_far
        self.fov = radians(fov)
        self.proj_dist = proj_dist
        self.proj_height = proj_height
        self.horizon = horizon
        # The idea on having this values as attributes is to eventually be able
        # to change speed by applying a force for example
        self.speed = SPEED
        self.strife_speed = STRIFE_SPEED
        self.vertical_speed = VERTICAL_SPEED
        self.turn_speed = TURN_SPEED
        self.sensitivity = SENSITIVITY

    @property
    def s(self):
        return self.position[0]

    @property
    def t(self):
        return self.position[2]

    @property
    def direction(self):
        return np.array((cos(self.theta), 0.0, sin(self.theta)))

    @property
    def right(self):
        return np.array(
            (cos(self.theta + pi / 2.0), 0.0, sin(self.theta + pi / 2.0))
        )

    @property
    def topdown(self):
        """
        Get the top-down position of the camera to calculate terrain rendering
        and return it as a numpy 2D array.

        Returns:
            ndarray: 2D array with coordinates for terrain texture
        """
        return np.array([self.s, self.t])

    def __str__(self):
        str = ""
        for attribute, value in self.__dict__.items():
            str += f"{attribute}: {value}\n"
        return str