# version 330 core
// Do not use any version older than 330!

/* This is the fragment shader for reading in a scene description, including 
   lighting.  Uniform lights are specified from the main program, and used in 
   the shader.  As well as the material parameters of the object.  */

// Inputs to the fragment shader are the outputs of the same name of the vertex shader.
// Note that the default output, gl_Position, is inaccessible!
in vec3 mynormal; 
in vec4 myvertex; 

// You will certainly need this matrix for your lighting calculations
uniform mat4 modelview;

// This first defined output of type vec4 will be the fragment color
out vec4 fragColor;

uniform vec3 color;

const int numLights = 10; 
uniform bool enablelighting; // are we lighting at all (global).
uniform vec4 lightposn[numLights]; // positions of lights 
uniform vec4 lightcolor[numLights]; // colors of lights
uniform int numused;               // number of lights used

// Now, set the material parameters.
// I use ambient, diffuse, specular, shininess. 
// But, the ambient is just additive and doesn't multiply the lights.  

uniform vec4 ambient; 
uniform vec4 emission;

uniform vec4 diffuse; 
uniform vec4 specular; 
 
uniform float shininess;

vec4 shadingCompute (const in vec3 direction, const in vec4 colorL, const in vec3 normal, const in vec3 halfvec) 
{    
        // lambertian surface
        // only depends on dot(light_direction, surface_normal); shape from shading
        float nDotL = dot(normal, direction);         
        vec4 lambert = diffuse * colorL * max (nDotL, 0.0);  

        // specular surface with phong illumination model
        // dependent on the eye direction (half vector)
        float nDotH = dot(normal, halfvec); 
        vec4 phong = specular * colorL * pow (max(nDotH, 0.0), shininess); 

        vec4 retval = lambert + phong; 
        return retval;      
}   

vec4 lightCompute(vec4 lightPos, vec4 lightColor)
{
    const vec3 eyepos = vec3(0, 0, 0);
    vec3 mypos = myvertex.xyz / myvertex.w;
    vec3 eyedirn = normalize(eyepos - mypos);
    vec3 normal = normalize(mynormal);

    vec3 lightDir;
    if(lightPos.w == 0)
    {
        lightDir = normalize(lightPos.xyz);
    }      
    else
    {
        vec3 lPos = lightPos.xyz / lightPos.w;
        lightDir = normalize(lPos - mypos);
    }    

    vec3 halfVec = normalize(lightDir + eyedirn);
    return shadingCompute(lightDir, lightColor, normal, halfVec);
}

void main (void) 
{       
    if (enablelighting) {
        
        vec4 allColor = vec4(0.0f, 0.0f, 0.0f, 1.0f);
        for(int idl = 0; idl < numused; idl++)
        {
            allColor += lightCompute(lightposn[idl], lightcolor[idl]);
        }
                   
        fragColor = allColor + ambient + emission;
    }

    else 
    {
        fragColor = vec4(color, 1.0f);
    }
}
