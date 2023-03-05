FRAME_WIDTH = 320
FRAME_HEIGHT = 200
COLOR_CHANNELS = 3
SPEED = 50                   # Speed of the camera moving forward
STRIFE_SPEED = 30            # Speed of the camera strife
VERTICAL_SPEED = 12          # Speed of the camera moving up and down
TURN_SPEED = 0.25            # Speed of the camera turning left and right
SENSITIVITY = 30            # Speed of the camera turning up and down
TERRAIN_MAX_HEIGHT = 150     # Max height in the terrain in world units
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
MOVE_UP = STRIFE_RIGHT + 1
MOVE_DOWN = MOVE_UP + 1
