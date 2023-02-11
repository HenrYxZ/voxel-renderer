from pyglet.window import key


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
    key.RIGHT: TURN_RIGHT
}
# ----


def get_actions(keys):
    actions = set()
    for key, action in keys_mapping.items():
        if keys[key]:
            actions.add(action)
    return actions
