from music21 import *
import pickle
import os
import sys


with open('preprocessing/pickled_input_midis/pickled_Een-Roos-Kan-Niet-Zonder-Zonneschijn.mid', "rb") as fp:
    pickled_values = pickle.load(fp)

with open('preprocessing/notes_dictionary', "rb") as fp:
    notes_dictionary = pickle.load(fp)

piano_notes = [tempo.MetronomeMark(number=120)]
percussion_notes = [tempo.MetronomeMark(number=120)]

for i in range(len(pickled_values)):
    # print(notes_dictionary[pickled_values[i]])
    if notes_dictionary[pickled_values[i]][0] == '':
        temp = note.Rest()
        temp.duration.quarterLength = 2.0
        piano_notes.append(temp)
    else:
        temp = chord.Chord(notes_dictionary[pickled_values[i]][0])
        temp.duration.quarterLength = 2.0
        piano_notes.append(temp)    
    if notes_dictionary[pickled_values[i]][1] == '':
        temp = note.Rest()
        temp.duration.quarterLength = 2.0
        percussion_notes.append(temp)
    else:
        temp = chord.Chord(notes_dictionary[pickled_values[i]][1])
        temp.duration.quarterLength = 2.0
        percussion_notes.append(temp)

outStream = stream.Stream()
outStream.append(stream.Part(piano_notes))
outStream.append(stream.Part(percussion_notes))

outFile = midi.translate.streamToMidiFile(outStream)

outFile.tracks[0].setChannel(1)
outFile.tracks[1].setChannel(10)

# print(outFile.tracks[0])
for i in range(len(outStream[0])):
    print(outStream[0][i])

outFile.open('test_file.mid', "wb")
outFile.write()
outFile.close()