#!/usr/bin/env python3

from zencad import *
import zencad.assemble
import zencad.libs.bullet

class leg(zencad.assemble.unit):
	h = 20
	def __init__(self, en=True):
		super().__init__()
		self.add(cylinder(r=3, h=self.h) + sphere(r=4).up(self.h))
		if en:
			self.rotator = zencad.assemble.rotator(
				location=up(self.h), 
				axis=(0,1,0), 
				parent=self)

aa = zencad.assemble.unit(parts=[box(4,4,4)])
a = zencad.assemble.rotator(axis=(0,1,0))
aa.link(a)
a.add_shape(sphere(4))
b = leg()
c = leg(False)

dd = zencad.assemble.unit(parts=[box(4,4,4)])
d = zencad.assemble.rotator(axis=(0,1,0))
dd.link(d)
d.add_shape(sphere(4))
e = leg()
f = leg(False)

a.link(b)
d.link(e)

b.rotator.link(c)
e.rotator.link(f)

aa.move(20,0,0)
dd.move(-20,0,0)

b.rotator.set_coord(math.pi/4)
#disp(a)
#disp(d)

sim = zencad.libs.bullet.simulation()
sim.set_gravity(*(0,0,-10))

sim.add_assemble(aa, fixed_base = True)
sim.add_assemble(dd, fixed_base = True)


def animate(wdg):
	sim.step()

show(animate=animate)

