##
##  UNIVERSIDAD DEL VALLE DE GUATEMALA
##  GRÁFICAS POR COMPUTADORA
##  SECCIÓN 20
##
##  PROYECTO 2: RAY TRACING
##  LUIS PEDRO CUÉLLAR - 18220
##

import random

from gl import Raytracer, color
from obj import Obj, Texture, EnvMap
from sphere import *


r = Raytracer(1000, 750)
r.glClearColor(0.2, 0.6, 0.8)

brick = Material(diffuse = color(0.8, 0.25, 0.25 ), spec = 16)
stone = Material(diffuse = color(0.4, 0.4, 0.4 ), spec = 32)
mirror = Material(spec = 64, matType = REFLECTIVE)
glass = Material(spec = 64, ior = 1.5, matType= TRANSPARENT) 
grass = Material(texture = Texture('./textures/grassBlock.bmp'))
snow = Material(texture = Texture('./textures/snowBlock.bmp'))
iceBlock = Material(texture = Texture('./textures/iceBlock.bmp'), ior = 1.5)
pumpkinHead = Material(texture = Texture('./textures/pumpkin.bmp'))
treeLog = Material(texture = Texture('./textures/woodBlock.bmp'))
treeLeaves = Material(texture = Texture('./textures/leaves.bmp'))

#   Environment Map
r.environmentMap = EnvMap('./textures/snowPicture.bmp')

# Lights (they do work)
r.directionalLight = DirectionalLight(direction = [1, -1, -2], intensity = 0.5)
r.ambientLight = AmbientLight(strength = 0.1)

##  GRASS
r.scene.append(AABB([0, -3, -14], [24, 0.1, 24] , grass ) )

##  SNOW MAN
r.scene.append(AABB([-4, -1.5, -10], [3, 3, 3], snow))
r.scene.append(AABB([-4, 1, -10], [2.5, 2.5, 2.5], snow))
r.scene.append(AABB([-4, 3, -10], [2, 2, 2], pumpkinHead))

##  TREE LOGS
r.scene.append(AABB([0, -3, -18], [1.5, 1.5, 1.5], treeLog))
r.scene.append(AABB([0, -2, -18], [1.5, 1.5, 1.5], treeLog))
r.scene.append(AABB([0, -1, -18], [1.5, 1.5, 1.5], treeLog))
r.scene.append(AABB([0, 0, -18], [1.5, 1.5, 1.5], treeLog))
r.scene.append(AABB([0, 1, -18], [1.5, 1.5, 1.5], treeLog))

##  TREE LEAVES
r.scene.append(AABB([-2, 2, -16], [2, 2, 2], treeLeaves))
r.scene.append(AABB([-4, 2, -16], [2, 2, 2], treeLeaves))
r.scene.append(AABB([0, 2, -16], [2, 2, 2], treeLeaves))
r.scene.append(AABB([2, 2, -16], [2, 2, 2], treeLeaves))
r.scene.append(AABB([4, 2, -16], [2, 2, 2], treeLeaves))
r.scene.append(AABB([-2, 4, -16], [2, 2, 2], treeLeaves))
r.scene.append(AABB([0, 4, -16], [2, 2, 2], treeLeaves))
r.scene.append(AABB([2, 4, -16], [2, 2, 2], treeLeaves))
r.scene.append(AABB([0, 6, -16], [2, 2, 2], treeLeaves))

##  IGLOO
r.scene.append(AABB([1, -3, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([1, -2, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([1, -1, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([1, 0, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([2, -3, -11], [1, 1, 1], iceBlock))
r.scene.append(AABB([2, -2, -11], [1, 1, 1], iceBlock))
r.scene.append(AABB([2, -1, -11], [1, 1, 1], iceBlock))
r.scene.append(AABB([2, 0, -11], [1, 1, 1], iceBlock))

r.scene.append(AABB([6, -3, -11], [1, 1, 1], iceBlock))
r.scene.append(AABB([6, -2, -11], [1, 1, 1], iceBlock))
r.scene.append(AABB([6, -1, -11], [1, 1, 1], iceBlock))
r.scene.append(AABB([6, 0, -11], [1, 1, 1], iceBlock))
r.scene.append(AABB([6, -3, -11], [1, 1, 1], iceBlock))
r.scene.append(AABB([7, -3, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([7, -2, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([7, -1, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([7, 0, -12], [1, 1, 1], iceBlock))

r.scene.append(AABB([3, -3, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([3, -2, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([3, -1, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([3, 0, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([3, 1, -12], [1, 1, 1], iceBlock))

r.scene.append(AABB([4, -3, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([4, -2, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([4, -1, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([4, 0, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([4, 1, -12], [1, 1, 1], iceBlock))

r.scene.append(AABB([5, -3, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([5, -2, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([5, -1, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([5, 0, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([5, 1, -12], [1, 1, 1], iceBlock))

r.scene.append(AABB([2, 1, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([3, 1, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([4, 1, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([5, 1, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([6, 1, -12], [1, 1, 1], iceBlock))

r.scene.append(AABB([2.5, 2, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([3.5, 2, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([4.5, 2, -12], [1, 1, 1], iceBlock))
r.scene.append(AABB([5.5, 2, -12], [1, 1, 1], iceBlock))





r.rtRender()

r.glFinish('output.bmp') 