import numpy as np

class RayTracer:
    
    def __init__(self, scene_config):
        self.scene = scene_config
        self.image = np.zeros([scene_config.width])