#!/usr/bin/env python3

from zencad import *
import zencad.assemble
import zencad.libs.bullet
import zencad.libs.kinematic

import zencad.bullet

class leg(zencad.assemble.unit):
	h = 800
	def __init__(self, en=True):
		super().__init__()
		self.add(cylinder(r=60, h=self.h) + sphere(r=80).up(self.h))
		if en:
			self.rotator = zencad.assemble.rotator(
				location=up(self.h), 
				axis=(0,1,0), 
				parent=self)
		else:
			self.output = zencad.assemble.unit(parts=[sphere(1)], location=up(self.h), parent=self)

#tbox= box(40,40,20, center=True) -box(20,center=True).right(20) - box(20,center=True).left(20)
#tbox= tbox.up(80)
#tbox = zencad.assemble.unit(parts=[tbox])

ta = zencad.assemble.unit(parts=[box(220,220,160,center=True)])
zencad.assemble.unit(parts=[box(400,400,50,center=True)], location=up(80+25), parent=ta)
zencad.assemble.unit(parts=[box(400,400,50,center=True)], location=down(80+25), parent=ta)
zencad.assemble.unit(parts=[box(400,90,160,center=True)], location=forw(110+45), parent=ta)
zencad.assemble.unit(parts=[box(400,90,160,center=True)], location=back(110+45), parent=ta)

ta.up(1000)#.forw(1000)

tbox2 = box(800,800,350,center=True).up(600/2)

aa = zencad.assemble.unit(parts=[box(40,40,40)], location=up(30))
a = zencad.assemble.rotator(axis=(0,1,0))
aa.link(a)
a.add_shape(sphere(80))
b = leg()
c = leg(False)

dd = zencad.assemble.unit(parts=[box(40,40,40)], location=up(30))
d = zencad.assemble.rotator(axis=(0,1,0))
dd.link(d)
d.add_shape(sphere(80))
e = leg()
f = leg(False)

a.link(b)
d.link(e)

t= zencad.assemble.unit(parts=[box(40,40)])

b.rotator.link(c)
e.rotator.link(f)

aa.move(800,0,50)
dd.move(-800,0,50)

#a.set_coord(deg(45))
#b.rotator.set_coord(-90)
#d.set_coord(0)
#e.rotator.set_coord(0)
#disp(a)
#disp(d)

sim = zencad.libs.bullet.simulation(plane=True)
sim.set_gravity(*(0,0,-10))

sim.add_assemble(aa, fixed_base = True)
sim.add_assemble(dd, fixed_base = True)
#sim.add_assemble(tbox)
sim.add_assemble(ta)
sim.add_body(tbox2)

KP = 16
KPI = 30
KV = 0.2
KVI = 0.01#2000000

CLAMP0 = 6
CLAMP1 = 0.11

serv0 = zencad.bullet.servo_controller3(kunit=a, simulation=sim)
serv0.init()
serv0.set_regs(
	pidspd=zencad.bullet.pid(kp=KV,ki=KVI, clamp = CLAMP0),
	pidpos=zencad.bullet.pid(kp=KP,ki=KPI, clamp = CLAMP1), 
	filt=1, maxforce=None)

serv1 = zencad.bullet.servo_controller3(kunit=b.rotator, simulation=sim)
serv1.init()
serv1.set_regs(
	pidspd=zencad.bullet.pid(kp=KV,ki=KVI, clamp = CLAMP0),
	pidpos=zencad.bullet.pid(kp=KP,ki=KPI, clamp = CLAMP1), 
	filt=1, maxforce=None)

serv2 = zencad.bullet.servo_controller3(kunit=d, simulation=sim)
serv2.init()
serv2.set_regs(
	pidspd=zencad.bullet.pid(kp=KV,ki=KVI, clamp = CLAMP0),
	pidpos=zencad.bullet.pid(kp=KP,ki=KPI, clamp = CLAMP1), 
	filt=1, maxforce=None)

serv3 = zencad.bullet.servo_controller3(kunit=e.rotator, simulation=sim)
serv3.init()
serv3.set_regs(
	pidspd=zencad.bullet.pid(kp=KV,ki=KVI, clamp = CLAMP0),
	pidpos=zencad.bullet.pid(kp=KP,ki=KPI, clamp = CLAMP1), 
	filt=1, maxforce=None)

#serv0.set_speed_target(3)
serv0.set_position_target(deg(45))
serv1.set_position_target(deg(-90))
serv2.set_position_target(deg(-45))
serv3.set_position_target(deg(90))

chain0 = zencad.libs.kinematic.kinematic_chain(c.output)
chain1 = zencad.libs.kinematic.kinematic_chain(f.output)

tgt0 = disp(cylinder(r=10,h=800,center=True).rotateX(deg(90)), color.red)
tgt1 = disp(cylinder(r=10,h=800,center=True).rotateX(deg(90)), color.red)

def animate(state):
	tim = state.loctime

	sim.step()

#	serv0.serve_spd_only(state.delta)
	serv0.serve(state.delta)
	serv1.serve(state.delta)
	serv2.serve(state.delta)
	serv3.serve(state.delta)

	print(tim)
	target0 = vector3(200,0,450) + vector3(0,0,10) * tim
	target1 = vector3(-200,0,450) + vector3(0,0,10) * tim

	error0 = target0 - c.output.global_location.translation() 
	error1 = target1 - f.output.global_location.translation() 

	sigs0 = chain0.decompose_linear(error0, use_base_frame=True)
	sigs1 = chain1.decompose_linear(error1, use_base_frame=True)

	serv0.set_speed2(sigs0[0])
	serv1.set_speed2(sigs0[1])
	serv2.set_speed2(sigs1[0])
	serv3.set_speed2(sigs1[1])

	#print(serv0.pidpos.value(), serv1.pidpos.value(), serv0.pidspd.value(), serv1.pidspd.value())
	print(serv0.pidspd.integral, serv1.pidspd.integral, serv2.pidspd.integral, serv3.pidspd.integral)
	print(serv0.pidpos.integral, serv1.pidpos.integral, serv2.pidpos.integral, serv3.pidpos.integral)
	#print(serv0.poserr)

	tgt0.relocate(move(target0))
	tgt1.relocate(move(target1))

show(animate=animate, animate_step=1/240)

