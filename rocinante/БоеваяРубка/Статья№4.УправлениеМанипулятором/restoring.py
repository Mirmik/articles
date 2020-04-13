#!/usr/bin/env python3

#!/usr/bin/env python3 
"""
ZenCad example: manual-control

We can control current object position in real time.
In that example we create special widget to change link`s positions by sliders.
"""

from zencad import *
import zencad.assemble
import zencad.libs.kinematic
from zencad.libs.screw import screw
import zencad.malgo

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy

import time

CTRWIDGET = None
SLDS = None

XSLD = None
YSLD = None
ZSLD = None

numpy.set_printoptions(formatter={'float':lambda x: '%010.3f'%x })

vcoords = [0] * 4

class Slider(QSlider):
	def __init__(self):
		super().__init__(Qt.Horizontal)
		self.setRange(-5000,5000)
		self.setValue(0)
		self.setSingleStep(1)


class link(zencad.assemble.unit):
	def __init__(self, h=60, ax=(0,1,0)):
		super().__init__()
		if ax != (0,0,1):
			self.add_shape(cylinder(5,h) + cylinder(6,10,center=True).transform(up(h) * short_rotate((0,0,1), ax)))
		else:
			self.add_shape(cylinder(5,h))	
		self.rotator = zencad.assemble.rotator(parent=self, ax=ax, location=up(h))

r = zencad.assemble.rotator(ax=(0,0,1))
a = link(ax=(0,1,0))
b = link(ax=(1,0,0))
c = link(ax=(0,1,0))

r.link(a)
a.rotator.link(b)
b.rotator.link(c)

LINKS = [a,b,c]

rots = [r] + [ a.rotator for a in LINKS ]

chain = zencad.libs.kinematic.kinematic_chain(LINKS[-1].rotator.output)

disp(a, color=(0.5,0.5,0.6,0.5))

def preanimate(widget, animate_thread):
	global CTRWIDGET, XSLD, YSLD, ZSLD
	CTRWIDGET = QWidget()
	layout = QVBoxLayout()
	XSLD = Slider()
	YSLD = Slider()
	ZSLD = Slider()

	XSLD.setValue(2000)
	YSLD.setValue(2000)
	ZSLD.setValue(2000)

	layout.addWidget(XSLD)
	layout.addWidget(YSLD)
	layout.addWidget(ZSLD)

	CTRWIDGET.setLayout(layout)
	CTRWIDGET.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Dialog)
	CTRWIDGET.show()

tgtshp = sphere(5)
ctr = disp(tgtshp)

import random
N = 8
M = 4
Larr = [ translate(random.random()-0.5, random.random()-0.5, random.random()-0.5) for i in range(N) ]
LconstT = [vector3(random.random()-0.5, random.random()-0.5, random.random()-0.5) for i in range(N) ]
LconstR = [vector3(random.random()-0.5, random.random()-0.5, random.random()-0.5) * 0.001 for i in range(N) ]
LW = [vector3(random.random()-0.5, random.random()-0.5, random.random()-0.5) * 0.001 for i in range(M) ]

NUMS = [1,3,5]

LconstT[2] = vector3(0,0,60)
LconstT[4] = vector3(0,0,60)
LconstT[6] = vector3(0,0,60)

LW[0] = vector3(0,0,1)
LW[1] = vector3(0,1,0)
LW[2] = vector3(1.00,0,0)

def update_Larr():
	global Larr
	
	Larr = [None] * N

	rot = [vector3(0,0,0)] * N
	crot = [vector3(0,0,0)] * N
	k = 0
	for i in range(N):
		crot[i] = vector3(LconstR[i])

		if i in NUMS:
			if (LW[k].length() < 1e-5):
				break
			rot[i] = rots[k].coord * vector3(LW[k])
			k += 1


	for i in range(M):
		if LW[i].length() >= math.pi * 2:
			LW[i] = vector3(0,0,0)

	for i in range(N):
		Larr[i] = translate(LconstT[i]) * rotate((crot[i] + vector3(*rot[i])).length(), (crot[i] + vector3(*rot[i])).normalize())



def Lprod(a, b):
	P = nulltrans()
	for i in range(a,b):
		P = P * Larr[i]
	return P

def nullify_translate(i):
		P = Larr[i]
		s = screw.from_trans(P)
		s.lin = vector3(0,0,0)
		P=s.to_trans()
		Larr[i] = P

def nullify_rotation(i):
		P = Larr[i]
		s = screw.from_trans(P)
		s.ang = vector3(0,0,0)
		P=s.to_trans()
		Larr[i] = P

