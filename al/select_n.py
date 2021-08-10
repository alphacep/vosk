#!/usr/bin/python3
import sys

step = 8
for i, line in enumerate(open(sys.argv[1])):
    if i % 8 == 5:
        print (line.strip())
