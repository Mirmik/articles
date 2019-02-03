#!/usr/bin/python3

import evalcache
import evalcache.lazyfile

lazyfile = evalcache.lazyfile.LazyFile()

@lazyfile(field="path")
def foo(data, path):
	f = open(path, "w")
	f.write(data)
	f.close()

foo("HelloWorld","data.dat")