import numpy as np
import matplotlib.pyplot as plt

class RayTracer:
    
    @staticmethod
    def norm_vec(vec):
        return vec / np.linalg.norm(vec)

    def __init__(self, scene):
        self.scene = scene
        self.image = np.zeros([scene.height, scene.width, 3])
        
    def ray_trace(self):
        # pixel-wise ray tracing
        denominator = (self.scene.height * self.scene.width) // 25
        count = 0
        print('Ray Tracing: ', end='', flush=True)

        for idh in range(0, self.scene.height):
            for idw in range(0, self.scene.width):
                origin, direction = self.camera_ray(idh, idw)
                self.image[idh, idw, :] = self.single_ray(origin, direction, depth=1)

                count = count + 1
                if count % denominator == 0:
                    print('>', end=' ', flush=True)
        print('Done! \n')

        plt.imshow(self.image)
        plt.show()

    def camera_ray(self, idh, idw):
        idh = idh + 0.5
        idw = idw + 0.5
        camera = self.scene.camera

        alpha = np.tan(camera['fovx_rad']/2) * \
                (idw - self.scene.width/2) / (self.scene.width/2)
        beta  = np.tan(camera['fovy_rad']/2) * \
                (self.scene.height/2 - idh) / (self.scene.height/2)
        
        direction = self.norm_vec(camera['dir'] + alpha * camera['u'] + beta * camera['v'])
        return (camera['loc'], direction)

    def single_ray(self, origin, direction, depth):
        return 0.2 * np.ones([1, 3])    