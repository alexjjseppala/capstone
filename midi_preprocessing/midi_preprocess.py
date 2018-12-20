from music21 import *
import os

directory = "midi_downsampling/dst_midis"

for filename in os.listdir(directory):
    if filename.endswith(".mid"):
        parsed_midi = converter.parse('midi_downsampling/dst_midis/' + filename)

        #flat combines all voices(not sure why it wasnt fully flattened before, but had to move on)
        #chordify combines all notes with same offset into a chord for each stream
        #Note: appears that rests were dropped, should be fine since we have the offsets
        piano_stream = parsed_midi[0].flat.chordify()

        percussion_stream = parsed_midi[1].flat.chordify()

        #NEXT STEP
        # combine the piano stream and the percussion streams together
        # and ensure that they sync up, this could use a design discussion regarding the format of the array

        # Test printing
        for i in range(len(piano_stream)):
            print(piano_stream[i].offset)
            print(piano_stream[i])
        print("________________________________________________________________________________________________________________________________________________")
        for i in range(len(percussion_stream)):
            print(percussion_stream[i].offset)
            print(percussion_stream[i])
        print("tst")
        continue
    else:
        continue
