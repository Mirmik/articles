#!/usr/bin/env python3

import pycrow
import time
from zencad import *
import zencad.assemble
import zencad.cynematic
import zencad.malgo

import random

import numpy

#pycrow.diagnostic(live=True)
#pycrow.create_udpgate(12, 10012)
#pycrow.start_spin()

def incomming(pack):
	global x
	arr = numpy.frombuffer(pack.rawdata(), dtype=numpy.float32)
	if len(arr) == 5:
		x = arr 

#pycrow.incoming_handler(incomming)

class zveno1(zencad.assemble.unit):
	def __init__(self, l):
		super().__init__()
		
		m = (
			cylinder(r=3, h=l) 
			+ cylinder(r=3, h=6, center=True).rotateX(deg(90)).up(l)
			+ cylinder(r=3, h=6, center=True).rotateX(deg(90))
		)
		self.set_shape(m)
		
		self.outrot = zencad.cynematic.rotator(
			ax = (0,1,0),
			name="zv.outrot",
			parent=self, 
			location=up(l))

o = zencad.cynematic.rotator(ax=(0,0,1))
o2 = zencad.cynematic.rotator(ax=(0,0,1))
a = zveno1(40)
b = zveno1(30)
c = zveno1(20)
d = zveno1(10)
e = zveno1(10)

d.relocate(rotate((0,0,1),deg(0)))

o.link(b)
#a.outrot.link(b)
b.outrot.link(c)
c.outrot.link(d)
#d.outrot.link(o2)
#e.outrot.link(o2)

#o.set_coord(deg(0))
#a.outrot.set_coord(deg(0))

b.outrot.set_coord(deg(45))
c.outrot.set_coord(deg(45))
d.outrot.set_coord(deg(0))
#o2.set_coord(deg(0))

o.location_update(deep=True, view=True)

chain = zencad.cynematic.cynematic_chain(d.outrot, o)

scn = zencad.Scene()
o.bind_scene_deep(scn)

zcur = d.outrot.global_location.translation().z

x = [0,deg(45),deg(45),0]
v = [0,0,0,0]
state = 0
lasttime = time.time()
def update(wdg):
	global state
	global lasttime
	curtime = time.time()
	deltatime = curtime - lasttime
	lasttime = curtime

	#print("eval:")
	senses = chain.sensivity(basis=o)

	cur = d.outrot.global_location.translation()
	print(cur)

	#print("senses", senses)
	
	if state == 0:
		vcoords, iters = zencad.malgo.naive_backpack((0,0,0,-10,0,0), [(*w, *v) for w, v in senses])
		if cur.x < -20: state = 1
	if state == 1:
		vcoords, iters = zencad.malgo.naive_backpack((0,0,0,0,0,-10), [(*w, *v) for w, v in senses])
		if cur.z < 15: state = 2
	if state == 2:
		vcoords, iters = zencad.malgo.naive_backpack((0,0,0,10,0,0), [(*w, *v) for w, v in senses])
		if cur.x > 20: state = 3
	if state == 3:
		vcoords, iters = zencad.malgo.naive_backpack((0,0,0,0,0,10), [(*w, *v) for w, v in senses])
		if cur.z > zcur: state = 0

	#print("vcoords", vcoords)
	
	#time.sleep(10000)

	for i in range(len(x)):
		v[i] = vcoords[i]
		x[i] += v[i] * deltatime * 2



	o.set_coord(x[0])
#	a.outrot.set_coord(x[1])
	b.outrot.set_coord(x[1])
	c.outrot.set_coord(x[2])
	#d.outrot.set_coord(x[4])
	
	o.location_update(deep=True, view=True)

	#wdg.set_eye(zencad.rotateZ(zencad.deg(deltatime*7))(wdg.eye()), orthogonal=True)

show(scn, animate=update)