#!/usr/bin/python3

import sys
import librosa
import numpy
import phash
import pickle

numpy.set_printoptions(threshold=sys.maxsize)

try:
    inf = open(sys.argv[3], "rb")
    database = pickle.load(inf)
except:
    database = {}

def get_hash(utt, start, end):
     y, sr = librosa.load(wavs[utt], sr=16000)
     y = y[int(start * sr):int(end * sr)]
     # Get the hop size so we get about 50 frames

     hop = int(y.shape[0] / 64) + 1
     S = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr, n_mels=32, fmax=8000, n_fft=512, hop_length=hop), ref=numpy.max)
     h = phash.hash(S)
     return h

wavs = {}
for line in open(sys.argv[1]):
    items = line.split()
    wavs[items[0]] = items[1]

phones={}
for line in open(sys.argv[2]):
    utt, channel, start, dur, pn = line.split()
    if utt not in phones:
        phones[utt] = []
    phones[utt].append((utt, pn, float(start), float(dur)))

for utt in phones:
    utt_phones = phones[utt]
    for i, phone in enumerate(utt_phones):
        _, pn, start, dur = phone
        # End should be approximately + 0.5 seconds from start
        j = i
        end = start
        while end < start + 0.5 and j < len(utt_phones):
             end = end + utt_phones[j][3]
             j = j + 1
        if j - i < 3 or end - start < 0.4: # Ignore this
             continue
        mhash = get_hash(utt, start, end)
        if mhash not in database:
            database[mhash] = []
        database[mhash].append((utt_phones[i:j + 1], start, end))

#for k in database:
#    if len(database[k]) > 1:
#         print (k, database[k])
#         for x in database[k]:
#             print (" ".join([y[1] for y in x[0]]))

pickle.dump(database, open(sys.argv[3], "wb"))
