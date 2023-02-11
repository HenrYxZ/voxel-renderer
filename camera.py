from math import sin, cos, pi
from pyglet.math import Vec3


from constants import *


class Camera:
    def __init__(self, position=Vec3(0.0, 0.0, 0.0), phi=pi/2, theta=pi/2):
        """
        Initialize a camera

        Args:
            position (Vec3): The position in 3D space
            phi (float): Angle of the camera in the x-axis
            theta (float): Angle of the camera in the y-axis
        """
        self.position = position
        self.phi = phi
        self.theta = theta
        self.up = Vec3(0.0, 1.0, 0.0)
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
