##
##  UNIVERSIDAD DEL VALLE DE GUATEMALA
##  GRÁFICAS POR COMPUTADORA
##  SECCIÓN 20
##
##  PROYECTO 2: RAY TRACING
##  LUIS PEDRO CUÉLLAR - 18220
##


import numpy as np


class MathGl(object):
    ##  this function does the cross of two arrays
    def cross(self, a, b):
        length = len(a)
        c = []

        if length == 2 :
            c.append((a[0] * b[1]) - (a[1] * b[0]))

        elif length == 3 :
            c.append((a[1] * b[2]) - (a[2] * b[1]))
            c.append(-((a[0] * b[2]) - (a[2] * b[0])))
            c.append((a[0] * b[1]) - (a[1] * b[0]))

        return c

    ## this function does the difference between two arrays
    def subtract(self, a, b):
        length = len(a)
        c = []

        if length == 2 :
            c.append(a[0] - b[0])
            c.append(a[1] - b[1])

        elif length == 3 :
            c.append(a[0] - b[0])
            c.append(a[1] - b[1])
            c.append(a[2] - b[2])

        return c

    ##  this fucntion does the norm of a vector
    def norm(self, a):
        normal = 0
        for x in a:
            normal += x **2

        normal = normal ** 0.5

        for x in range(len(a)):
            try:
                a[x] /= normal
            except ZeroDivisionError:
                pass
        
        return a

    ##  this function gets the magnitud of a vector
    def getVectorMagnitud(self, a):
        magnitud = 0
        for x in a:
            magnitud += x ** 2
        
        magnitud = magnitud ** 0.5

        return magnitud

    ##  this function does the dot product between two arrays or numbers
    def dot(self, a, b):
        is_a_Array = isinstance(a, list)
        is_b_Array = isinstance(b, list)
        c = 0

        if (is_a_Array == True) and (is_b_Array == True) :
            length = len(a)

            if length == 2:
                c = (a[0] * b[0]) + (a[1] * b[1])

            else :
                c = (a[0] * b[0]) + (a[1] * b[1]) + (a[2] * b[2])

        else:
            c = a * b

        return c

    ##  this function calculates the barycentric coordinates
    def barycentric_coords(self, a, b, c, p):
        ##  u => a
        ##  v => b
        ##  w => c
        try:
            u = (((b[1] - c[1]) * (p[0] - c[0]) + (c[0] - b[0]) * (p[1] - c[1])) /
                  ((b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])))

            v = (((c[1] - a[1]) * (p[0] - c[0]) + (a[0] - c[0]) * (p[1] - c[1])) /
                  ((b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])))

            w = 1 - u - v
        except:
            return -1, -1, -1

        return u, v, w

    ##  this function does the division between two matrix
    def divMatrix(self, A, B):
        try:
            for i in range(len(A)):
                A[i] /= B

            return A
        except:
            pass

    ##  this function does the transpose of a matrix
    def transposeMatrix(self, m):
        return list(map(list, zip(*m)))

    def getMatrixMinor(self, m, i, j):
        return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]

    ##  this function calculates de determinants of a matrix
    def getMatrixDeternminant(self, m):
        #base case for 2x2 matrix
        if len(m) == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]

        determinant = 0
        for c in range(len(m)):
            determinant += ((-1) ** c) * m[0][c] * self.getMatrixDeternminant(self.getMatrixMinor(m, 0, c))
        return determinant

    ##  this function does the inverse of a matrix
    def getMatrixInverse(self, m):
        determinant = self.getMatrixDeternminant(m)
        #special case for 2x2 matrix:
        if len(m) == 2:
            return [[m[1][1] / determinant, -1 * m[0][1] / determinant],
                    [-1 * m[1][0] / determinant, m[0][0] / determinant]]

        #find matrix of cofactors
        cofactors = []
        for r in range(len(m)):
            cofactorRow = []
            for c in range(len(m)):
                minor = self.getMatrixMinor(m, r, c)
                cofactorRow.append(((-1) ** (r + c)) * self.getMatrixDeternminant(minor))
            cofactors.append(cofactorRow)
        cofactors = self.transposeMatrix(cofactors)
        for r in range(len(cofactors)):
            for c in range(len(cofactors)):
                cofactors[r][c] = cofactors[r][c] / determinant
        return cofactors

    ##  this function does the product between a vector and a matrix
    def getMVProduct(self, v, G):
        result = []
        for i in range(len(G[0])): #this loops through columns of the matrix
            total = 0
            for j in range(len(v)): #this loops through vector coordinates & rows of matrix
                total += v[j] * G[i][j]
            result.append(total)
        return result

    ##  this functin does the product between two matrix
    def getMatricesProduct(self, a, b):
        if len(a[0]) != len(b):
            return None

        # Create the result matrix and fill it with zeros
        output_list=[]

        temp_row=len(b[0])*[0]
        for r in range(len(a)):
            output_list.append(temp_row[:])
        for row_index in range(len(a)):
            for col_index in range(len(b[0])):
                sum = 0
                for k in range(len(a[0])):
                    sum += a[row_index][k] * b[k][col_index]
                output_list[row_index][col_index] = sum
        return output_list

    ##  this function calculates the conversion of degrees to radians
    def getDeg2Rad(self, A):
        return (A * np.pi / 180)

    ##  this function does the sum of two vectors
    def getSumVectors(self, a, b):
        if len(a) != len(b):
            return
        
        length = len(a)
        c = [0 for x in a]

        for index in range(length):
            c[index] = a[index] + b[index]

        return c

    ##  this function does the product between two vectors
    def getProductVectors(self, a, b):
        result = [0 for x in a]
        length = len(a)

        for i in range(length):
            result[i] = a[i] * b[i]

        return result

    ##  this function does the product between a vector and a scalar
    def getVxSProduct(self, v, s):
        result = [0 for x in v]
        length = len(v)

        for i in range(length):
            result[i] = v[i] * s

        return result 

    # calcula el vector de reflexion
    def getReflectVector(self, normal, direction):
        # R = 2 * (N dot L) * N - L
        reflect = 2 * self.dot(normal, direction)
        reflect = self.getVxSProduct(normal, reflect)
        reflect = self.subtract(reflect, direction)
        reflect = self.norm(reflect)
        
        return reflect
        
    # (N, I, ior) - normal, vector incidente y el indice de refracción
    def getRefractVector(self, N, I, ior):
        cosi = max(-1, min(1, np.dot(I, N)))
        etai = 1
        etat = ior

        if cosi < 0:
            cosi = -cosi
        else:
            etai, etat = etat, etai
            N = self.getVxSProduct(-1, N)

        eta = etai/etat
        k = 1 - eta * eta * (1 - (cosi * cosi))

        if k < 0: 
            return None
        
        R = self.getSumVectors(self.getVxSProduct(eta, I), self.getVxSProduct((eta * cosi - k**0.5), N))
        return self.norm(R)

    # (N, I, ior) - normal, vector incidente y el indice de refracción
    def getFresnel(self, N, I, ior):

        cosi = max(-1, min(1, self.dot(I, N)))
        etai = 1
        etat = ior

        if cosi > 0:
            etai, etat = etat, etai

        sint = etai / etat * (max(0, 1 - cosi * cosi) ** 0.5)

        if sint >= 1:
            return 1

        cost = max(0, 1 - sint * sint) ** 0.5
        cosi = abs(cosi)
        Rs = ((etat * cosi) - (etai * cost)) / ((etat * cosi) + (etai * cost))
        Rp = ((etai * cosi) - (etat * cost)) / ((etai * cosi) + (etat * cost))
        return (Rs * Rs + Rp * Rp) / 2
