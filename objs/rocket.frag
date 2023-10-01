#version 330 compatibility

float rand(vec2 co){
    return fract(sin(dot(co, vec2(12.9898, 78.233))) * 43758.5453);
}

uniform vec4 Global_ambient;
uniform vec4 Light_ambient;
uniform vec4 Light_diffuse;
uniform vec4 Light_specular;

uniform float Material_shininess;
uniform vec4 Material_specular;
uniform vec4 Material_ambient;
uniform vec4 Material_diffuse;

in vec2 vST;
in vec3 vN;
in vec3 vL;
in vec3 vE;


void main() {
	vec3 Normal = normalize(vN);
	vec3 Light = normalize(vL);
	vec3 Eye = normalize(vE);
	
	vec4 ambient = Light_ambient * Material_ambient;
	
	float d = max(dot(Normal, Light), 0);
	vec4 diffuse = Light_diffuse * d * Material_diffuse;
	
	float s = 0;
	vec3 ref = normalize(reflect(Light, Normal));
	s = pow(max(dot(Eye,ref),0.), Material_shininess);	
	
	vec4 specular = Light_specular * s * Material_specular;
	
	float attenuation = 1.0 / (0.5 + 0.0001 * pow(length(vL), 2));
	gl_FragColor = ambient + attenuation * (diffuse + specular);
	
	
}