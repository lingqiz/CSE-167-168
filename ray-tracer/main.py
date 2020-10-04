import numpy as np
import sys 
import scene
import ray_trace
import multiprocessing

if __name__ == '__main__':
    if len(sys.argv) <= 2 or len(sys.argv) > 4:
        raise ValueError('Incorrect Number of Input Argument')
    
    file_name = str(sys.argv[1])
    reader = scene.SceneReader(file_name)
    scene_config = reader.read_file()
    ray_tracer = ray_trace.RayTracer(scene_config)
    ray_tracer.ray_trace(parallel=True, show_image=False, num_process=int(sys.argv[2]))

    if len(sys.argv) == 4:
        ray_tracer.show_image()
    
    if len(sys.argv) == 3 or int(sys.argv[3]):        
        # save the image both as npy and png file 
        np.save('./render_image.npy', ray_tracer.image)
        ray_tracer.save_image()