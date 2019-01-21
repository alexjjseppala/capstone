from music21 import *
import pickle
import os
import sys

# with open('preprocessing/pickled_input_midis/pickled_Een-Roos-Kan-Niet-Zonder-Zonneschijn.mid', "rb") as fp:
#     pickled_values = pickle.load(fp)

with open('preprocessing/pickled_ZZs_song.mid', "rb") as fp:
    pickled_values = pickle.load(fp)

with open('preprocessing/notes_dictionary', "rb") as fp:
    notes_dictionary = pickle.load(fp)

# parsed_midi = converter.parse('preprocessing/downsampled_midis_test/Een-Roos-Kan-Niet-Zonder-Zonneschijn.mid')


for i in range(len(pickled_values)):
    print(notes_dictionary[pickled_values[i]])