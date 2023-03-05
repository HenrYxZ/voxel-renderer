import numpy as np
from PIL import Image
import pyglet
from pyglet.window import FPSDisplay
from pyglet.window import key


from camera import Camera
from control import FPSControl
from constants import *
from fixed_resolution import FixedResolution
from renderer import render
from terrain import Terrain
import utils


IMG_FORMAT = "RGB"
PITCH = FRAME_WIDTH * COLOR_CHANNELS
VERTICAL_PADDING = 20


class App(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(
            fullscreen=True, caption="Voxel Renderer", vsync=False,
            *args, **kwargs
        )
        self.keys = key.KeyStateHandler()
        self.frame = np.zeros(
            [FRAME_HEIGHT, FRAME_WIDTH, COLOR_CHANNELS], dtype=np.uint8
        )
        self.image_data = pyglet.image.ImageData(
            FRAME_WIDTH, FRAME_HEIGHT, "rgb", self.frame.tobytes()
        )
        self.camera = Camera()
        self.camera_control = FPSControl(self.camera)
        self.push_handlers(self.keys)
        height_img = Image.open("maps/D1.png")
        color_img = Image.open("maps/C1W.png").convert('RGB')
        env_img = Image.open("maps/env.jpg")
        height_map = (
            np.array(height_img, dtype=np.uint8) / MAX_COLOR_VALUE
        ) * TERRAIN_MAX_HEIGHT
        color_map = np.array(color_img, dtype=np.uint8)
        self.env_map = np.array(env_img, dtype=np.uint8)
        self.terrain = Terrain(height_map, color_map)
        self.timer = utils.Timer()
        self.fps_display = FPSDisplay(self)
        self.fixed_viewport = FixedResolution(
            self, FRAME_WIDTH, FRAME_HEIGHT + 2 * VERTICAL_PADDING
        )
        self.set_mouse_visible(False)

    def on_update(self, dt):
        # Handle input with the camera control
        actions = utils.get_actions(self.keys)
        self.camera_control.handle_actions(actions, dt)
        # self.timer.start()
        self.frame = render(
            FRAME_WIDTH, FRAME_HEIGHT, COLOR_CHANNELS, self.terrain,
            self.camera, self.env_map
        )
        # self.timer.stop()
        # print(self.timer)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.P:
            print(self.camera)
        if symbol == key.C:
            pyglet.image.get_buffer_manager().get_color_buffer().save(
                'docs/screenshot.png'
            )
        super(App, self).on_key_press(symbol, modifiers)

    def on_draw(self, **kwargs):
        self.clear()

        with self.fixed_viewport:
            # self.timer.start()
            self.image_data.set_data(IMG_FORMAT, PITCH, self.frame.tobytes())
            self.image_data.blit(0, VERTICAL_PADDING)
            # self.timer.stop()
            # print(self.timer)

            # Debugging
            self.fps_display.draw()
