#!/usr/bin/env python3

import math
import numpy

def func(Re, Wc, Wu, delta):
	Re_dt = Wc - Wu + numpy.cross(Wc, Re) 
	return Re + Re_dt * delta


Re = numpy.array([math.pi/2,0,0])
Wc = numpy.array([0,1,0])
Wu = numpy.array([0,0,0])

for i in range(1000):
	Re = func(Re, Wc, Wu, math.pi * 2 / 1000)
	print(Re)
