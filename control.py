from math import pi
import numpy as np


from constants import *


class Control:
    def __init__(self, target):
        """
        The control for a camera handles input conveniently
        Args:
            target (Camera): The camera that you want to control
        """
        self.target = target

    def handle_keys(self, keys, dt):
        pass


class FPSControl(Control):
    def handle_actions(self, actions, dt):
        print(self.target.direction)
        if MOVE_FORWARD in actions:
            self.target.position += (
                self.target.direction * self.target.speed * dt
            )
        if MOVE_BACKWARD in actions:
            self.target.position -= (
                self.target.direction * self.target.speed * dt
            )
        if STRIFE_LEFT in actions:
            self.target.position -= (
                self.target.right * self.target.strife_speed * dt
            )
        if STRIFE_RIGHT in actions:
            self.target.position += (
                self.target.right * self.target.strife_speed * dt
            )
        if TURN_LEFT in actions:
            self.target.theta -= self.target.turn_speed * dt
        if TURN_RIGHT in actions:
            self.target.theta += self.target.turn_speed * dt
        if TURN_DOWN in actions:
            self.target.phi -= self.target.sensitivity * dt
        if TURN_UP in actions:
            self.target.phi += self.target.sensitivity * dt
        # Limit phi to be in the [pi/4, 3pi/4] range
        self.target.phi = np.clip(self.target.phi, pi / 4, 3 * pi / 4)
        # Keep theta between 0 and 2 pi
        if self.target.theta > 2 * pi:
            self.target.theta -= 2 * pi
        if self.target.theta < 0:
            self.target.theta += 2 * pi
