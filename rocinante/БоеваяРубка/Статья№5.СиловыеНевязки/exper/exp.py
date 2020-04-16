#!/usr/bin/env python3

from zen2d import *

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

a.relocate(translate(0,0))
c.relocate(translate(40,40) * rotate(deg(120)))
b.relocate(translate(-40,40) * rotate(deg(-120)))

disp(a)
disp(b)
disp(c)

disp(iline_between(a,b))
disp(iline_between(b,c))
disp(iline_between(c,a))

show()