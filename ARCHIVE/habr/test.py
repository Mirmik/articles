#!/usr/bin/python3

import evalcache

lazy = evalcache.Lazy(cache={}, onuse=True)

@lazy
def fib(n):
	if n < 2:
		return n
	return fib(n - 1) + fib(n - 2)

for i in range(0,100):
	print(fib(i))
