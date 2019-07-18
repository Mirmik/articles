#!/usr/bin/env python3

import pycrow
import time
from zencad import *
from zencad.controllers import *

import random

import numpy

pycrow.create_udpgate(12, 10012)
pycrow.start_spin()

x = [0,0,0,0,0]
def incomming(pack):
	global x
	arr = numpy.frombuffer(pack.rawdata(), dtype=numpy.float32)
	if len(arr) == 5:
		x = arr 

pycrow.incoming_handler(incomming)

class zveno1(zencad.controllers.Unit):
	def __init__(self, l):
		super().__init__()
		
		m = (
			cylinder(r=3, h=l) 
			+ cylinder(r=3, h=6, center=True).rotateX(deg(90)).up(l)
			+ cylinder(r=3, h=6, center=True).rotateX(deg(90))
		)
		self.set_shape(m)
		
		self.outrot = zencad.controllers.CynematicRotator(
			ax = (0,1,0),
			name="zv.outrot",
			parent=self, 
			location=up(l))

o = zencad.controllers.CynematicRotator(ax=(0,0,1))
a = zveno1(40)
b = zveno1(30)
c = zveno1(20)
d = zveno1(10)
e = zveno1(10)

d.relocate(rotate((0,0,1),deg(90)))

o.link(a)
a.outrot.link(b)
b.outrot.link(c)
c.outrot.link(d)
d.outrot.link(e)

o.set_coord(deg(50))
a.outrot.set_coord(deg(45))
b.outrot.set_coord(deg(60))
c.outrot.set_coord(deg(-20))
d.outrot.set_coord(deg(-30))

o.location_update(deep=True)

scn = zencad.Scene()
a.bind_scene_deep(scn)

#v = [1,1,1,1,1]
lasttime = time.time()
def update(wdg):
#	global lasttime
#	curtime = time.time()
#	deltatime = curtime - lasttime
#	lasttime = curtime

#	deltatime = deltatime * 3 / 4

#	for i in range(len(x)):
#		v[i] += random.uniform(-deltatime*3, deltatime*3)
#		x[i] += v[i] * deltatime

	o.set_coord(x[0])
	a.outrot.set_coord(x[1])
	b.outrot.set_coord(x[2])
	c.outrot.set_coord(x[3])
	d.outrot.set_coord(x[4])
	
	o.location_update(deep=True, view=True)

	#wdg.set_eye(zencad.rotateZ(zencad.deg(deltatime*7))(wdg.eye()), orthogonal=True)

show(scn, animate=update)