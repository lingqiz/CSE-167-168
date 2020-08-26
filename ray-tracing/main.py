import numpy as np
import sys 
import scene
import ray_trace
import multiprocessing
import matplotlib.pyplot as plt

def render_row(ray_tracer, idh):
    image_row = np.zeros([ray_tracer.scene.width, 3])
    for idw in range(0, ray_tracer.scene.width):
        origin, direction = ray_tracer.camera_ray(idh, idw)        
        image_row[idw, :] = ray_tracer.single_ray(origin, direction, depth=1)

    return image_row   

def ray_trace_parallel(ray_tracer, num_process = 4, show_image=True):
    print('Parallel Ray Tracing')

    image_rows = []
    with multiprocessing.Pool(num_process) as pool:
        arg_list = zip([ray_tracer] * ray_tracer.scene.height, range(0, ray_tracer.scene.height))
        image_rows = pool.starmap(render_row, arg_list)    
        
    for idh in range(0, ray_tracer.scene.height):
        ray_tracer.image[idh, :, :] = image_rows[idh]

    if show_image:        
        plt.imshow(ray_tracer.image)
        plt.show()

if __name__ == '__main__':    
    if len(sys.argv) != 2:
        raise ValueError('Incorrect Number of Input Argument')

    file_name = str(sys.argv[1])
    reader = scene.SceneReader(file_name)
    scene_config = reader.read_file()

    ray_tracer = ray_trace.RayTracer(scene_config)
    # ray_tracer.ray_trace(show_image=True)
        
    ray_trace_parallel(ray_tracer, show_image=True)
    