from numba import njit
import numpy as np
from pyglet.window import key
import time


from constants import *


# ----
# Input
keys_mapping = {
    key.W: MOVE_FORWARD,
    key.S: MOVE_BACKWARD,
    key.Q: TURN_LEFT,
    key.E: TURN_RIGHT,
    key.A: STRIFE_LEFT,
    key.D: STRIFE_RIGHT,
    key.UP: TURN_UP,
    key.DOWN: TURN_DOWN,
    key.LEFT: TURN_LEFT,
    key.RIGHT: TURN_RIGHT,
    key.R: MOVE_UP,
    key.F: MOVE_DOWN
}
# ----


def get_actions(keys):
    actions = set()
    for value, action in keys_mapping.items():
        if keys[value]:
            actions.add(action)
    return actions


@njit(fastmath=True)
def wrap_repeat_coords(old_s, old_t, w, h):
    # Ensure s and t are in ranges of the textures (wrap repeat)
    s = old_s
    t = old_t
    while s < 0:
        s += w
    if s >= w:
        s %= w
    while t < 0:
        t += h
    if t >= h:
        t %= h
    return s, t


@njit(fastmath=True)
def sample_tex(u, v, tex):
    h, w, _ = tex.shape
    if u > 1:
        u -= 1
    j = min(max(0, round(v * (h - 1))), h - 1)
    i = round(u * (w - 1))
    return tex[h - 1 - j, i]


@njit
def normalize(arr):
    """
    Normalize a vector using numpy.
    Args:
        arr (ndarray): Input vector
    Returns:
        ndarray: Normalized input vector
    """
    norm = np.linalg.norm(arr)
    if norm == 0:
        return arr
    return arr / norm


@njit
def lerp(a, b, t):
    return (1 - t) * a + t * b


def humanize_time(secs):
    minutes, secs = divmod(secs, 60)
    hours, minutes = divmod(minutes, 60)
    return '%02d:%02d:%02d' % (hours, minutes, secs)


class Timer:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.elapsed_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time

    def __str__(self):
        return f"{self.elapsed_time * 1000:,} ms"
