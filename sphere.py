##
##  UNIVERSIDAD DEL VALLE DE GUATEMALA
##  GRÁFICAS POR COMPUTADORA
##  SECCIÓN 20
##
##  DR2: LIGHT AND SHADOWS
##  LUIS PEDRO CUÉLLAR - 18220
##


import numpy as np

from gl import color
from mathGl import MathGl


white = color(1, 1, 1)

class AmbientLight(object):
    def __init__(self, strength = 0, _color = white):
        self.strength = strength
        self.color = _color

class PointLight(object):
    def __init__(self, position = [0, 0, 0], _color = white, intensity = 1):
        self.position = position
        self.color = _color
        self.intensity = intensity

class Material(object):
    def __init__(self, diffuse = white, spec = 0):
        self.diffuse = diffuse
        self.spec = spec

class Intersect(object):
    def __init__(self, distance, point, normal, sceneObject):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.sceneObject = sceneObject

class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

        self.mathGl = MathGl()

    def ray_intersect(self, orig, dir):
        L = self.mathGl.subtract(self.center, orig)
        tca = self.mathGl.dot(L, dir)
        
        l = self.mathGl.norm(L)
        d = (l**2 - tca**2) **0.5

        if d > self.radius:
            return None
        
        thc = (self.radius ** 2 - d**2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1

        if t0 < 0:
            return None
        
        for i in range(len(dir)):
            dir[i] *= t0

        hit = self.mathGl.add(orig, dir)
        norm = self.mathGl.subtract(hit, self.center)
        norm = self.mathGl.divMatrix(norm, self.mathGl.norm(norm))
        
        return Intersect(distance = t0,
                            point = hit,
                            normal = norm,
                            sceneObject = self)