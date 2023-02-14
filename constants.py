FRAME_WIDTH = 320
FRAME_HEIGHT = 200
COLOR_CHANNELS = 3
SPEED = 5                   # Speed of the camera moving forward
STRIFE_SPEED = 3            # Speed of the camera strife
TURN_SPEED = 1.6            # Speed of the camera turning left and right
SENSITIVITY = 10            # Speed of the camera turning up and down
TERRAIN_MAX_HEIGHT = 70     # Max height in the terrain in world units
MAX_COLOR_VALUE = 255

# Input codes
MOVE_FORWARD = 0
MOVE_BACKWARD = MOVE_FORWARD + 1
TURN_LEFT = MOVE_BACKWARD + 1
TURN_RIGHT = TURN_LEFT + 1
TURN_UP = TURN_RIGHT + 1
TURN_DOWN = TURN_UP + 1
STRIFE_LEFT = TURN_DOWN + 1
STRIFE_RIGHT = STRIFE_LEFT + 1
