#version 330 core
// Do not use any version older than 330! Modern OpenGL will break!

// Inputs to the vertex shader
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;

// Uniform variables
uniform mat4 modelview;
uniform mat4 projection;

// Additional outputs for the vertex shader in addition to gl_Position
smooth out vec3 mynormal;
smooth out vec4 myvertex;

void main() {
	myvertex = modelview * vec4(position, 1.0f);
	gl_Position = projection * myvertex;
    
	// Forward these vectors to the fragment shader
	mynormal = mat3(transpose(inverse(modelview))) * normal;
	myvertex = vec4(position, 1.0f);
}

