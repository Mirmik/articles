#!/usr/bin/env python3

from zencad import *
import zencad.assemble
import zencad.libs.bullet
import zencad.libs.kinematic

import zencad.bullet

class leg(zencad.assemble.unit):
	h = 800
	hb = 800
	def __init__(self, en=True):
		super().__init__()
		
		m = cylinder(r=60, h=self.hb)
		if en:
			m += sphere(r=80).up(self.h)
		self.add(m)
		if en:
			self.rotator = zencad.assemble.rotator(
				location=up(self.h), 
				axis=(0,1,0), 
				parent=self) 
		else:
			self.output1 = zencad.assemble.unit(location=up(self.h), parent=self)
			self.output2 = zencad.assemble.unit(parts=[sphere(80)], parent=self.output1)

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

aa = zencad.assemble.unit(parts=[box(40,40,40,center=True)], location=up(30))
a = zencad.assemble.rotator(axis=(0,1,0))
aa.link(a)
a.add_shape(sphere(80))
b = leg()
c = leg(False)

dd = zencad.assemble.unit(parts=[box(40,40,40,center=True)], location=up(30))
d = zencad.assemble.rotator(axis=(0,1,0))
dd.link(d)
d.add_shape(sphere(80))
e = leg()
f = leg(False)

a.link(b)
d.link(e)

#t= zencad.assemble.unit(parts=[box(40,40)])

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

KP = 24#16
#KPI = 0
KPI = 15#30
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

chain0 = zencad.libs.kinematic.kinematic_chain(c.output2)
chain1 = zencad.libs.kinematic.kinematic_chain(f.output2)

tgt0 = disp(cylinder(r=10,h=800,center=True).rotateX(deg(90)), color.red)
tgt1 = disp(cylinder(r=10,h=800,center=True).rotateX(deg(90)), color.red)

#zencad.bullet.enable_force_torque_sensor(c.output)
#zencad.bullet.enable_force_torque_sensor(f.output)

i0=screw()
i1=screw()

def animate(state):
	global i0
	global i1

	tim = state.loctime

	sim.step()

#	serv0.serve_spd_only(state.delta)
	serv0.serve(state.delta)
	serv1.serve(state.delta)
	serv2.serve(state.delta)
	serv3.serve(state.delta)

	si = math.sin((tim-10) / 4)
	co = math.cos((tim-10) / 4)

	if tim < 10:
		target0 = vector3(180,0,400) + vector3(0,0,50) * tim
		target1 = vector3(-180,0,400) + vector3(0,0,50) * tim
		target = vector3(0,0,400) + vector3(0,0,50) * tim
		i0=screw()
		i1=screw()
	else:
		target0 = vector3(180,0,750) + vector3(0,0,150) * co + vector3(300,0,0) * si
		target1 = vector3(-180,0,750) + vector3(0,0,150) * co + vector3(300,0,0) * si
		target = vector3(0,0,750) + vector3(0,0,150) * co + vector3(300,0,0) * si

	error0 = target0 - c.output2.global_location.translation() 
	error1 = target1 - f.output2.global_location.translation() 

	target = translate(target)
	current = ta.global_location

	error = current.inverse() * target

	errscr = screw.from_trans(error)
	i0 += errscr * state.delta

	arm0 = c.output2.global_location.translation() - current.translation()
	u0 = (errscr*1+i0*0.1).kinematic_carry(arm0) 
	arm1 = f.output2.global_location.translation() - current.translation()
	u1 = (errscr*1+i0*0.1).kinematic_carry(arm1) 

	#i0 += u0*state.delta
	#i1 += u1*state.delta 
	aaa = zencad.bullet.get_force_torque_sensor(c.output2).lin
	bbb = zencad.bullet.get_force_torque_sensor(f.output2).lin

	if tim < 10:
		sigs0 = chain0.decompose_linear(error0 + aaa*0, use_base_frame=True)
		sigs1 = chain1.decompose_linear(error1 + bbb*0, use_base_frame=True)
	else:
		sigs0 = chain0.decompose_linear(u0.lin*2 - arm0*0.4 + aaa*0, use_base_frame=True)
		sigs1 = chain1.decompose_linear(u1.lin*2 - arm1*0.4 + bbb*0, use_base_frame=True)


	if tim < 10:
		KOMPKOEFF = 0.2
	else:
		KOMPKOEFF = 0.2
	serv0.set_speed2(sigs0[0] - serv0.force * KOMPKOEFF)
	serv1.set_speed2(sigs0[1] - serv1.force * KOMPKOEFF)
	serv2.set_speed2(sigs1[0] - serv2.force * KOMPKOEFF)
	serv3.set_speed2(sigs1[1] - serv3.force * KOMPKOEFF)

	print("F0:", serv0.force, serv2.force)
	print("F1:", serv1.force, serv3.force)
	print("aaa", aaa)
	print("bbb", bbb)

	tgt0.relocate(move(target0))
	tgt1.relocate(move(target1))

show(animate=animate, animate_step=1/240)

