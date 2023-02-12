from dataclasses import dataclass
import numpy as np


@dataclass
class Terrain:
    height_map:np.ndarray
    color_map:np.ndarray
