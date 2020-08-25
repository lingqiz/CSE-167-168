# class and helper function for scene def
import numpy as np
from read_helper import *

class Scene:

    @staticmethod
    def norm_vec(vec):
        return vec / np.linalg.norm(vec)

    def __init__(self):
        # basic setup
        self.width = 0
        self.height = 0
        self.depth = 5
        self.output_name = 'ray_tracing'
        
        # default attenuation
        self.light_attenu = np.array([1.0, 0.0, 0.0])        

        # elements of the scene
        self.camera = {}
        self.lights = []
        self.vertices = []
        self.spheres = []
        self.triangles = []        
        
    def cam_init(self, input):
        input = [float(coor) for coor in input]
        camera = {}

        cam_from = np.array(input[0:3])
        camera['loc'] = cam_from

        cam_at   = np.array(input[3:6])
        cam_up   = np.array(input[6:9])

        camera['fovy']  = input[-1]

        # camera in the -z direction
        camera['dir'] = self.norm_vec(cam_at - cam_from)        

        # construct coordinate frame
        camera['u'] = self.norm_vec(np.cross(cam_up, camera['dir']))
        camera['v'] = self.norm_vec(np.cross(camera['dir'], camera['u']))

        self.camera = camera

    def triangle_init(self, input, mtx, material):
        self.triangles.append({'ver_index':input, 'transform':mtx, **material})


class SceneReader:
    
    # class interpreter map
    def_mapping = {'size':def_size, 'camera':def_cam, 'maxdepth':def_depth, 'output':def_filename, \
        'directional':def_dirlight, 'point':def_ptlight, 'pushTransform':def_push, 'popTransform':def_pop, \
        'translate':def_translate, 'rotate':def_rotation, 'scale':def_scale, 'sphere': def_sphere, \
        'tri':def_triangle, 'vertex':def_vertex}
    
    def __init__(self, file_name):
        # assume scene file is in current dir
        self.file_name = './' + file_name
        self.transform = [np.eye(4)]

        self.material = {'ambient':0.2*np.ones(3), 'diffuse':np.zeros(3), 'specular':np.zeros(3), \
                        'emission':np.zeros(3), 'shininess':np.array(0.0)}
        
        self.scene = Scene()
        
    def read_file(self, file_name = None):
        if file_name is None:            
            file_name = self.file_name

        scene_def = open(file_name, 'r')
        for line in scene_def:            
            if len(line) <= 1 or line[0] == "#":
                continue

            arg_list = line.split()
            arg_key = arg_list[0]

            if arg_key in self.def_mapping.keys():                
                self.def_mapping[arg_key](arg_list[1:], self)

            elif arg_key in self.material.keys():
                self.material[arg_key] = np.array([float(val) for val in arg_list[1:]])

        scene_def.close()
        return self.scene
        