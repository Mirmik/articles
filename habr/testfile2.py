#!/usr/bin/python3

import evalcache
import evalcache.lazyfile

lazy = evalcache.lazy.Lazy(cache = evalcache.DirCache(".evalcache"))
lazyfile = evalcache.lazyfile.LazyFile(cache = evalcache.DirCache(".evalcache"))

@lazyfile(field="path")
def foo(data, path):
	f = open(path, "w")
	f.write(data)
	f.close()

@lazy
def datagenerator():
	return "HelloWorld"

foo(datagenerator(),"data.dat")