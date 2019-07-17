#!/usr/bin/env python3

from zencad import *
from zencad.controllers import *

class zv(zencad.controllers.Unit):
	def __init__(self, l):
		super().__init__()
		
		self.set_shape(cylinder(r=3, h=l))
		
		self.outrot = zencad.controllers.CynematicUnit(
			name="zv.outrot",
			parent=self, 
			location=up(l))


a = zv(40)
b = zv(30)

a.outrot.link(b)
a.outrot.output.relocate(rotate((0,1,0),deg(45)))

a.location_update_deep()
a.print_tree()

scn = zencad.Scene()
a.bind_scene_deep(scn)



show(scn)