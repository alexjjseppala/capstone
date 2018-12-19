from music21 import *

parsed_midi = midi.MidiFile()
parsed_midi.open('midi_downsampling/dst_midis/CherryBlossomGirl.mid', "rb")
parsed_midi.read()
parsed_midi.close()

s = midi.translate.midiFileToStream(parsed_midi)

print(s)