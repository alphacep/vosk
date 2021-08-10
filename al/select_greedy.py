#!/usr/bin/python3
import sys
import math
from collections import defaultdict

counts = defaultdict(int)

def get_ent(counts, sent_counts, tot):
    ent = 0
    for w in counts:
        if w in sent_counts:
            p = float(counts[w] + sent_counts[w]) / tot
            ent += p * math.log(p)
        else:
            p = float(counts[w]) / tot
            ent += p * math.log(p)
    for w in sent_counts:
        if w not in counts:
            p = float(sent_counts[w]) / tot
            ent += p * math.log(p)

    return -ent

ent = 0
tot = 0
for line in open(sys.argv[1]):
    items = line.split()

    new_tot = tot + len(items) - 1

    sent_counts = defaultdict(int)
    for w in items[1:]:
        sent_counts[w] = sent_counts[w] + 1
    new_ent = get_ent(counts, sent_counts, new_tot)

    if new_ent > ent + 1e-8:
        print (line.strip())
        ent = new_ent
        tot = tot + len(items) - 1
        for w in items[1:]:
            counts[w] = counts[w] + 1
