from mido import MidiFile, MidiTrack, Message, merge_tracks
from music21 import *

filename = "Beguine-Again.mid"
# filename = "CherryBlossomGirl.mid"

parsed_midi = midi.MidiFile()
parsed_midi.open(filename, "rb")
parsed_midi.read()
parsed_midi.close()
parsed_midi_tracks = parsed_midi.tracks
#get channels for each track to find where the percussion track is (channel 10 music21 channel 9 mido)
percussion_track_indexes = []
for track in range(len(parsed_midi_tracks)):
    channels = parsed_midi_tracks[track].getChannels()
    if(10 in channels):
        percussion_track_indexes.append(track)

mid = MidiFile(filename)

other_tracks = []
percussion_tracks = []

for track in range(len(mid.tracks)):
    if track in percussion_track_indexes:
        percussion_tracks.append(mid.tracks[track])
    else:
        other_tracks.append(mid.tracks[track])

    
# one_track = merge_tracks(mid.tracks)
percussion_track = merge_tracks(percussion_tracks)
other_track = merge_tracks(other_tracks)

percussion_track = MidiTrack([msg for msg in percussion_track if msg.type == "note_on" or msg.type == "note_off"])
other_track = MidiTrack([msg for msg in other_track if msg.type == "note_on" or msg.type == "note_off"])
 
out_mid = MidiFile()
out_mid.tracks = [other_track,percussion_track]

#output to temp midi file
out_mid.save('only_notes.mid')



