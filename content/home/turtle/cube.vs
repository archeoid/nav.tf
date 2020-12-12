attribute vec3 aPos;
attribute vec3 aNormal;
uniform mat4 model;
uniform mat3 modelN;
uniform mat4 view;
uniform mat4 projection;
varying vec3 fragPos;
varying vec3 normal;
void main()
{
    fragPos = vec3(model * vec4(aPos, 1.0));
    normal = modelN * aNormal;
    gl_Position = projection * view * model * vec4(aPos.xyz, 1.0);
}