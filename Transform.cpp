// Transform.cpp: implementation of the Transform class.

// Note: when you construct a matrix using mat4() or mat3(), it will be COLUMN-MAJOR
// Keep this in mind in readfile.cpp and display.cpp
// See FAQ for more details or if you're having problems.

#include "Transform.h"

// Helper rotation function.  Please implement this.  
mat3 Transform::rotate(const float degrees, const vec3& axis) {
	float radAng  = degrees / 180.0 * pi;
	
	float x = axis[0];
	float y = axis[1];
	float z = axis[2];

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
  mat4 ret;
  // YOUR CODE FOR HW2 HERE
  // Likely the same as in HW 1.  
  return ret;
}

mat4 Transform::perspective(float fovy, float aspect, float zNear, float zFar)
{
  mat4 ret;
  // YOUR CODE FOR HW2 HERE
  // New, to implement the perspective transform as well.  
  return ret;
}

mat4 Transform::scale(const float &sx, const float &sy, const float &sz) 
{
  mat4 ret;
  // YOUR CODE FOR HW2 HERE
  // Implement scaling 
  return ret;
}

mat4 Transform::translate(const float &tx, const float &ty, const float &tz) 
{
  mat4 ret;
  // YOUR CODE FOR HW2 HERE
  // Implement translation 
  return ret;
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
