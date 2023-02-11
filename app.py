import numpy as np
import pyglet
from pyglet.window import key


from camera import Camera
from control import FPSControl
from constants import *


import utils


class App(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(
            FRAME_WIDTH, FRAME_HEIGHT, caption="Voxel Renderer", *args, **kwargs
        )
        self.keys = key.KeyStateHandler()
        self.frame = np.zeros([FRAME_HEIGHT, FRAME_WIDTH, COLOR_CHANNELS])
        self.image_data = pyglet.image.ImageData(
            FRAME_WIDTH, FRAME_HEIGHT, "rgb", self.frame.tobytes()
        )
        self.camera = Camera()
        self.camera_control = FPSControl(self.camera)
        self.push_handlers(self.keys)

    def on_update(self, dt):
        # Handle input with the camera control
        actions = utils.get_actions(self.keys)
        self.camera_control.handle_actions(actions, dt)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.P:
            print(print(self.camera.position))
        super(App, self).on_key_press(symbol, modifiers)

    def on_draw(self, **kwargs):
        self.clear()
        self.image_data.set_data("rgb", 3 * FRAME_WIDTH, self.frame.tobytes())
        self.image_data.blit(0, 0)
