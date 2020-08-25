import numpy as np

def def_size(input, reader):
    reader.scene.width = int(input[0])
    reader.scene.height = int(input[1])

def def_cam(input, reader):
    reader.scene.cam_init(input)

def def_depth(input, reader):
    reader.scene.depth = int(input[-1])

def def_filename(input, reader):
    reader.scene.output_name = input[-1]

def def_dirlight(input, reader):
    input = [float(val) for val in input]
    light_dir = np.array(input[0:3] + [0])
    light_spc = np.array(input[3:])
    reader.scene.lights.append((light_dir, light_spc))
    
def def_ptlight(input, reader):
    input = [float(val) for val in input]
    light_dir = np.array(input[0:3] + [1])
    light_spc = np.array(input[3:])
    reader.scene.lights.append((light_dir, light_spc))

def def_push(input, reader):
    mtx_stack = reader.transform
    mtx_stack.append(mtx_stack[-1])

def def_pop(input, reader):
    reader.transform.pop(-1)

def def_translate(input, reader):
    input = [float(val) for val in input]
    translate_mtx = np.eye(4)
    translate_mtx[0:3, -1] = np.array(input)
    
    reader.transform[-1] = reader.transform[-1] @ translate_mtx    

def def_scale(input, reader):
    input = [float(val) for val in input] + [1.0]
    reader.transform[-1] = reader.transform[-1] @ np.diag(input)    

def def_rotation(input, reader):
    input = [float(val) for val in input]

    axis = np.array(input[0:3])
    axis = axis / np.norm(axis)
    angle = input[-1] / 180.0 * np.pi 
    
    dual_mtx = np.array([[0, -axis[-1], axis[1]], \
                        [axis[-1], 0, -axis[0]], \
                        [-axis[1], axis[0], 0]])

    rotate_mtx = np.cos(angle) * np.eye(3) + (1 - np.cos(angle)) * np.outer(axis, axis) + np.sin(angle) * dual_mtx
    full_mtx = np.eye(4)
    full_mtx[0:3, 0:3] = rotate_mtx
    
    reader.transform[-1] = reader.transform[-1] @ full_mtx    

def def_vertex(input, reader):
    reader.scene.vertices.append(tuple([float(val) for val in input]))

def def_sphere(input, reader):
    input = [float(val) for val in input]    
    reader.scene.sphere_init(input, reader.transform[-1], reader.material.copy())

def def_triangle(input, reader):
    input = [int(val) for val in input]
    reader.scene.triangle_init(input, reader.transform[-1], reader.material.copy())