#!/usr/bin/python3
import sys
import math
from collections import defaultdict

counts = defaultdict(int)

def get_ent(counts, tot):
    ent = 0
    for w in counts:
        p = float(counts[w]) / tot
        ent += p * math.log2(p)

    return -ent

tot = 0
for line in open(sys.argv[1]):
    items = line.split()
    tot = tot + len(items) - 1
    for w in items[1:]:
        counts[w] = counts[w] + 1

print (get_ent(counts, tot))
