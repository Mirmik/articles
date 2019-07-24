#!/usr/bin/env python3

import os
import licant

def latex(tgt, tgtname, deps, src):
	licant.makefile(tgt, tgtname=tgtname, deps=deps, src=src, do="pdflatex -jobname={tgtname} {src}")

fls = [
		"src/main.tex",
		"src/introduction.tex",
		"src/ctrobj.tex",
		"src/htrans.tex",
		"src/straight.tex",
		"src/common.tex",
		"src/inverse.tex",
		"src/track.tex",
		"src/lerp.tex",
		"src/restr_coord.tex",
		"src/restr_traj.tex",
		"src/localbase.tex",
		"src/tree.tex",
		"src/findings.tex"
	]

for l in fls : licant.source(l)

latex(src="src/main.tex", tgt="refer.pdf", tgtname="refer",
	deps = fls
)

licant.fileset("all", targets=["refer.pdf"])

licant.ex("all")