def nullify_rotation_P(P):
		s = screw.from_trans(P)
		s.ang = vector3(0,0,0)
		P=s.to_trans()
		return P

itera =0
ccc = [ disp(sphere(3), color=(1,0,0,0.5)) for i in range(N) ]

accum = [numpy.array([0,0,0])] * N
accum2 = [numpy.array([0,0,0])] * N
K = 1
stime = time.time()
lasttime = stime
def animate(wdg):
	global itera
	global lasttime
	global vcoords
	global M
	curtime = time.time()
	DELTA = curtime - lasttime
	lasttime = curtime

	for i in range(M):
		if rots[i].coord > math.pi * 2: rots[i].set_coord(rots[i].coord - math.pi * 2)
		if rots[i].coord < - math.pi * 2: rots[i].set_coord(rots[i].coord + math.pi * 2)

	DELTA = DELTA * 0.4

	target_location = translate(XSLD.value()/5000*120, YSLD.value()/5000*120, ZSLD.value()/5000*120)

	sens = chain.sensivity()
	error = LINKS[-1].rotator.output.global_location.inverse() * target_location

	ttrans = error.translation() * K
	rtrans = error.rotation().rotation_vector() * K 

	target = ttrans
	vcoords, iters = zencad.malgo.svd_backpack(target, vectors=[v for w,v in sens ])

	r.set_coord(r.coord + vcoords[0] * DELTA)
	for i in range(len(LINKS)):
		LINKS[i].rotator.set_coord(LINKS[i].rotator.coord + vcoords[i+1] * DELTA)

	ctr.relocate(target_location)
	a.location_update(deep=True)

	PCur = LINKS[-1].rotator.output.global_location

	#print(PCur.inverse() * LCur)

	simplified_chain = chain.simplify_chain(chain.chain)

	N = len(simplified_chain)
	M = len(sens) 

	LCur = Lprod(0, N) 
	ERR = PCur.inverse() * LCur

	EpsL = [0] * N

	print()
	PPP = [ simplified_chain[i] if isinstance(chain.simplified_chain[i], pyservoce.libservoce.transformation) else chain.simplified_chain[i].location for i in reversed(range(N)) ]

	#TCHANGE = 10

	def Pprod(a, b):
		P = nulltrans()
		for i in range(a,b):
			P = P * PPP[i]
		return P


	

	def f0(i):
		return Larr[i].inverse() * PPP[i]

	def f1(i, t):
		return Larr[i].inverse() * Pprod(i,t) * Lprod(i+1,M).inverse()

	def f2(i, s, t):
		return Lprod(s,i+1).inverse() * Pprod(s,t) * Lprod(i+1,t).inverse()

	def f3(i, s, t):
		return Lprod(s,i+1).inverse() * nullify_rotation_P(Pprod(s,t)) * Lprod(i+1,t).inverse()

	def flat(E, alpha = 1):
		#if curtime - stime < TCHANGE:
		#else:
		
		#	alpha = 0.1

		E = screw.from_trans(E)

		rot = E.ang
		mov = E.lin

		E = screw(ang=rot, lin=mov) * alpha
		#print(E)
		return E.to_trans()

	EpsL = [nulltrans()] * N 


	#for i in range(0,N):
	#	EpsL[i] = EpsL[i] * flat(f3(i, 0, i+1), 0.5)

	for i in range(0,3):
		EpsL[i] = EpsL[i] * flat(f3(i, 0, 3+1), 0.2)

	for i in range(0,5):
		EpsL[i] = EpsL[i] * flat(f3(i, 0, 5+1), 0.2)

	for i in range(0,7):
		EpsL[i] = EpsL[i] * flat(f3(i, 0, 7+1), 0.2)

	for i in range(0,N):
		Larr[i] = Larr[i] * EpsL[i]



#	for i in range(0,N):
#		EpsL[i] = flat(f2(i, i, N), 0.5)

#	for i in range(0,N):
#		Larr[i] = Larr[i] * EpsL[i]
#		print(Larr[i])


	nullify_translate(0)
	nullify_translate(1)
	nullify_translate(3)
	nullify_translate(5)
	nullify_translate(7)

	nullify_rotation(0)
	nullify_rotation(2)
	nullify_rotation(4)
	nullify_rotation(6)
	nullify_rotation(7)

	print()
	print("P",PPP)
	print("L",Larr)

	def to_np(v):
		return numpy.array([v.x, v.y, v.z])


	for i in range(len(ccc)):
		ccc[i].relocate(Lprod(0, i))

	#update_Larr()

	time.sleep(0.01)

def close_handle():
	CTRWIDGET.close()

show(animate=animate, preanimate=preanimate, close_handle=close_handle)