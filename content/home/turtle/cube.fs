precision mediump float;
varying vec3 normal;
varying vec3 fragPos;
uniform vec3 lightPos;
uniform vec3 color;
void main()
{
   float ambientStrength = 0.1;
   vec3 ambient = ambientStrength * vec3(1.0, 1.0, 1.0);
   vec3 norm = normalize(normal);
   vec3 lightDir = normalize(lightPos - fragPos);
   float diff = max(dot(norm, lightDir), 0.0);
   vec3 diffuse = diff * vec3(1.0, 1.0, 1.0);
   vec3 result = (ambient + diffuse) * color;
   gl_FragColor = vec4(result,1.0);
}