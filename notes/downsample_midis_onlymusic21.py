from mido import MidiFile, MidiTrack, Message, merge_tracks
from music21 import *
import os

#some nasty overhead, but it seems to work, I'll see how it does when doing a batch job

directory = "midi_downsampling/src_midis"

def downsample(filename):
    filepath = 'midi_downsampling/src_midis/' + filename

    parsed_midi = midi.MidiFile()
    parsed_midi.open(filepath, "rb")
    parsed_midi.read()
    parsed_midi.close()
    parsed_midi_tracks = parsed_midi.tracks
    #get channels for each track to find where the percussion track is (channel 10 music21 channel 9 mido)
    
    # parsed_midi = converter.parse(filepath)

    # stream = instrument.partitionByInstrument(parsed_midi)
    
    percussion_track_indexes = []
    for track in range(len(parsed_midi_tracks)):
        channels = parsed_midi_tracks[track].getChannels()
        if(10 in channels):
            percussion_track_indexes.append(track)

    pianoStream = stream.Stream()
    percussionStream = stream.Stream()
    for track in range(len(parsed_midi_tracks)):
        if track in percussion_track_indexes:
            parsed_midi_tracks[track].setChannel(10)
            percussionStream.append(stream.Part(midi.translate.midiTrackToStream(parsed_midi_tracks[track])))
        else:
            parsed_midi_tracks[track].setChannel(1)
            pianoStream.append(stream.Part(midi.translate.midiTrackToStream(parsed_midi_tracks[track])))
    
    pianoStream = pianoStream.flat
    percussionStream = percussionStream.flat

    pianoStream.append(instrument.Piano())
    # # pianoStream.insert(0,instrument.Piano())
    percussionStream.insert(0,instrument.Percussion())

    # #convert pianoStream instruments to piano
    
    # #convert percussionStream instruments to percussion

    outStream = stream.Stream()
    outStream.append(stream.Part(pianoStream))
    outStream.append(stream.Part(percussionStream))
    outStream.write('midi', fp='midi_downsampling/dst_midis/' + filename)

    print("test")

for filename in os.listdir(directory):
    if filename.endswith(".mid"):
        downsample(filename)
        continue
    else:
        continue



