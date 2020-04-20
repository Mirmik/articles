#!/usr/bin/env python3

from zen2d import *
import random
import time

class hvat(zen2d.unit):
	def __init__(self):
		super().__init__()

		self.add(zen2d.iline((-10,0), (-10,10)))
		self.add(zen2d.iline((10,0), (10,10)))
	
		self.add(zen2d.iline((-10,0), (10,0)))
		
		self.add(zen2d.iline((-10,0), (10,10)))
		self.add(zen2d.iline((10,0), (-10,10)))

a = hvat()
b = hvat()
c = hvat()
cbody = hvat()

cu = unit()

a.relocate(translate(0,-80))
b.relocate(translate(80*math.sin(deg(60)),80*math.cos(deg(60))) * rotate(deg(120)))
c.relocate(translate(-80*math.sin(deg(60)),80*math.cos(deg(60))) * rotate(-deg(120)))

cpos = (a.global_location + b.global_location + c.global_location) / 3
cbody.relocate(cpos)

disp(a)
disp(b)
disp(c)
disp(cbody)

disp(iline_between(a,b))
disp(iline_between(b,c))
disp(iline_between(c,a))


disp(itail(cbody, step = 0.2))


La = cbody.global_location.inverse() * a.global_location
Lb = cbody.global_location.inverse() * b.global_location
Lc = cbody.global_location.inverse() * c.global_location

print(cbody.global_location.inverse() )
print(La)
print(Lb)
print(Lc)

#a.relocate(translate(0,20) * rotate(deg(30)))
#b.relocate(translate(90*math.cos(deg(60)),60*math.sin(deg(60))) * rotate(deg(130)))
#c.relocate(translate(-70*math.cos(deg(60)),50*math.sin(deg(60))) * rotate(-deg(100)))


cpos = (a.global_location + b.global_location + c.global_location) / 3
tpos = translate(50,0) * rotate(deg(60))

#D = transformation(deg(120), (0,100))

def random_trans(lin, ang):
	l = vector((random.random()-0.5)  * lin, (random.random()-0.5) * lin)
	a = (random.random()-0.5)  * ang

	return transformation(a,l)

#ar = random_trans(20, 1)
#br = random_trans(20, 1)
#cr = random_trans(20, 1)

ar  = nulltrans()
br  = nulltrans()
cr  = nulltrans()

G = -9.81


integ = nulltrans()

tstart = time.time()
lasttime = tstart
lpos = cbody.global_location
iter = 0
v_a_errinteg = nulltrans()
v_b_errinteg = nulltrans()
v_c_errinteg = nulltrans()
tainteg = nulltrans()
tbinteg = nulltrans()
tcinteg = nulltrans()
vmodel_last = nulltrans()
vamodel_last = nulltrans()
vbmodel_last = nulltrans()
vcmodel_last = nulltrans()

class state:
	def __init__(self, pos):
		self.curpos = pos
		self.spd = nulltrans()
		self.mspd = nulltrans()

		self.espd = nulltrans()
		self.espd_integral = nulltrans()
		self.tsig_integral = nulltrans()

	def newpos(self, pos, delta):
		self.spd = (pos - self.curpos) / delta
		self.espd = self.spd - self.mspd
		self.espd_integral += self.espd.scale(delta)
		self.curpos = pos

	def new_tsig(self, tsig, delta):
		self.tsig = tsig
		self.tsig_integral += tsig.scale(delta)

	def set_model_speed(self, mspd):
		self.mspd = mspd

states = [state(a.global_location), state(b.global_location), state(c.global_location)]

def animate():
	global iter, tstart, lpos, verrinteg
	global tpos
	global lasttime, integ, tainteg, tbinteg, tcinteg, vmodel_last
	cpos = (a.global_location + b.global_location + c.global_location) / 3

	if iter < 50:
		iter += 1
		return

	if iter == 50:
		tstart = time.time()
		lasttime = tstart
		iter += 1

	curtime = time.time()
	delta = curtime - lasttime
	lasttime = curtime
	t = curtime - tstart

	vcur = (cpos - lpos) / delta
	lpos = cpos 

	states[0].newpos(a.global_location, delta)
	states[1].newpos(b.global_location, delta)
	states[2].newpos(c.global_location, delta)

	#delta = delta / 10
	

	#a.relocate(translate(-t, 0))


	#a_target = transformation(deg(60), (-50, -50))

	#a_error = a_target - a.global_location
	#v = a_error.scale(K)

	#print(v)

	ar = random_trans(20, 1)
	br = random_trans(20, 1)
	cr = random_trans(20, 1)


#	va = La - (cbody.global_location.inverse() * a.global_location)
#	vb = Lb - (cbody.global_location.inverse() * b.global_location)
#	vc = Lc - (cbody.global_location.inverse() * c.global_location)

	Kupr = 1
	if t % 20 > 10:
		tpos = tpos + transformation(0,(10,10)).scale(delta)
	else:
		tpos = tpos + transformation(0,(10,-10)).scale(delta)

	error = tpos - cpos
	integ = integ + error.scale(delta)
	
	Ta = La - (cbody.global_location.inverse() * a.global_location)
	Tb = Lb - (cbody.global_location.inverse() * b.global_location)
	Tc = Lc - (cbody.global_location.inverse() * c.global_location) 

	terr=[0] * 3

	terr[0] = Ta.rotate_by(cbody.global_location).scale(Kupr)
	terr[1] = Tb.rotate_by(cbody.global_location).scale(Kupr)
	terr[2] = Tc.rotate_by(cbody.global_location).scale(Kupr)

	tasig = terr[0] + translate(0,G)
	tbsig = terr[1] + translate(0,G)
	tcsig = terr[2] + translate(0,G)
	#tainteg += tasig.scale(delta)
	#tbinteg += tbsig.scale(delta)
	#tcinteg += tcsig.scale(delta)

	#vtarget = nulltrans()

	T = 1
	dzeta = 2

	Ki = 1/T**2
	K = Ki * 2 * dzeta * T 

	Kcomp = 1

	states[0].new_tsig(tasig, delta)
	states[1].new_tsig(tbsig, delta)
	states[2].new_tsig(tcsig, delta)

	vmodel = error.scale(K) + integ.scale(Ki)
	vtarget = vmodel

	vtarget2 = nulltrans()

	va_model = vtarget.kinematic_carry((a.global_location + ar - cbody.global_location).lin)
	vb_model = vtarget.kinematic_carry((b.global_location + br - cbody.global_location).lin)
	vc_model = vtarget.kinematic_carry((c.global_location + cr - cbody.global_location).lin)

	va = va_model + tasig.scale(Kcomp)# - states[0].espd_integral.scale(Kicomp)
	vb = vb_model + tbsig.scale(Kcomp)# - states[1].espd_integral.scale(Kicomp)
	vc = vc_model + tcsig.scale(Kcomp)# - states[2].espd_integral.scale(Kicomp)

	print()
	print()
	print(vmodel)
	print("a", tasig)
	print("b", tbsig)
	print("c", tcsig)

	a.relocate(a.global_location + va.scale(delta))
	b.relocate(b.global_location + vb.scale(delta))
	c.relocate(c.global_location + vc.scale(delta))

	cbody.relocate(cpos)

	states[0].set_model_speed(va)
	states[1].set_model_speed(vb)
	states[2].set_model_speed(vc)

show(animate)