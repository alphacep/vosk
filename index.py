#!/usr/bin/python3

import sys
import librosa
import numpy
import phash
import pickle


def get_hash(wavfn, start, end):
     y, sr = librosa.load(wavfn, sr=16000)
     y = y[int(start * sr):int(end * sr)]
     # Get the hop size so we get about 50 frames

     hop = int(y.shape[0] / 64) + 1
     S = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr, n_mels=32, fmax=8000, n_fft=512, hop_length=hop), ref=numpy.max)
     h = phash.hash(S)
     return h

class Segment():
    def __init__(self, utt, start, dur, name):
        self.utt = utt
        self.start = float(start)
        self.dur = float(dur)
        self.name = name

    def __repr__(self):
        return "[%s %s %.3f %.3f]" % (self.utt, self.name, self.start, self.dur)

def SegmentGenerator(wav_list, phone_list):
    wavs = {}
    for line in open(wav_list):
        items = line.split()
        wavs[items[0]] = items[1]

    segments={}
    for line in open(phone_list):
        utt, channel, start, dur, pn = line.split()
        if utt not in segments:
            segments[utt] = []
        segments[utt].append(Segment(utt, start, dur, pn))

    for utt in segments:
        utt_segments = segments[utt]
        for i, phone in enumerate(utt_segments):
            # End should be approximately + 0.5 seconds from start
            j = i
            start = phone.start
            end = phone.start
            while end < start + 0.5 and j < len(utt_segments):
                end = end + utt_segments[j].dur
                j = j + 1
            if j - i < 3 or end - start < 0.4: # Ignore this
                continue

            mhash = get_hash(wavs[utt], start, end)
            yield (mhash, start, end, utt_segments[i:j + 1])


def index_data():
    try:
        inf = open(sys.argv[3], "rb")
        database = pickle.load(inf)
    except:
        database = {}

    for mhash, start, end, segments in SegmentGenerator(sys.argv[1], sys.argv[2]):
        if mhash not in database:
            database[mhash] = []
#        print (mhash, start, end, segments)
        database[mhash].append((segments, start, end))
    pickle.dump(database, open(sys.argv[3], "wb"))

if __name__ == '__main__':
    index_data()
