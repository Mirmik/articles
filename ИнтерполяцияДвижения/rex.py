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
		self.set_color(0.6,0.6,0.6,0.5)
		
		self.outrot = zencad.cynematic.rotator(
			ax = (0,1,0),
			name="zv.outrot",
			parent=self, 
			location=up(l))

o = zencad.cynematic.actuator(ax=(1,0,0))
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
d.outrot.link(e)
#e.outrot.link(o2)

#o.set_coord(deg(0))
#a.outrot.set_coord(deg(0))

b.outrot.set_coord(deg(45))
c.outrot.set_coord(deg(45))
d.outrot.set_coord(deg(0))
#o2.set_coord(deg(0))

o.location_update(deep=True, view=True)

chain = zencad.cynematic.cynematic_chain(e, o)

scn = zencad.Scene()
o.bind_scene_deep(scn)

zcur = d.outrot.global_location.translation().z

x = [0,deg(45),deg(45),deg(10)]
v = [0,0,0,0]
state = 0
lasttime = time.time()

minmaxs = (None, (-deg(150), deg(150)), (-deg(150), deg(150)), (-deg(90), deg(90)))
minmaxs = (None, (deg(0), deg(150)), (-deg(120), deg(120)), (-deg(90), deg(90)))

tmodel = d.outrot.global_location

ccc = zencad.assemble.unit(shape = sphere(r=1))
ccc.bind_scene_deep(scn)

iteration = 0
def update(wdg):
	global state
	global tmodel
	global iteration
	global lasttime
	curtime = time.time()
	deltatime = curtime - lasttime
	lasttime = curtime

	if iteration == 0:
		iteration += 1
		return

	#print("eval:")
	senses = chain.sensivity()
	
	penalty = [0,0,0,0]
	for i in range(len(x)):
		k = 0
		if minmaxs[i]:
			if x[i] > minmaxs[i][1]: 
				k = 1
			elif x[i] < minmaxs[i][0]: 
				k = -1
		else: 
			k = 0
		penalty[i] = k


	#if state == 0:
	#	target = (0,0,0,-10,0,0)
	#	if cur.x < -20: state = 1
	#elif state == 1:
	#	target = (0,0,0,0,0,-10)
	#	if cur.z < 15: state = 2
	#elif state == 2:
	#	target = (0,0,0,10,0,0)
	#	if cur.x > 20: state = 3
	#elif state == 3:
	#	target = (0,0,0,0,0,10)
	#	if cur.z > zcur: state = 0

	TSPD = 10
	DELTATIME= deltatime
	print(deltatime)
	K = 10

	tmdel_position = tmodel.translation()

	if state == 0:
		tspd = numpy.array([-TSPD,0,0])
		if tmdel_position.x < -20: state = 1
	elif state == 1:
		tspd = numpy.array([0,0,-TSPD])
		if tmdel_position.z < 15: state = 2
	elif state == 2:
		tspd = numpy.array([TSPD,0,0])
		if tmdel_position.x > 20: state = 3
	elif state == 3:
		tspd = numpy.array([0,0,TSPD])
		if tmdel_position.z > zcur: state = 0

	tmodel = pyservoce.translate(*(tspd * DELTATIME)) * tmodel
	current = e.global_location

	ccc.relocate(tmodel)

	ftrans = current.inverse() * tmodel
	#ftrans = current * tmodel.inverse()
	#ftrans = tmodel.inverse() * current
	#ftrans = tmodel * current.inverse()
	ttrans = ftrans.translation() * K
	rtrans = ftrans.rotation().rotation_vector() * K 
	#print(ftrans.rotation())
	#print(rtrans)

	#exit(0)
	#print("ttrans", ttrans)

	target = (*rtrans,*ttrans)

	#vcoords, iters = zencad.malgo.naive_backpack(target, koeffs=[1,1,1,1], maxiters=100, alpha=0.5, 
	#	penalty=penalty, 
	#	vectors=[(*w, *v) for w, v in senses])
	
	vcoords, iters = zencad.malgo.svd_backpack(target, 
		penalty=penalty, 
		koeffs=[10,1,1,1],
		vectors=[(*w, *v) for w, v in senses])
	

	for i in range(len(x)):
		v[i] = vcoords[i]
		x[i] += v[i] * DELTATIME

	o.set_coord(x[0])
#	a.outrot.set_coord(x[1])
	b.outrot.set_coord(x[1])
	c.outrot.set_coord(x[2])
	d.outrot.set_coord(x[3])
	
	o.location_update(deep=True, view=True)
	ccc.location_update(view=True)

	#wdg.set_eye(zencad.rotateZ(zencad.deg(deltatime*7))(wdg.eye()), orthogonal=True)

show(scn, animate=update)