#!/usr/bin/env python3

import licant

licant.make.source("ten-10-7.md")
licant.make.source("chi-6-4.md")
licant.make.source("jin-3-1.md")

def pandoc(src, tgt):
    licant.core.core.add(
        licant.make.FileTarget(
            tgt=tgt,
            src=src,
            deps=[src],
            build=licant.make.Executor("pandoc {src} -o {tgt}"),
        )
    )

pandoc("ten-10-7.md", "ten-10-7.docx")
pandoc("chi-6-4.md", "chi-6-4.docx")
pandoc("jin-3-1.md", "jin-3-1.docx")

licant.fileset("all", ["ten-10-7.docx", "chi-6-4.docx", "jin-3-1.docx"])
licant.ex("all")