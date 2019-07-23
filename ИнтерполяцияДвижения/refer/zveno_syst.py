#!/usr/bin/env python3

from zencad import *
import zencad.assemble
import zencad.cynematic
import pyservoce

scn = Scene()
view = scn.viewer.create_view()

view.set_triedron(True)
view.set_background(pyservoce.white)
scn.viewer.set_triedron_axes(True)

class zv(zencad.assemble.unit):
	def __init__(self, l, ax, p):
		super().__init__()
		self.shape = (
			cylinder(r=3, h=l) + (
			cylinder(r=3, h=6, center=True).rotateX(deg(90)).up(l) if p == 1 else cylinder(r=3, h=6, center=True).rotateX(deg(90))
		))

		self.set_color(0.6,0.6,0.6,0.8)
		self.outrot = zencad.cynematic.rotator(ax=ax, parent=self, location=up(l))

a = zv(20, ax=(0,1,0),p=1)
b = zv(20, ax=(0,0,1),p=2)

arrwidth = 1.5
arrlen = 1.5

a.add_triedron(width=arrwidth, arrlen=arrlen)
b.add_triedron(width=arrwidth, arrlen=arrlen)

a.outrot.add_triedron(width=arrwidth, arrlen=arrlen)
b.outrot.add_triedron(width=arrwidth, arrlen=arrlen)

a.outrot.link(b)

a.outrot.set_coord(deg(60))

a.location_update(deep=True, view=True)
a.bind_scene_deep(scn)

show(scn, view=view)
