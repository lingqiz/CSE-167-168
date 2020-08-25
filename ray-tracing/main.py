import numpy as np
import sys 
import scene
import ray_trace


if len(sys.argv) != 2:
    raise ValueError('Incorrect Number of Input Argument')

file_name = str(sys.argv[1])
reader = scene.SceneReader(file_name)
scene_config = reader.read_file()

ray_trace.RayTracer(scene_config).ray_trace()