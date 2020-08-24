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