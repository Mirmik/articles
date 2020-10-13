#!/usr/bin/env python3

from zencad import *
import zencad.assemble
import zencad.libs.bullet

import zencad.bullet

class leg(zencad.assemble.unit):
	h = 80
	def __init__(self, en=True):
		super().__init__()
		self.add(cylinder(r=6, h=self.h) + sphere(r=8).up(self.h))
		if en:
			self.rotator = zencad.assemble.rotator(
				location=up(self.h), 
				axis=(0,1,0), 
				parent=self)

tbox= box(40,40,20, center=True) -sphere(4).right(10) - sphere(4).left(10)
tbox= tbox.up(80)
#tbox = zencad.assemble.unit(parts=[tbox])

tbox2 = box(80,80,30,center=True).up(60/2)

aa = zencad.assemble.unit(parts=[box(4,4,4)], location=up(3))
a = zencad.assemble.rotator(axis=(0,1,0))
aa.link(a)
a.add_shape(sphere(8))
b = leg()
c = leg(False)

dd = zencad.assemble.unit(parts=[box(4,4,4)], location=up(3))
d = zencad.assemble.rotator(axis=(0,1,0))
dd.link(d)
d.add_shape(sphere(8))
e = leg()
f = leg(False)

a.link(b)
d.link(e)

t= zencad.assemble.unit(parts=[box(4,4)])

b.rotator.link(c)
e.rotator.link(f)

aa.move(80,0,0)
dd.move(-80,0,0)

b.rotator.set_coord(0)
#disp(a)
#disp(d)

sim = zencad.libs.bullet.simulation(plane=True)
sim.set_gravity(*(0,0,-10))

sim.add_assemble(aa, fixed_base = True)
sim.add_assemble(dd, fixed_base = True)
#sim.add_assemble(tbox)
sim.add_body(tbox, collision=zencad.bullet.volumed_collision(tbox))
sim.add_body(tbox2, collision=zencad.bullet.volumed_collision(tbox2))

KP = 16
KPI = 30
KV = 0.000002
KVI = 0.00001#2000000

serv0 = zencad.bullet.servo_controller3(kunit=a, simulation=sim)
serv0.init()
serv0.set_regs(
	pidspd=zencad.bullet.pid(kp=KV,ki=KVI, clamp = 10),
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

#serv0.set_speed_target(3)
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

	print(serv0.pidpos.value(), serv1.pidpos.value())

show(animate=animate, animate_step=1/240)

