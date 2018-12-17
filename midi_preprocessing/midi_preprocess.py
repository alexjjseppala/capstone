from music21 import *
import os

directory = "midi_downsampling/dst_midis"

for filename in os.listdir(directory):
    if filename.endswith(".mid"):
        parsed_midi = midi.MidiFile()
        parsed_midi.open('midi_downsampling/dst_midis/' + filename, "rb")
        parsed_midi.read()
        parsed_midi.close()

        # parts = instrument.partitionByInstrument(parsed_midi.tracks)
        # print(parts)

        #this next part is currently reconstructing instead, just to make sure it can be rebuilt properly enough
        piano_stream = midi.translate.midiTrackToStream(parsed_midi.tracks[0]).flat.notesAndRests
        percussion_stream = midi.translate.midiTrackToStream(parsed_midi.tracks[1]).flat.notesAndRests

        outStream = stream.Stream()
        outStream.append(stream.Part(piano_stream))
        outStream.append(stream.Part(percussion_stream))#try to make music21 detect this as a percussion part
        # print("asdf")
        # for piano_element in piano_stream:
        #     print(piano_element)
        # for percussion_element in percussion_stream:
        #     print(percussion_element)

        #writeback test
        outStream.write('midi', fp='test_output.mid')
        print("done")
        
        continue
    else:
        continue
