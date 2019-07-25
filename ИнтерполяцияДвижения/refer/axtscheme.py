#!/usr/bin/env python3

from zencad import *
import zencad.assemble
import zencad.cynematic
import pyservoce

scn = Scene()
view = scn.viewer.create_view()

view.set_triedron(False)
view.set_background(pyservoce.white)
scn.viewer.set_triedron_axes(False)

class zv(zencad.assemble.unit):
	def __init__(self, location=None):
		super().__init__()
		self.shape = box(30, 30, 15).left(5) - box(20, 30, 10).left(0) 
		self.set_color(0.6,0.6,0.6,0.8)
		if location: self.relocate(location)
		self.upper = zencad.assemble.unit(location=up(15)*forw(15)*right(10), parent=self)
		self.upper.add_triedron(arrlen=4, width=2, length=20)
		self.upper.xaxis.set_color(pyservoce.black)
		self.upper.yaxis.set_color(pyservoce.black)
		self.upper.zaxis.set_color(pyservoce.black)

base = box(20, 200, 10)

scn.add(base.unlazy(), color = (0.6,0.6,0.6))

a = zv()
b = zv(location=right(50))
c = zv(location=forw(100))
#b = zv(20, ax=(0,0,1),p=2)
#
#arrwidth = 1.5
#arrlen = 1.5
#
#a.add_triedron(width=arrwidth, arrlen=arrlen)
#b.add_triedron(width=arrwidth, arrlen=arrlen)
#
#a.outrot.add_triedron(width=arrwidth, arrlen=arrlen)
#b.outrot.add_triedron(width=arrwidth, arrlen=arrlen)
#
#a.outrot.link(b)
#
#a.outrot.set_coord(deg(60))

arr = pyservoce.draw_arrow(pyservoce.point3(50+10,15,0), pyservoce.vector3(0,100,0), clr=pyservoce.black, width=2, arrlen=4)

scn.viewer.display(arr)

a.location_update(deep=True, view=True)
a.bind_scene_deep(scn)

b.location_update(deep=True, view=True)
b.bind_scene_deep(scn)

c.location_update(deep=True, view=True)
c.bind_scene_deep(scn)

show(scn, view=view)
