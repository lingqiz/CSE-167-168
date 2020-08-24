import numpy as np
import sys 
import scene


if len(sys.argv) != 2:
    raise ValueError('Incorrect Number of Input Argument')

file_name = str(sys.argv[1])
scene.SceneReader(file_name).read_file()