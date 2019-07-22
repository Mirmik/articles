#!/usr/bin/env python3

import os
import licant

def latex(tgt, tgtname, deps, src):
	licant.makefile(tgt, tgtname=tgtname, deps=deps, src=src, do="pdflatex -jobname={tgtname} {src}")

licant.source("src/main.tex")

latex(src="src/main.tex", tgt="refer.pdf", tgtname="refer",
	deps = [
		"src/main.tex"
])

licant.fileset("all", targets=["refer.pdf"])

licant.ex("all")