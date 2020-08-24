# class and helper function for scene def
import numpy as np

class SceneReader:
    def __init__(self, file_name):
        # assume scene file is in current dir
        self.file_name = './' + file_name
        self.transform = []
        self.vertices = []
        

    def read_file(self, file_name = None):
        if file_name is None:            
            file_name = self.file_name

        scene_def = open(file_name, 'r')
        for line in scene_def:
            if len(line) <= 1 or line[0] == "#":
                continue

            print(line.split())

        scene_def.close()
