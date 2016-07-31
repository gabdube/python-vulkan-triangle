# -*- coding: utf-8 -*-

# Some math functions
# Tuple are returned because list can't be hashed (and so lrucache fails)

from math import tan, radians, sin, cos
from functools import lru_cache
from itertools import accumulate
from copy import deepcopy

from ctypes import c_float, Structure

class Mat4(Structure):
    rowtype = c_float*4

    _fields_ = (('r1', rowtype), ('r2', rowtype), ('r3', rowtype), ('r4', rowtype))

    def __init__(self, **kw):
        self.r1 = Mat4.rowtype(*(kw.get('r1') or (1,0,0,0)))
        self.r2 = Mat4.rowtype(*(kw.get('r2') or (0,1,0,0)))
        self.r3 = Mat4.rowtype(*(kw.get('r3') or (0,0,1,0)))
        self.r4 = Mat4.rowtype(*(kw.get('r4') or (0,0,0,1)))
        Structure.__init__(self)

    def data(self):
        return tuple([tuple(x) for x in [self.r1, self.r2, self.r3, self.r4]])

    def set_data(self, data):
        self.r1[::] = data[0]
        self.r2[::] = data[1]
        self.r3[::] = data[2]
        self.r4[::] = data[3]

identity = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]
vec_scalar_mult = lambda v, s: [i*s for i in v]
vec_add = lambda v1, v2: [ i+j for i,j in zip(v1, v2) ]
tupleize = lambda l: tuple([tuple(i) for i in l])

@lru_cache(maxsize=16)
def perspective(fov, aspect, z_near, z_far):
    tan_half_fov = tan(radians(fov)/2)

    result = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
    result[0][0] = 1/(aspect*tan_half_fov)
    result[1][1] = 1/(tan_half_fov)
    result[2][3] = -1
    result[2][2] = z_far / (z_near - z_far)
    result[3][2] = -(z_far*z_near) / (z_far - z_near)

    return tupleize(result)


@lru_cache(maxsize=32)
def translate(mat=None, vec=(0.0, 0.0, 0.0)):
    mat = mat or deepcopy(identity)
    result = deepcopy(mat)
    

    rows = (
        vec_scalar_mult(mat[0], vec[0]),
        vec_scalar_mult(mat[1], vec[1]),
        vec_scalar_mult(mat[2], vec[2]),
        mat[3]
    )

    result[3] = list(accumulate(rows, vec_add))[-1]

    return tupleize(result)

def rotate(mat=None, angle=0, vec=(0.0, 0.0, 0.0)):
    mat = mat or deepcopy(identity)
    a = radians(angle)
    c = cos(a)
    s = sin(a)

    axis = vec
    temp = vec_scalar_mult(axis, 1.0-c)
    rot = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
    
    rot[0][0] = c + temp[0] * axis[0]
    rot[0][1] = 0 + temp[0] * axis[1] + s * axis[2]
    rot[0][2] = 0 + temp[0] * axis[2] - s * axis[1]

    rot[1][0] = 0 + temp[1] * axis[0] - s * axis[2];
    rot[1][1] = c + temp[1] * axis[1] 
    rot[1][2] = 0 + temp[1] * axis[2] + s * axis[0]

    rot[2][0] = 0 + temp[2] * axis[0] + s * axis[1]
    rot[2][1] = 0 + temp[2] * axis[1] - s * axis[0]
    rot[2][2] = c + temp[2] * axis[2] 

    rows = []
    for i in range(3):
        rows.append(
            (
                vec_scalar_mult(mat[0], rot[i][0]),
                vec_scalar_mult(mat[1], rot[i][1]),
                vec_scalar_mult(mat[2], rot[i][2]),
                [0.0, 0.0, 0.0, 0.0]
            )
        )

    result = (
        list(accumulate(rows[0], vec_add))[-1],
        list(accumulate(rows[1], vec_add))[-1], 
        list(accumulate(rows[2], vec_add))[-1],
        [float(x) for x in mat[3]]
    )

    return tupleize(result) 