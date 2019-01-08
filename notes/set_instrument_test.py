from music21 import *
import os

#some nasty overhead, but it seems to work, I'll see how it does when doing a batch job

filename = "CherryBlossomGirl.mid"

# filename = "mz_311_1.mid"

filepath = "midi_downsampling/src_midis/" + filename

parsed_midi = midi.MidiFile()
parsed_midi.open(filepath, "rb")
parsed_midi.read()
parsed_midi.close()

parsed_midi_tracks = parsed_midi.tracks

percussion_tracks_stream = stream.Score()
piano_tracks_stream = stream.Score()

#for each track
for track in range(len(parsed_midi_tracks)):
    #translate track to stream part
    track_stream = midi.translate.midiTrackToStream(parsed_midi_tracks[track])
    #if channel 10 is included in track
    if 10 in parsed_midi_tracks[track].getChannels():
        #add percussion instrument to track
        track_stream.insert(0, instrument.Percussion())
        #add to percussion_tracks_stream
        percussion_tracks_stream.append(stream.Part(track_stream))
    # else
    else:
        #add piano instrument to stream
        track_stream.insert(0, instrument.Piano())
        #add to piano_tracks_stream
        piano_tracks_stream.append(stream.Part(track_stream))
#flatten each stream
percussion_tracks_stream = percussion_tracks_stream.flat
piano_tracks_stream = piano_tracks_stream.flat

#output file
outStream = stream.Score()
outStream.append(stream.Part(piano_tracks_stream))
outStream.append(stream.Part(percussion_tracks_stream))
outStream.write('midi', fp='midi_downsampling/dst_midis/' + filename)


#     for track in range(len(parsed_midi_tracks)):
#         channels = parsed_midi_tracks[track].getChannels()
#         if(10 in channels):
#             percussion_track_indexes.append(track)

# s=converter.parse(filepath)
# for p in s.parts:
#     p.insert(0, instrument.Piano())

