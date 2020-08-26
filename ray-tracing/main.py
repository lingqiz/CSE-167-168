import numpy as np
import sys 
import scene
import ray_trace
import multiprocessing
import matplotlib.pyplot as plt

if __name__ == '__main__':    
    if len(sys.argv) != 2:
        raise ValueError('Incorrect Number of Input Argument')

    file_name = str(sys.argv[1])
    reader = scene.SceneReader(file_name)
    scene_config = reader.read_file()

    ray_tracer = ray_trace.RayTracer(scene_config)
    # ray_tracer.ray_trace(show_image=True)
        
    ray_tracer.ray_trace_parallel(show_image=True)
    
    