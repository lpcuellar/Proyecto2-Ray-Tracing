##
##  UNIVERSIDAD DEL VALLE DE GUATEMALA
##  GRÁFICAS POR COMPUTADORA
##  SECCIÓN 20
##
##  DR2: LIGHT AND SHADOWS
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

    def add(self, a, b):
        length = len(a)
        c = []

        if length == 2 :
            c.append(a[0] + b[0])
            c.append(a[1] + b[1])

        elif length == 3 :
            c.append(a[0] + b[0])
            c.append(a[1] + b[1])
            c.append(a[2] + b[2])

        return c

    ##  this fucntion does the norm of a vector
    def norm(self, a):
        length = len(a)
        c = 0

        if length == 2 :
            c = (a[0] ** 2) + (a[1] ** 2)
            c = c ** 0.5


        elif length == 3 :
            c = (a[0] ** 2) + (a[1] ** 2) + (a[2] ** 2)
            c = c ** 0.5

        return c

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

    def divMatrix(self, A, B):
        try:
            for i in range(len(A)):
                A[i] /= B

            return A
        except:
            pass

    def transposeMatrix(self, m):
        return list(map(list, zip(*m)))

    def getMatrixMinor(self, m, i, j):
        return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]

    def getMatrixDeternminant(self, m):
        #base case for 2x2 matrix
        if len(m) == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]

        determinant = 0
        for c in range(len(m)):
            determinant += ((-1) ** c) * m[0][c] * self.getMatrixDeternminant(self.getMatrixMinor(m, 0, c))
        return determinant

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

    def getMVProduct(self, v, G):
        result = []
        for i in range(len(G[0])): #this loops through columns of the matrix
            total = 0
            for j in range(len(v)): #this loops through vector coordinates & rows of matrix
                total += v[j] * G[i][j]
            result.append(total)
        return result

    def getMatricesProduct(self, a, b):
        if len(a[0]) != len(b):
            return None

        # Create the result matrix and fill it with zeros
        output_list=[]
            
        for i in range(len(a)):
            row = []

            for j in range(len(a[i])):
                mult = a[i][j] * b[i][j]
                row.append(mult)
            
            output_list.append(row)

        return output_list

    def deg2rad(self, A):
        return (A * np.pi / 180)

    
