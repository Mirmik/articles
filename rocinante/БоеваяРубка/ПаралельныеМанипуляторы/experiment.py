#!/usr/bin/env python3

from zencad import *
import zencad.assemble
import zencad.libs.bullet

import zencad.bullet

class leg(zencad.assemble.unit):
	h = 40
	def __init__(self, en=True):
		super().__init__()
		self.add(cylinder(r=3, h=self.h) + sphere(r=4).up(self.h))
		if en:
			self.rotator = zencad.assemble.rotator(
				location=up(self.h), 
				axis=(0,1,0), 
				parent=self)

tbox= box(20,20,10, center=True) -sphere(4).right(10) - sphere(4).left(10)
tbox= tbox.up(20)
tbox = zencad.assemble.unit(parts=[tbox])

tbox2 = box(40,40,15,center=True).up(15/2)
tbox2 = zencad.assemble.unit(parts=[tbox2])

aa = zencad.assemble.unit(parts=[box(4,4,4)], location=up(3))
a = zencad.assemble.rotator(axis=(0,1,0))
aa.link(a)
a.add_shape(sphere(4))
b = leg()
c = leg(False)

dd = zencad.assemble.unit(parts=[box(4,4,4)], location=up(3))
d = zencad.assemble.rotator(axis=(0,1,0))
dd.link(d)
d.add_shape(sphere(4))
e = leg()
f = leg(False)

a.link(b)
d.link(e)

t= zencad.assemble.unit(parts=[box(4,4)])

b.rotator.link(c)
e.rotator.link(f)

aa.move(40,0,0)
dd.move(-40,0,0)

b.rotator.set_coord(0)
#disp(a)
#disp(d)

sim = zencad.libs.bullet.simulation(scale_factor=1000, plane=True)
sim.set_gravity(*(0,0,-1))

sim.add_assemble(aa, fixed_base = True)
sim.add_assemble(dd, fixed_base = True)
sim.add_assemble(tbox)
sim.add_assemble(tbox2)

KP = 10
KPI = 1
KV = 0.0000001
KVI = 0.000001#2000000

serv0 = zencad.bullet.servo_controller3(kunit=a, simulation=sim)
serv0.init()
serv0.set_regs(
	pidspd=zencad.bullet.pid(kp=KV,ki=KVI),
	pidpos=zencad.bullet.pid(kp=KP,ki=KPI), 
	filt=1, maxforce=None)

serv1 = zencad.bullet.servo_controller3(kunit=b.rotator, simulation=sim)
serv1.init()
serv1.set_regs(
	pidspd=zencad.bullet.pid(kp=KV,ki=KVI),
	pidpos=zencad.bullet.pid(kp=KP,ki=KPI), 
	filt=1, maxforce=None)

serv2 = zencad.bullet.servo_controller3(kunit=d, simulation=sim)
serv2.init()
serv2.set_regs(
	pidspd=zencad.bullet.pid(kp=KV,ki=KVI),
	pidpos=zencad.bullet.pid(kp=KP,ki=KPI), 
	filt=1, maxforce=None)

serv3 = zencad.bullet.servo_controller3(kunit=e.rotator, simulation=sim)
serv3.init()
serv3.set_regs(
	pidspd=zencad.bullet.pid(kp=KV,ki=KVI),
	pidpos=zencad.bullet.pid(kp=KP,ki=KPI), 
	filt=1, maxforce=None)

#serv0.set_speed_target(1)
serv0.set_position_target(deg(45))
serv1.set_position_target(deg(-90))
serv2.set_position_target(deg(-45))
serv3.set_position_target(deg(90))

def animate(state):
	sim.step()

#	serv0.serve_spd_only(state.delta)
	serv0.serve(state.delta)
	serv1.serve(state.delta)
	serv2.serve(state.delta)
	serv3.serve(state.delta)

	print(serv0.pidspd.value(), serv0.pidspd.error)

show(animate=animate, animate_step=1/240)

