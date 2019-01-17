#run "nohup python midi_downsampling_step_1/downsample_midis.py &" on the server to run the script on the full dataset
# the output will be written to nohup.out at the top level project directory 

from music21 import *
import os
import time
import sys
import signal
 
def test_request(arg=None):
    """Your http request."""
    time.sleep(2)
    return arg
 
class Timeout():
    """Timeout class using ALARM signal."""
    class Timeout(Exception):
        pass
 
    def __init__(self, sec):
        self.sec = sec
 
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)
 
    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm
 
    def raise_timeout(self, *args):
        raise Timeout.Timeout()

#converts all midi files in the midi_downsampling_step_1/src_midis to simpler version (2 tracks, one piano one percussion)
#and stores them into midi_downsampling_step_1/dst_midis

directory = "midi_downsampling_step_1/src_midis"

def downsample(filename):
    filepath = "midi_downsampling_step_1/src_midis/" + filename

    parsed_midi = midi.MidiFile()
    parsed_midi.open(filepath, "rb")
    parsed_midi.read()
    parsed_midi.close()
    parsed_midi_tracks = parsed_midi.tracks

    piano_tracks = []
    percussion_tracks = []
    #removing single track songs with percussion
    if len(parsed_midi_tracks) == 1 and 10 in parsed_midi_tracks[0].getChannels():
        print("skip!")
    else:
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
            piano_notes = piano_stream.flat.notesAndRests
        if len(percussion_tracks) > 0:
            percussion_stream = midi.translate.midiTracksToStreams(percussion_tracks)
            percussion_notes = percussion_stream.flat.notesAndRests
        
        #in theory the normalization and training could be done here
        #or this script could be run to pre-simplify the midi files first

        outStream.append(stream.Part(piano_notes))
        outStream.append(stream.Part(percussion_notes))

        # outStream[0].chordify()
        # outStream[1].chordify()

        # outStream[0] = outStream[0].flat
        # outStream[1] = outStream[1].flat

        outFile = midi.translate.streamToMidiFile(outStream)

        outFile.tracks[0].setChannel(1)
        outFile.tracks[1].setChannel(10)

        outFile.open('midi_downsampling_step_1/dst_midis/' + filename, "wb")
        outFile.write()
        outFile.close()

start = time.time()
filenames = os.listdir(directory)
total = len(filenames) - 1
count = 0
for filename in filenames:
    if filename.endswith(".mid"):
        count += 1
        sys.stdout.write("\r" + str(count) + "/" + str(total))
        sys.stdout.flush()
        try:
            with Timeout(20):
                downsample(filename)
        except:
            print("skip!")
        continue
    else:
        continue
end = time.time()
sys.stdout.write("\nDone!\nTime elapsed: " + str(end - start))