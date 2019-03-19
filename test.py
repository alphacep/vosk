#!/usr/bin/python3

d = [[('around_world_in_80_days_24_verne_64kb-0100', 'SIL', 0.0, 0.21),
('around_world_in_80_days_24_verne_64kb-0100', 'DH_B', 0.21, 0.09),
('around_world_in_80_days_24_verne_64kb-0100', 'AH_E', 0.3, 0.03)],
[('master_of_world_06_verne_64kb-0520', 'SIL', 0.0, 0.21),
('master_of_world_06_verne_64kb-0520', 'EH_B', 0.21, 0.12),
('master_of_world_06_verne_64kb-0520', 'V_I', 0.33, 0.09)]]

import sys
import librosa
import numpy
import phash


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import librosa.display

numpy.set_printoptions(threshold=sys.maxsize)

database = {}

def get_hash(utt, start, end):
     y, sr = librosa.load(wavs[utt], sr=16000)
     y = y[int(start * sr):int(end * sr)]
     # Get the hop size so we get about 64 frames
     hop = int(y.shape[0] / 64) + 1
     S = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr, n_mels=32, fmax=8000, n_fft=512, hop_length=hop), ref=numpy.max)
     h = phash.hash(S)
     print (h)
     return h

wavs = {}
for line in open(sys.argv[1]):
    items = line.split()
    wavs[items[0]] = items[1]


plt.subplot(2, 1, 1)
get_hash('around_world_in_80_days_24_verne_64kb-0100', 0.0, 0.51)
plt.subplot(2, 1, 2)
get_hash('master_of_world_06_verne_64kb-0520', 0.0, 0.54)
plt.savefig("test.png")
