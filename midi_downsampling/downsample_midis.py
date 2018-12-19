from music21 import *
import os
import time
import sys

#converts all midi files in the midi_downsampling/src_midis to simpler version (2 tracks, one piano one percussion)
#and stores them into midi_downsampling/dst_midis

directory = "midi_downsampling/src_midis"

def downsample(filename):
    filepath = "midi_downsampling/src_midis/" + filename

    parsed_midi = midi.MidiFile()
    parsed_midi.open(filepath, "rb")
    parsed_midi.read()
    parsed_midi.close()
    parsed_midi_tracks = parsed_midi.tracks

    piano_tracks = []
    percussion_tracks = []
    for track in range(len(parsed_midi_tracks)):
        channels = parsed_midi_tracks[track].getChannels()
        if 10 in channels:
            percussion_tracks.append(parsed_midi_tracks[track])
        else:
            piano_tracks.append(parsed_midi_tracks[track])
    
    outStream = stream.Stream()
    piano_notes = []
    percussion_notes = []
    if len(piano_tracks) > 0:
        piano_stream = midi.translate.midiTracksToStreams(piano_tracks)
        piano_notes = piano_stream.flat.notes
    if len(percussion_tracks) > 0:
        percussion_stream = midi.translate.midiTracksToStreams(percussion_tracks)
        percussion_notes = percussion_stream.flat.notes
    
    #in theory the normalization and training could be done here
    #or this script could be run to pre-simplify the midi files first

    outStream.append(stream.Part(piano_notes))
    outStream.append(stream.Part(percussion_notes))

    outFile = midi.translate.streamToMidiFile(outStream)

    outFile.tracks[0].setChannel(1)
    outFile.tracks[1].setChannel(10)

    outFile.open('midi_downsampling/dst_midis/' + filename, "wb")
    outFile.write()
    outFile.close()

start = time.time()
filenames = os.listdir(directory)
total = len(filenames)
count = 0
for filename in filenames:
    if filename.endswith(".mid"):
        count += 1
        sys.stdout.write("\r" + str(count) + "/" + str(total))
        sys.stdout.flush()
        downsample(filename)
        continue
    else:
        continue
end = time.time()
sys.stdout.write("\nDone!\nTime elapsed: " + str(end - start))