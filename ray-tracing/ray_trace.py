import numpy as np
import multiprocessing
import warnings
import matplotlib
import matplotlib.pyplot as plt
from tqdm import tqdm

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

    @staticmethod
    def shading_compute(light_dir, light_color, normal, half_vec, obj):
        n_dot_l = np.max([np.dot(normal, light_dir), 0.0])
        lambert = obj['diffuse'] * light_color * n_dot_l

        n_dot_h = np.max([np.dot(normal, half_vec), 0.0])
        phong = obj['specular'] * light_color * (n_dot_h ** obj['shininess'])

        return lambert + phong
 
    def __init__(self, scene):
        self.zero_thres = 1e-8
        self.delta_move = 1e-5
        self.scene = scene
        self.image = np.zeros([scene.height, scene.width, 3])

    def save_image(self):
        matplotlib.image.imsave('./' + self.scene.output_name, self.image)
        
    def ray_trace(self, parallel=False, show_image=True, num_process=2):
        if parallel:
            self.ray_trace_parallel(num_process=num_process, show_image=show_image)
        else:
            self.ray_trace_serial(show_image=show_image)

    # pixel-wise ray tracing
    def ray_trace_serial(self, show_image=True):    
        denominator = self.scene.height // 25
        count = 0
        print('Ray Tracing: ', end='', flush=True)

        for idh in range(0, self.scene.height):
            self.image[idh, :, :] = self.render_row(idh)
            
            count = count + 1
            if count % denominator == 0:
                print('>', end=' ', flush=True)

        print('Done! \n')

        if show_image:
            plt.imshow(self.image)
            plt.show()
    
    # pixel-wise ray tracing with parallel processing
    def ray_trace_parallel(self, num_process=2, show_image=True):
        print('Parallel Ray Tracing')

        image_rows = []
        with multiprocessing.Pool(num_process) as pool:        
            for row in tqdm(pool.imap(self.render_row, range(0, self.scene.height), \
                        chunksize=5), total=self.scene.height):                            
                image_rows.append(row)
            
        for idh in range(0, self.scene.height):
            self.image[idh, :, :] = image_rows[idh]

        if show_image:        
            plt.imshow(self.image)
            plt.show()
    
    # run ray tracing for each row
    def render_row(self, idh):
        image_row = np.zeros([self.scene.width, 3])
        for idw in range(0, self.scene.width):
            origin, direction = self.camera_ray(idh, idw)        
            image_row[idw, :] = self.single_ray(origin, direction, depth=0)

        return image_row

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
        if depth > self.scene.max_depth:
            return np.zeros(3)

        flag, t, surf, obj = self.intersection(origin, direction)
        intersection = origin + t * direction

        if not flag:
            return np.zeros(3)

        obj_color = obj['ambient'] + obj['emission']        
        for light in self.scene.lights:
            obj_color += self.light_shading(light, self.scene.light_attenu, \
                        -direction, intersection, surf, obj)
        
        # resursive ray tracing for specular reflectance
        if np.abs(np.sum(obj['specular'])) < self.zero_thres:
            return obj_color

        if np.abs(np.linalg.norm(direction) - 1.0) > self.zero_thres \
             or np.abs(np.linalg.norm(surf) - 1.0) > self.zero_thres:              
            raise ValueError('Vector not normalized')
        
        # for numerical stability, add small displacement
        mirror_dir = direction - 2 * np.dot(direction, surf) * surf
        return obj_color + \
            obj['specular'] * self.single_ray(intersection + self.delta_move * mirror_dir, mirror_dir, depth + 1)

    def light_shading(self, light, atten, eye_dir, vertex, surface, obj):
        light_dir, light_spc = light
        # directional light
        if light_dir[-1] == 0:
            light_dir = self.norm_vec(light_dir[0:3])

            # visibility test
            # shadow if light source is blocked
            flag, _, _, _ = self.intersection(vertex + self.delta_move * light_dir, light_dir)
            if flag:
                return np.zeros(3)
            
            half_vec = self.norm_vec(light_dir + eye_dir)
            return self.shading_compute(light_dir, light_spc, surface, half_vec, obj)

        # point light
        if light_dir[-1] == 1:
            light_pos = light_dir[0:3] / light_dir[-1]

            light_dir = light_pos - vertex
            light_dist = np.linalg.norm(light_dir)
            light_dir = light_dir / light_dist

            # visibility test
            flag, t_block, _, _ = self.intersection(vertex + self.delta_move * light_dir, light_dir)
            if flag and t_block < light_dist:
                return np.zeros(3)

            half_vec = self.norm_vec(light_dir + eye_dir)
            atten_cst = atten[0] + atten[1] * light_dist + atten[2] * (light_dist ** 2)
            return self.shading_compute(light_dir, light_spc/atten_cst, surface, half_vec, obj)

        warnings.warn('Light Source Type Undefined', RuntimeWarning)        

    def intersection(self, origin, direction):
        # init   
        flag = False
        # ray = origin + t * direction
        t = float('inf')
        
        surf = None
        obj  = None

        origin_world = origin
        direction_world = direction
        # ray and sphere intersection test
        for sphere in self.scene.spheres:
            # apply transformation to the ray
            # 'transform' is the pre-computed inverse transformation
            origin = (sphere['transform'] @ np.append(origin_world, 1))[0:3]
            direction = (sphere['transform'] @ np.append(direction_world, 0))[0:3]

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
                                                
                surf = self.norm_vec((sphere['transform'].T)[0:3, 0:3] @ \
                    (origin + t * direction - sloc))
                obj = sphere
                    
        # ray and triangle intersection test
        for triangle in self.scene.triangles:
            origin = (triangle['transform'] @ np.append(origin_world, 1))[0:3]
            direction = (triangle['transform'] @ np.append(direction_world, 0))[0:3]

            vertice = self.scene.vertices[:, triangle['ver_index']]
            A = vertice[:, 0]
            B = vertice[:, 1]
            C = vertice[:, 2]

            normal = triangle['surface']
            
            # intersection test
            if np.abs(np.dot(direction, normal)) < self.zero_thres:
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
            
            # numerical stability, zero threshold
            threshold = 0 - self.zero_thres
            if a > threshold and b > threshold and c > threshold:
                flag = True
                t = t_temp

                surf = triangle['transformed_normal']
                obj = triangle                

        return (flag, t, surf, obj)