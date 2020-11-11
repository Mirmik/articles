#!/usr/bin/env python3

import sympy
import zencad
from zencad import deg
from zencad.libs.screw import screw
import numpy

numpy.set_printoptions(precision=4, floatmode="fixed")
numpy.set_printoptions(suppress=True)
sympy.var("k d")

R = zencad.rotateX(deg(45))
s = screw(
		lin=R(zencad.vector3(0,0,1)), 
		ang=R(zencad.vector3(0,0,0.1)))
#vk = vk.force_carry(R)

#vk= R(vk)
#vd= R(vd)

arr = numpy.ndarray([6,6])

ang = 0
for i in range(6):
	RR =  zencad.rotateZ(deg(ang)) * zencad.moveY(3)

	ss = s.rotate_by(zencad.rotateZ(deg(ang)))
	ss = ss.force_carry(-RR.translation())

	vvk = ss.lin
	vvd = ss.ang

	#vvk = zencad.rotateZ(deg(ang))(vk)
	#vvd = zencad.rotateZ(deg(ang))(vd)
	ang = ang + 60 
	arr[0][i] = vvk[0]
	arr[1][i] = vvk[1]
	arr[2][i] = vvk[2]

	if i % 2 == 0:
		arr[3][i] = vvd[0]
		arr[4][i] = vvd[1]
		arr[5][i] = vvd[2]
	else:
		arr[3][i] = -vvd[0]
		arr[4][i] = -vvd[1]
		arr[5][i] = -vvd[2]

for i in range(6):
	arr[i][1] = 0

print(arr)
	
print(numpy.linalg.matrix_rank(arr))

#print(numpy.linalg.solve(arr, numpy.array([0,0,20,0,0,0])) - numpy.linalg.solve(arr, numpy.array([1,0,20,0,0,0])))