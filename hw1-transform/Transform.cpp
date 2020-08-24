// Transform.cpp: implementation of the Transform class.

#include "Transform.h"

//Please implement the following functions:

// Helper rotation function.  
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

// Your implementation of the glm::lookAt matrix
mat4 Transform::lookAt(vec3 eye, vec3 up) {
	// construct a coordinate system through cross product (for rotation)
	vec3 viewDir = glm::normalize(eye);
	vec3 otherDir = glm::normalize(glm::cross(up, viewDir));
	vec3 upDir = glm::cross(viewDir, otherDir);

	mat4 rotateMtx = mat4(otherDir[0], upDir[0], viewDir[0], 0, otherDir[1], upDir[1], viewDir[1], 0, otherDir[2], upDir[2], viewDir[2], 0, 0, 0, 0, 1);

	// translation matrix for correct eye location
	mat4 transMtx  = mat4(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, -eye[0], -eye[1], -eye[2], 1);

	return rotateMtx * transMtx;
}

Transform::Transform()
{

}

Transform::~Transform()
{

}
