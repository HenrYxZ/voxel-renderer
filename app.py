import numpy as np
from PIL import Image
import pyglet
from pyglet.window import FPSDisplay
from pyglet.window import key


from camera import Camera
from control import FPSControl
from constants import *
from renderer import render, Renderer
from terrain import Terrain
import utils


class App(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(
            FRAME_WIDTH, FRAME_HEIGHT, caption="Voxel Renderer", *args, **kwargs
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
        height_map = (
            np.array(height_img, dtype=np.uint8) / MAX_COLOR_VALUE
        ) * TERRAIN_MAX_HEIGHT
        color_map = np.array(color_img, dtype=np.uint8)
        self.terrain = Terrain(height_map, color_map)
        self.renderer = Renderer(FRAME_WIDTH, FRAME_HEIGHT, COLOR_CHANNELS)
        self.timer = utils.Timer()
        self.fps_display = FPSDisplay(self)
        self.pause = False

    def on_update(self, dt):
        # Handle input with the camera control
        actions = utils.get_actions(self.keys)
        self.camera_control.handle_actions(actions, dt)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.P:
            print(self.camera.position)
        super(App, self).on_key_press(symbol, modifiers)

    def on_draw(self, **kwargs):
        self.clear()

        # self.timer.start()
        render(self.frame, self.terrain, self.camera)
        # self.timer.stop()
        # print(self.timer)

        # self.frame = self.renderer.render_terrain(self.terrain, self.camera)

        # self.timer.start()
        self.image_data.set_data("RGB", 3 * FRAME_WIDTH, self.frame.tobytes())
        self.image_data.blit(0, 0)
        # self.timer.stop()
        # print(self.timer)

        # Debugging
        self.fps_display.draw()
