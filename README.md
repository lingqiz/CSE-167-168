## UCSD CSE 167x (edX), Computer Graphics

---
### Simple OpenGL pipeline
* Transformation
* Phong shading model

#### Example Scene
<img src="https://github.com/lingqiz/UCSD-CSE-167x/blob/master/opengl-1.png" width="384">

---
### Simple ray tracer in Python 
* Effect of shadow (visibility test)
* Phong shading model
* Mirror reflection with resursive ray tracing
* Simple acceleration with CPU parallel processing
* TODO: implement acceleration structure for the ray tracer

#### Usage
- `python main.py 'scene_file_path' #num_of_process`
- `scene_file` defines camera, light, objects and their surface properties
- see `.test` for example `scene_file` definition
<img src="https://github.com/lingqiz/UCSD-CSE-167x/blob/master/ray_tracer.png" width="600">

#### Example Scene
<img src="https://github.com/lingqiz/UCSD-CSE-167x/blob/master/trace-1-highres.png" width="600">
<img src="https://github.com/lingqiz/UCSD-CSE-167x/blob/master/trace-2-highres.png" width="600">
<img src="https://github.com/lingqiz/UCSD-CSE-167x/blob/master/trace-3.png" width="600">
<img src="https://github.com/lingqiz/UCSD-CSE-167x/blob/master/trace-4.png" width="600">

---