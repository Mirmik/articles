#!/usr/bin/env python3

import licant

licant.include("rabbit")
licant.include("nos")
licant.include("igris")

licant.cxx_application("target",
	sources = ["main.cpp"],
	mdepends=["rabbit", "nos", "igris"]
)

licant.ex("target")