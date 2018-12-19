from music21 import *
import os

#some nasty overhead, but it seems to work, I'll see how it does when doing a batch job

filename = "CherryBlossomGirl.mid"

# filename = "mz_311_1.mid"

filepath = "midi_downsampling/src_midis/" + filename

# parsed_midi = midi.MidiFile()
# parsed_midi.open(filepath, "rb")
# parsed_midi.read()
# parsed_midi.close()

# parsed_midi_tracks = parsed_midi.tracks

# for track in range(len(parsed_midi_tracks)):
#     if 

midi = converter.parse(filepath)
parts = instrument.partitionByInstrument(midi)
pianoScore = stream.Score()
percScore = stream.Score()
for i in range(4):
    parts[i].insert(0,instrument.Piano())
    pianoScore.append(parts[i])
parts[4].insert(0,instrument.Violin())
percScore.append(parts[4])
pianoScore = pianoScore.flat
finalScore = stream.Score()
finalScore.append(pianoScore)
finalScore.append(percScore)
# for el in parts[4].recurse():
#      if 'Instrument' in el.classes: # or 'Piano'
#          el.activeSite.replace(el, instrument.SteelDrum())

# parts2 = instrument.partitionByInstrument(tempScore)

finalScore.write('midi', fp='midi_downsampling/dst_midis/' + filename)