#!/usr/bin/env python3

import os
import licant

def latex(tgt, tgtname, deps, src):
	licant.makefile(tgt, tgtname=tgtname, deps=deps, src=src, do="pdflatex -jobname={tgtname} {src}")

fls = [
		"src/main.tex"
	]

for l in fls : licant.source(l)

latex(src="main.tex", tgt="refer.pdf", tgtname="refer",
	deps = fls
)

@licant.routine
def re():
	licant.do(["refer.pdf", "build"])

licant.ex("refer.pdf")