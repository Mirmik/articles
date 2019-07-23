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

class zzz(zencad.assemble.unit):
	def __init__(self):
		super().__init__()
		self.shape = (box(20,5,5,center=True)).rotateZ(deg(90))
		self.add_triedron(arrlen=1, width=1)
		self.xaxis.set_color(pyservoce.black)
		self.yaxis.set_color(pyservoce.black)
		self.zaxis.set_color(pyservoce.black)
		self.set_color(0.6,0.6,0.6,0.7)

a = zzz()
b = zzz()
c = zzz()
d = zzz()

b.relocate(translate(0,10,10) * rotateX(-deg(20)))
c.relocate(translate(0,20,20) * rotateX(-deg(40)))
d.relocate(translate(0,30,30) * rotateX(-deg(60)))

arr = pyservoce.draw_arrow(pyservoce.point3(0,0,0), pyservoce.vector3(0,7,7), pyservoce.black, width=2, arrlen=2)
arr2 = pyservoce.draw_arrow(pyservoce.point3(0,0,0), pyservoce.vector3(10,0,0), pyservoce.black, width=2, arrlen=2)
arr21 = pyservoce.draw_arrow(pyservoce.point3(0,0,0), pyservoce.vector3(0,30,30), pyservoce.black, width=2, arrlen=2)
arr22 = pyservoce.draw_arrow(pyservoce.point3(0,30,30), pyservoce.vector3(20,0,0), pyservoce.black, width=2, arrlen=2)
dashdot = pyservoce.draw_line(pyservoce.point3(0,0,0), pyservoce.point3(0,40,40), pyservoce.black, width=1.5, style=pyservoce.dotdash_line)

scn.viewer.display(arr)
scn.viewer.display(arr2)
scn.viewer.display(arr21)
scn.viewer.display(arr22)
scn.viewer.display(dashdot)

a.bind_scene(scn)
b.bind_scene(scn)
c.bind_scene(scn)
d.bind_scene(scn)

show(scn, view=view)