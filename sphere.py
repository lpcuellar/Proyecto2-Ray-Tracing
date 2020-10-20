##
##  UNIVERSIDAD DEL VALLE DE GUATEMALA
##  GRÁFICAS POR COMPUTADORA
##  SECCIÓN 20
##
##  PROYECTO 2: RAY TRACING
##  LUIS PEDRO CUÉLLAR - 18220
##


import numpy as np
from numpy import arccos, arctan2

from gl import color
from mathGl import MathGl

mathGl = MathGl()

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

white = color(1, 1, 1)

class AmbientLight(object):
    def __init__(self, strength = 0, _color = white):
        self.strength = strength
        self.color = _color

class DirectionalLight(object):
    def __init__(self, direction = [0, -1, 0], _color = white, intensity = 1):
        self.direction = mathGl.norm(direction)
        self.intensity = intensity
        self.color = _color

class PointLight(object):
    def __init__(self, position = [0, 0, 0], _color = white, intensity = 1):
        self.position = position
        self.intensity = intensity
        self.color = _color

class Material(object):
    def __init__(self, diffuse = white, spec = 0, ior = 1, texture = None, matType = OPAQUE):
        self.diffuse = diffuse
        self.spec = spec

        self.matType = matType
        self.ior = ior

        self.texture = texture

class Intersect(object):
    def __init__(self, distance, point, normal, texCoords, sceneObject):
        self.distance = distance
        self.point = point
        self.normal = normal

        self.texCoords = texCoords

        self.sceneObject = sceneObject

class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, origin, direction):
        L = mathGl.subtract(self.center, origin)
        tca = mathGl.dot(L, direction)
        l = mathGl.getVectorMagnitud(L)

        d = (l ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None
        
        thc = (self.radius ** 2 - d ** 2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1

        if t0 < 0:
            return None 

        hit = mathGl.getSumVectors(origin, mathGl.getVxSProduct(direction, t0))
        norm = mathGl.subtract(hit, self.center)
        norm = mathGl.norm(norm)

        u = 1 - (arctan2(norm[2], norm[0]) / (2 * np.pi) + 0.5)
        v = arccos(-norm[1]) / np.pi

        uvs = [u, v]
        return Intersect(distance = t0,
                         point = hit,
                         normal = norm,
                         texCoords = uvs,
                         sceneObject = self)

class Plane(object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = mathGl.norm(normal)
        self.material = material

    def ray_intersect(self, origin, direction):
        denom = mathGl.dot(direction, self.normal)

        if abs(denom) > 0.0001:
            t = mathGl.dot(self.normal, mathGl.subtract(self.position, origin)) / denom

            if t > 0:
                hit = mathGl.getSumVectors(origin, mathGl.getVxSProduct(direction, t))

                return Intersect(distance = t,
                                 point = hit, 
                                 normal = self.normal, 
                                 texCoords = None, 
                                 sceneObject = self)
        
        return None

class AABB(object):
    def __init__(self, position, size, material):
        self.position = position
        self.size = size
        self.material = material
        self.planes = []

        halfSizeX = size[0] / 2
        halfSizeY = size[1] / 2
        halfSizeZ = size[2] / 2

        self.planes.append(Plane(mathGl.getSumVectors(position, [halfSizeX, 0, 0]), [1, 0, 0], material))
        self.planes.append(Plane(mathGl.getSumVectors(position, [-halfSizeX, 0, 0]), [-1, 0, 0], material))

        self.planes.append(Plane(mathGl.getSumVectors(position, [0, halfSizeY, 0]), [0, 1, 0], material))
        self.planes.append(Plane(mathGl.getSumVectors(position, [0, -halfSizeY, 0]), [0, -1, 0], material))

        self.planes.append(Plane(mathGl.getSumVectors(position, [0, 0, halfSizeZ]), [0, 0, 1], material))
        self.planes.append(Plane(mathGl.getSumVectors(position, [0, 0, -halfSizeZ]), [0, 0, -1], material))

    def ray_intersect(self, origin, direction):
        epsilon = 0.001

        boundsMin = [0, 0, 0]
        boundsMax = [0, 0, 0]

        for i in range(3):
            boundsMin[i] = self.position[i] - (epsilon + self.size[i] / 2)
            boundsMax[i] = self.position[i] + (epsilon + self.size[i] / 2)


        t = float('inf')
        intersect = None

        uvs = None

        for plane in self.planes:
            planeInter = plane.ray_intersect(origin, direction)

            if planeInter is not None:
                if planeInter.point[0] >= boundsMin[0] and planeInter.point[0] <= boundsMax[0]:
                    if planeInter.point[1] >= boundsMin[1] and planeInter.point[1] <= boundsMax[1]:
                        if planeInter.point[2] >= boundsMin[2] and planeInter.point[2] <= boundsMax[2]:
                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter

                                if abs(plane.normal[0]) > 0:
                                    u = (planeInter.point[1] - boundsMin[1]) / (boundsMax[1] - boundsMin[1])
                                    v = (planeInter.point[2] - boundsMin[2]) / (boundsMax[2] - boundsMin[2])
                                
                                elif abs(plane.normal[1]) > 0: 
                                    u = (planeInter.point[0] - boundsMin[0]) / (boundsMax[0] - boundsMin[0])
                                    v = (planeInter.point[2] - boundsMin[2]) / (boundsMax[2] - boundsMin[2])
                                
                                elif abs(plane.normal[2]) > 0:
                                    u = (planeInter.point[0] - boundsMin[0]) / (boundsMax[0] - boundsMin[0])
                                    v = (planeInter.point[1] - boundsMin[1]) / (boundsMax[1] - boundsMin[1])

                                uvs = [u, v]

        if intersect is None:
            return None
        
        return Intersect(distance = intersect.distance,
                         point = intersect.point,
                         normal = intersect.normal,
                         texCoords = uvs,
                         sceneObject = self)