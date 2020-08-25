import numpy as np
import matplotlib.pyplot as plt

class RayTracer:
    
    @staticmethod
    def norm_vec(vec):
        return vec / np.linalg.norm(vec)

    @staticmethod
    def barycentric(normal, edge1, edge2, point, intersec):
        vec_cross = np.cross(normal, edge1)
        ap_normal = vec_cross / np.dot(vec_cross, edge2)
        ap_w = np.dot(-ap_normal, point)

        return np.dot(ap_normal, intersec) + ap_w     

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
        
        direction = self.norm_vec(alpha * camera['u'] + beta * camera['v'] - camera['dir'])
        return (camera['loc'], direction)

    def single_ray(self, origin, direction, depth):
        flag, t, surf, obj = self.intersection(origin, direction)
        if not flag:
            return np.zeros([1, 3])

        return obj['ambient']

    def intersection(self, origin, direction):
        # init   
        flag = False
        # ray = origin + t * direction
        t = float('inf')
        
        surf = None
        obj  = None

        # ray and sphere intersection test
        for sphere in self.scene.spheres:            
            sloc = sphere['loc']
            radi = sphere['radius']

            a = np.dot(direction, direction)
            b = 2 * np.dot(direction, origin - sloc)
            c = np.dot(origin - sloc, origin - sloc) - (radi ** 2)

            root = np.roots([a, b, c])
            root = np.sort(root[np.logical_and(np.isreal(root), root > 0)])
            
            if len(root) > 0 and root[0] < t:
                flag = True
                t = root[0]
                                
                surf = self.norm_vec(origin + t * direction - sloc)
                obj = sphere
                    
        # ray and triangle intersection test
        for triangle in self.scene.triangles:            
            vertice = self.scene.vertices[:, triangle['ver_index']]
            A = vertice[:, 0]
            B = vertice[:, 1]
            C = vertice[:, 2]

            normal = triangle['surface']
            
            # intersection test
            if np.abs(np.dot(direction, normal)) < (10 ** -10):
                continue            
            t_temp = (np.dot(A, normal) - np.dot(origin, normal)) \
                    / np.dot(direction, normal)
            if t_temp < 0 or t_temp > t:
                continue
                                    
            # test intersection inside the triangle
            intersec = origin + t_temp * direction
            a = self.barycentric(normal, C - B, A - C, C, intersec)
            b = self.barycentric(normal, A - C, B - A, A, intersec)
            c = 1 - a - b
            
            if a >= 0 and b >= 0 and c >= 0:
                flag = True
                t = t_temp

                surf = normal
                obj = triangle                

        return (flag, t, surf, obj)