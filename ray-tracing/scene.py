# class and helper function for scene def
import numpy as np

class SceneReader:    
    @staticmethod
    def def_size(input, reader, scene):
        scene.width = int(input[0])
        scene.width = int(input[1])

    @staticmethod
    def def_cam(input, reader, scene):
        scene.cam_init(input)

    # class interpreter map
    def_mapping = {'size' : def_size, 'camera' : def_cam}

    def __init__(self, file_name):
        # assume scene file is in current dir
        self.file_name = './' + file_name
        self.transform = []

        self.diffuse = np.zeros(3)
        self.specular = np.zeros(3)
        self.emission = np.zeros(3)
        self.shininess = 0.0

        self.scene = Scene()
        
    def read_file(self, file_name = None):
        if file_name is None:            
            file_name = self.file_name

        scene_def = open(file_name, 'r')
        for line in scene_def:
            if len(line) <= 1 or line[0] == "#":
                continue

            arg_list = line.split()            
    

        scene_def.close()

class Scene:
    @staticmethod
    def norm_vec(vec):
        return vec / np.linalg.norm(vec)

    def __init__(self):
        self.width = 0
        self.height = 0
        
        # default attenuation term and ambient light
        self.light_attenu = np.array([1.0, 0.0, 0.0])
        self.ambient = np.array([0.2, 0.2, 0.2])

        self.camera = {}
        self.vertices = []
        self.lights = []
        
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

        