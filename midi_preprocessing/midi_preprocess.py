from music21 import *
import os
import numpy as np

directory = "midi_downsampling/dst_midis"

for filename in os.listdir(directory):
    if filename.endswith(".mid"):
        parsed_midi = converter.parse('midi_downsampling/dst_midis/' + filename)

        #flat combines all voices(not sure why it wasnt fully flattened before, but had to move on)
        #chordify combines all notes with same offset into a chord for each stream
        piano_stream = parsed_midi[0].flat.chordify()

        percussion_stream = parsed_midi[1].flat.chordify()

        #combine and sychronize the piano and percussion notes and chords together

        #find shortest duration and longest time in each stream to dermine the lowest sample rate
        #which is used to create the synchronized array sizes
        piano_smallest_interval = min([x['durationSeconds'] for x in piano_stream.secondsMap])
        percussion_smallest_interval = min([x['durationSeconds'] for x in percussion_stream.secondsMap])
        smallest_interval = min(piano_smallest_interval,percussion_smallest_interval)

        highest_time = max(piano_stream.highestTime, percussion_stream.highestTime)

        note_array_percussion = [0] * round(highest_time/smallest_interval)
        note_array_piano = [0] * round(highest_time/smallest_interval)

        #put each note or chord into the array based on their offsets
        for i in range(len(piano_stream)):
            note_array_piano[round(piano_stream[i].offset/smallest_interval)] = piano_stream[i]
        for i in range(len(percussion_stream)):
            note_array_percussion[round(percussion_stream[i].offset/smallest_interval)] = percussion_stream[i]
        
        #printing for testing
        #they seem to sync up!
        # for i in range(len(note_array_percussion)):
        #     print(str(note_array_piano[i]) + "|" + str(note_array_percussion[i]) + "\n")

        #insert normalizing code here using the notes and found in the chosen downsampled dataset
        continue
    else:
        continue
