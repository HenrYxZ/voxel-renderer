import numpy as np
from numpy import pi
import unittest


from constants import *
from camera import Camera
from control import FPSControl


class FPSControlTestCase(unittest.TestCase):
    def setUp(self):
        position = np.array([512.0, 100.0, 512.0])
        phi = pi / 2.0
        theta = pi / 2.0
        up = np.array([0.0, 1.0, 0.0])
        z_far = 600
        fov = 90.0
        proj_dist = 1.0
        window_height = 2.0

        self.camera = Camera(
            position, phi, theta, up, z_far, fov, proj_dist, window_height
        )

    def test_turn_horizontal_and_move(self):
        control = FPSControl(self.camera)
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
