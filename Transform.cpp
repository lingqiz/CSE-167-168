// Transform.cpp: implementation of the Transform class.

// Note: when you construct a matrix using mat4() or mat3(), it will be COLUMN-MAJOR
// Keep this in mind in readfile.cpp and display.cpp
// See FAQ for more details or if you're having problems.

#include "Transform.h"

// Helper rotation function.  Please implement this.  
mat3 Transform::rotate(const float degrees, const vec3& axis) {
	float radAng  = degrees / 180.0 * pi;
	
  vec3 normAxis = glm::normalize(axis);
	float x = normAxis[0];
	float y = normAxis[1];
	float z = normAxis[2];

	mat3 identity   = mat3(1, 0, 0, 0, 1, 0, 0, 0, 1);
	mat3 projection = mat3(x*x, x*y, x*z, x*y, y*y, y*z, x*z, y*z, z*z);	
	mat3 dual 		= mat3(0, z, -y, -z, 0, x, y, -x, 0);
	
	return cos(radAng) * identity + (1 - cos(radAng)) * projection + sin(radAng) * dual; 
}

// Transforms the camera left around the "crystal ball" interface
void Transform::left(float degrees, vec3& eye, vec3& up) {
	mat3 rotateMtx = rotate(degrees, glm::normalize(up));
	eye = rotateMtx * eye;
	up  = rotateMtx * up;
}

// Transforms the camera up around the "crystal ball" interface
void Transform::up(float degrees, vec3& eye, vec3& up) {
	vec3 rotDir = glm::cross(eye, up);
	mat3 rotateMtx = rotate(degrees, glm::normalize(rotDir));
	eye = rotateMtx * eye;
	up  = rotateMtx * up;
}


mat4 Transform::lookAt(const vec3 &eye, const vec3 &center, const vec3 &up) 
{
    vec3 w = glm::normalize(eye);
    vec3 u = glm::normalize(glm::cross(up,eye));
    vec3 v = glm::normalize(glm::cross(w,u));
    // You will change this return call
    return glm::transpose(mat4(vec4(u.x,u.y,u.z,glm::dot(u, -eye)),
                               vec4(v.x,v.y,v.z,glm::dot(v, -eye)),
                               vec4(w.x,w.y,w.z,glm::dot(w, -eye)),
                               vec4(0,0,0,1)
                               ));
}

mat4 Transform::perspective(float fovy, float aspect, float zNear, float zFar)
{
    mat4 ret(0);
    
    float scale = 1 / tan(fovy * 0.5 * M_PI / 180);
    ret[0][0] = scale/aspect; // scale the x coordinates of the projected point
    ret[1][1] = scale; // scale the y coordinates of the projected point
    ret[2][2] = -zFar / (zFar - zNear); // used to remap z to [0,1]
    ret[3][2] = -zFar * zNear / (zFar - zNear); // used to remap z [0,1]
    ret[2][3] = -1; // set w = -z
    ret[3][3] = 0;
    
    return ret;
}

mat4 Transform::scale(const float &sx, const float &sy, const float &sz) 
{
    return glm::transpose(mat4(vec4(sx,0,0,0),
                               vec4(0,sy,0,0),
                               vec4(0,0,sz,0),
                               vec4(0,0,0,1)
                               ));
}

mat4 Transform::translate(const float &tx, const float &ty, const float &tz) 
{
      return glm::transpose(mat4(vec4(1,0,0,tx),
                               vec4(0,1,0,ty),
                               vec4(0,0,1,tz),
                               vec4(0,0,0,1)
                               ));
}

// To normalize the up direction and construct a coordinate frame.  
// As discussed in the lecture.  May be relevant to create a properly 
// orthogonal and normalized up. 
// This function is provided as a helper, in case you want to use it. 
// Using this function (in readfile.cpp or display.cpp) is optional.  

vec3 Transform::upvector(const vec3 &up, const vec3 & zvec) 
{
  vec3 x = glm::cross(up,zvec); 
  vec3 y = glm::cross(zvec,x); 
  vec3 ret = glm::normalize(y); 
  return ret; 
}


Transform::Transform()
{

}

Transform::~Transform()
{

}
