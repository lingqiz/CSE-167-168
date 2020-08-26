import numpy as np
import sys 
import scene
import ray_trace
import multiprocessing
import matplotlib.pyplot as plt

if __name__ == '__main__':    
    if len(sys.argv) != 3:
        raise ValueError('Incorrect Number of Input Argument')

    file_name = str(sys.argv[1])
    reader = scene.SceneReader(file_name)
    scene_config = reader.read_file()

    ray_tracer = ray_trace.RayTracer(scene_config)
    ray_tracer.ray_trace(int(sys.argv[2]) != 0, show_image=True)
