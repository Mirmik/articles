#!/usr/bin/env python3

from zencad import *
import zencad.assemble
import zencad.cynematic

def pal(u):
	m = cylinder(r=3, h= u) - halfspace().rotateX(deg(90)).forw(2) + sphere(r = 3).up(u) 
	return m.rotateZ(deg(90))


class palcls(zencad.assemble.unit):
	h = 30

	def __init__(self):
		super().__init__()
		self.shp = cylinder(r=3, h=self.h)
		self.set_shape(self.shp)
		self.out = zencad.cynematic.rotator(ax=(0,1,0), location=up(self.h), parent=self)
		self.palu = zencad.assemble.unit(shape=pal(30))
		self.out.link(self.palu)

class basecls(zencad.assemble.unit):
	def __init__(self):
		super().__init__()
		self.set_shape(box(10,50, 8, center=True))
		
		self.aout = zencad.cynematic.rotator(ax=(0,1,0), parent=self)
		self.bout = zencad.cynematic.rotator(ax=(0,1,0), parent=self)
		self.cout = zencad.cynematic.rotator(ax=(0,1,0), parent=self)
		self.dout = zencad.cynematic.rotator(ax=(0,1,0), parent=self)

		self.apalu = palcls()
		self.bpalu = palcls()
		self.cpalu = palcls()
		self.dpalu = palcls()

		self.aout.link(self.apalu)
		self.bout.link(self.bpalu)
		self.cout.link(self.cpalu)
		self.dout.link(self.dpalu)

		self.aout.relocate(right(-5) * forw(20) * rotateY(-deg(90)))
		self.bout.relocate(right(5) * forw(20) * rotateY(deg(90)) * rotateZ(deg(180)))
		self.cout.relocate(right(-5) * back(20) * rotateY(-deg(90)))
		self.dout.relocate(right(5) * back(20) * rotateY(deg(90)) * rotateZ(deg(180)))

		self.out = [self.aout, self.bout, self.cout, self.dout] 
		self.palu = [self.apalu, self.bpalu, self.cpalu, self.dpalu]
		
		self.sout = [ s.out for s in self.palu ]

base = basecls() 

for l in base.out:
	l.set_coord(deg(-45), deep=True, view=True)

for l in base.sout:
	l.set_coord(deg(-45), deep=True, view=True)

base.location_update(deep=True)
#disp(base.apalu, deep=True)
disp(base, deep=True)

show()