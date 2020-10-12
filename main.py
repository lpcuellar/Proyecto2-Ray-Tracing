##
##  UNIVERSIDAD DEL VALLE DE GUATEMALA
##  GRÁFICAS POR COMPUTADORA
##  SECCIÓN 20
##
##  DR2: LIGHT AND SHADOWS
##  LUIS PEDRO CUÉLLAR - 18220
##


import random

from gl import Raytracer, color
from object import Object, Texture
from sphere import Sphere, Material, PointLight, AmbientLight

r = Raytracer(500, 500)

brick = Material(diffuse = color(0.8, 0.25, 0.25))
stone = Material(diffuse = color(0.4, 0.4, 0.4 ))
grass = Material(diffuse = color(0.5, 1, 0))

snow = Material(diffuse = color(1, 0.96, 0.96))
orange = Material(diffuse = color(1, 0.65, 0))
coal = Material(diffuse = color(0.2, 0.2, 0.2))
dark = Material(diffuse = color(1, 1, 1))


r.pointLight = PointLight(position = [-2, 2, 0], intensity = 1)
r.ambientLight = AmbientLight(strength = 0.1)

r.scene.append( Sphere([ 0, 0, -5],    1, brick) )
r.scene.append( Sphere([ -0.5, 0.5, -3], 0.25, stone) )
#r.scene.append( Sphere(V3(-1,-1, -5), 0.5, grass) )
#r.scene.append( Sphere(V3( 1,-1, -5), 0.5, glass) )
 
r.rtRender()

r.glFinish('output.bmp') 