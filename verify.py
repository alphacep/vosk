#!/usr/bin/python3


import sys
import librosa
import numpy
import phash
import pickle

from index import SegmentGenerator, Segment


def verify_data():

    try:
        inf = open(sys.argv[3], "rb")
        database = pickle.load(inf)
    except:
        database = {}

    for mhash, start, end, segments in SegmentGenerator(sys.argv[1], sys.argv[2]):
        if mhash in database:
            target = " ".join([x.name for x in segments])
            source = [" ".join([x.name for x in chunk[0]]) for chunk in database[mhash]]
            if target in source:
                 print ("+", target, source, segments[0].utt, start, end)
            else:
                 print ("-", target, source, segments[0].utt, start, end)

if __name__ == '__main__':
    verify_data()
