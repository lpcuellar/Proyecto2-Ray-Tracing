##
##  UNIVERSIDAD DEL VALLE DE GUATEMALA
##  GRÁFICAS POR COMPUTADORA
##  SECCIÓN 20
##
##  PROYECTO 2: RAY TRACING
##  LUIS PEDRO CUÉLLAR - 18220
##


import struct
import numpy as np
from numpy import cos, sin, tan

from obj import Obj
from mathGl import MathGl

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2
MAX_RECURSION_DEPTH = 3

##  char --> 1 byte
def char(var):
    return struct.pack('=c', var.encode('ascii'))

##  word --> 2 bytes
def word(var):
    return struct.pack('=h', var)

##  dword --> 4 bytes
def dword(var):
    return struct.pack('=l', var)

##  function that puts the rgb value of a color into bytes
def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

class Raytracer(object):
    def __init__(self, width, height, background = None):
        self.glInit(width, height, background)

    ##  initiates the image with the width, height and background color
    def glInit(self, width, height, background):
        background = color(0, 0, 0) if background == None else background
        self.bg_color = background
        self.current_color = color(1, 1, 1)

        self.camera_position = [0, 0, 0]
        self.fov = 60
        self.scene = []

        self.pointLights = []
        self.ambientLight = None
        self.directionalLight = None

        self.environmentMap = None

        self.mathGl = MathGl()
        self.glCreateWindow(width, height)

    ##  creates the window with the given
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear(self.bg_color)
        self.glViewPort(0, 0, width, height)

    ##  colors the image with the background color
    def glClear(self, bg_color):
        self.bg_color = bg_color
        self.pixels = [ [ self.bg_color for x in range(self.width)] for y in range(self.height) ]
        self.zbuffer = [ [ float('inf') for x in range(self.width)] for y in range(self.height) ]

    def glBackground(self, texture):
        self.pixels = [ [ texture.getColor(x / self.width, y / self.height) for x in range(self.width)] for y in range(self.height) ]

    ##  defines an area inside the window in which it can be drawn points and lines
    def glViewPort(self, x, y, width, height):
         self.vp_x = x
         self.vp_y = y
         self.vp_width = width
         self.vp_height = height

    ##   changes de background color of the image
    def glClearColor(self, r, g, b):
        self.bg_color = color(r, g, b)

        self.glClear(self.bg_color)

   
    ##  draws a point in the image with the given NDC coordinates
    def glVertex(self, x, y, color = None):
        ver_x = (x + 1) * (self.vp_width / 2) + self.vp_x
        ver_y = (y + 1) * (self.vp_height / 2) + self.vp_y

        if (ver_x >= self.width) or (ver_x < 0) or (ver_y >= self.height) or (ver_y < 0) :
            return
        
        try:
            self.pixels[round(ver_y)][round(ver_x)] = color or self.current_color
        except: 
            pass

    ##  draws a pint in the image with pixel coordinates
    def glVertex_coordinates(self, x, y, color = None):
        if (x < self.vp_x) or (x >= self.vp_x + self.vp_width) or (y < self.vp_y) or (y >= self.vp_y + self.vp_height) :
            return
        if (x >= self.width) or (x < 0) or (y >= self.height) or (y < 0):
            return
        try:
            self.pixels[y][x] = color or self.current_color
        except:
            pass

    ##  changes the color of the points that can be drawn
    def glColor(self, r, g, b):
        self.current_color = color(r, g, b)

    def rtRender(self):
        for y in range(self.height):
            for x in range(self.width):
                px = 2 * ((x + 0.5) / self.width) - 1
                py = 2 * ((y + 0.5) / self.height) - 1

                tangente = tan((self.fov * np.pi / 180) / 2)
                r = tangente * self.width / self.height

                px *= r
                py *= tangente

                direction = [px, py, -1]
                direction = self.mathGl.norm(direction)

                self.glVertex_coordinates(x, y, self.castRay(self.camera_position, direction))

    def scene_intercept(self, origin, direction, objOrigin = None):
        tempZBuffer = float('inf')
        material = None
        intersect = None

        for obj in self.scene:
            if obj is not objOrigin:
                hit = obj.ray_intersect(origin, direction)
                if hit is not None:
                    if hit.distance < tempZBuffer:
                        tempZBuffer = hit.distance
                        material = obj.material
                        intersect = hit

        return material, intersect

    def castRay(self, origin, direction, objOrigin = None, recursion = 0):
        material, intersect = self.scene_intercept(origin, direction, objOrigin)

        if material is None or recursion >= MAX_RECURSION_DEPTH:
            if self.environmentMap:
                return self.environmentMap.getColor(direction)
            return self.bg_color

        objectColor = [ material.diffuse[2] / 255,
                        material.diffuse[1] / 255,
                        material.diffuse[0] / 255 ]

        ambientColor = [0, 0, 0]
        directionalLightColor = [0, 0, 0]
        pointLightColor = [0, 0, 0]

        reflectorColor = [0, 0, 0]
        refractorColor = [0, 0, 0]

        finalColor = [0, 0, 0]

        viewDirection = self.mathGl.subtract(self.camera_position, intersect.point)
        viewDirection = self.mathGl.norm(viewDirection)

        if self.ambientLight:
            ambientColor = [ self.ambientLight.strength * self.ambientLight.color[2] / 255,
                             self.ambientLight.strength * self.ambientLight.color[1] / 255,
                             self.ambientLight.strength * self.ambientLight.color[0] / 255 ]
        
        if self.directionalLight:
            diffuseColor = [0, 0, 0]
            specColor = [0, 0, 0]
            shadow_intensity = 0

            light_direction = self.mathGl.getVxSProduct(self.directionalLight.direction, -1)

            intensity = self.directionalLight.intensity * max(0, self.mathGl.dot(light_direction, intersect.normal))

            diffuseColor = [ intensity * self.directionalLight.color[2] / 255,
                             intensity * self.directionalLight.color[1] / 255,
                             intensity * self.directionalLight.color[0] / 255 ]

            reflect = self.mathGl.getReflectVector(intersect.normal, light_direction)

            specIntensity = self.directionalLight.intensity * (max(0, self.mathGl.dot(viewDirection, reflect)) ** material.spec)
            specColor = [ specIntensity * self.directionalLight.color[2] / 255,
                          specIntensity * self.directionalLight.color[1] / 255,
                          specIntensity * self.directionalLight.color[0] / 255 ]
    
            shadMat, shadInter = self.scene_intercept(intersect.point, light_direction, intersect.sceneObject)

            if shadInter is not None:
                shadow_intensity = 1

            directionalLightColor = self.mathGl.getVxSProduct(self.mathGl.getSumVectors(diffuseColor, specColor), (1 - shadow_intensity)) 

        for pointLight in self.pointLights:
            diffuseColor = [0, 0, 0]
            specColor = [0, 0, 0]
            shadow_intensity = 0

            light_direction = self.mathGl.subtract(pointLight.position, intersect.point)
            light_direction = self.mathGl.norm(light_direction)

            intensity = pointLight.intensity * max(0, self.mathGl.dot(light_direction, intersect.normal))
            diffuseColor = [ intensity * pointLight.color[2] / 255,
                             intensity * pointLight.color[1] / 255,
                             intensity * pointLight.color[0] / 255 ]
            
            reflect = self.mathGl.getReflectVector(intersect.normal, light_direction)

            spec_intensity = pointLight.intensity * (max(0, self.mathGl.dot(viewDirection, reflect)) ** material.spec)
            specColor = [ spec_intensity * pointLight.color[2] / 255,
                          spec_intensity * pointLight.color[1] / 255,
                          spec_intensity * pointLight.color[0] / 255 ]

            shadMat, shadInter = self.scene_intercept(intersect.point, light_direction, intersect.sceneObject)

            if shadInter is not None and shadInter.distance < self.mathGl.getVectorMagnitud(self.mathGl.subtract(pointLight.position, intersect.point)):
                shadow_intensity = 1

            pointLightColor = self.mathGl.getSumVectors(pointLightColor, self.mathGl.getVxSProduct(self.mathGl.getSumVectors(diffuseColor, specColor), (1 - shadow_intensity)))

        if material.matType == OPAQUE:
            finalColor = self.mathGl.getSumVectors(ambientColor, self.mathGl.getSumVectors(directionalLightColor, pointLightColor))

            if material.texture and intersect.texCoords:
                texColor = material.texture.getColor(intersect.texCoords[0], intersect.texCoords[1])

                texColor = [ texColor[2] / 255,
                                texColor[1] / 255,
                                texColor[0] / 255 ]

                finalColor = self.mathGl.getProductVectors(finalColor, texColor)
        
        elif material.matType == REFLECTIVE:
            reflect = self.mathGl.getReflectVector(intersect.normal, self.mathGl.getVxSProduct(direction, -1))
            reflectColor = self.castRay(intersect.point, reflect, intersect.sceneObject, recursion + 1)
            reflectColor = [ reflectColor[2] / 255,
                             reflectColor[1] / 255,
                             reflectColor[0] / 255 ]

            finalColor = reflectColor

        elif material.matType == TRANSPARENT:
            outside = self.mathGl.dot(direction, intersect.normal) < 0
            bias = self.mathGl.getVxSProduct(intersect.normal, 0.001)
            kr = self.mathGl.getFresnel(intersect.normal, direction, material.ior)

            reflect = self.mathGl.getReflectVector(intersect.normal, self.mathGl.getVxSProduct(direction, -1))

            reflectOrigin = self.mathGl.getSumVectors(intersect.point, bias) if outside else self.mathGl.subtract(intersect.point, bias)
            reflectColor = self.castRay(reflectOrigin, reflect, None, recursion + 1)
            reflectColor = [ reflectColor[2] / 255,
                             reflectColor[1] / 255,
                             reflectColor[0] / 255 ]

            if kr < 1:
                refractor = self.mathGl.getRefractVector(intersect.normal, direction, material.ior)
                refractorOrigin = self.mathGl.subtract(intersect.point, bias) if outside else self.mathGl.getSumVectors(intersect.point, bias)
                refractorColor = self.castRay(refractorOrigin, refractor, None, recursion + 1)
                refractorColor = [ refractorColor[2] / 255,
                                   refractorColor[1] / 255,
                                   refractorColor[0] / 255 ]

            finalColor = self.mathGl.getSumVectors(self.mathGl.getVxSProduct(reflectColor, kr), self.mathGl.getVxSProduct(refractorColor, (1 - kr)))

        finalColor = self.mathGl.getProductVectors(finalColor, objectColor)

        r = min(1, finalColor[0])
        g = min(1, finalColor[1])
        b = min(1, finalColor[2])

        return color(r, g, b)
        
    ##  this function is used to write the image into the file, and saves it
    def glFinish(self, filename):
        file = open(filename, 'wb')

        ##  file header --> 14 bytes
        file.write(bytes('B'.encode('ascii')))
        file.write(bytes('M'.encode('ascii')))

        file.write(dword(14 + 40 + self.width * self.height * 3))
        file.write(dword(0))
        file.write(dword(14 + 40))

        ##  image header --> 40 bytes
        file.write(dword(40))
        file.write(dword(self.width))
        file.write(dword(self.height))
        file.write(word(1))
        file.write(word(24))
        file.write(dword(0))
        file.write(dword(self.width * self.height * 3))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))

        ##  pixels --> 3 bytes each

        for x in range(self.height) :
            for y in range(self.width) :
                file.write(self.pixels[x][y])

        file.close()

    def glZBuffer(self, filename):
        archivo = open(filename, 'wb')

        # File header 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
        archivo.write(dword(14 + 40 + self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(dword(40))
        archivo.write(dword(self.width))
        archivo.write(dword(self.height))
        archivo.write(word(1))
        archivo.write(word(24))
        archivo.write(dword(0))
        archivo.write(dword(self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))

        # Minimo y el maximo
        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(self.height):
            for y in range(self.width):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] < minZ:
                        minZ = self.zbuffer[x][y]

                    if self.zbuffer[x][y] > maxZ:
                        maxZ = self.zbuffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                depth = self.zbuffer[x][y]
                if depth == -float('inf'):
                    depth = minZ
                depth = (depth - minZ) / (maxZ - minZ)
                archivo.write(color(depth, depth, depth))

        archivo.close()