#run "nohup python preprocessing/preprocessing_combined.py &" on the server to run the script on the full dataset
# the output will be written to nohup.out at the top level project src_directory 

from music21 import *
import os
import time
import sys
import signal
import pickle

# output_dictionary = []
 
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

src_directory = "preprocessing/src_midis"

def note_array_to_pitch_string(note):
    pitches = ""
    if note != 0:
        if not note.isRest:
            for pitch in range(len(note.pitches)):
                pitches += note.pitches[pitch].nameWithOctave
                pitches += " "
    return pitches

def downsample(parsed_midi_tracks):
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
        piano_notes = piano_stream.flat.notesAndRests
    if len(percussion_tracks) > 0:
        percussion_stream = midi.translate.midiTracksToStreams(percussion_tracks)
        percussion_notes = percussion_stream.flat.notesAndRests
    
    #in theory the normalization and training could be done here
    #or this script could be run to pre-simplify the midi files first

    outStream.append(stream.Part(piano_notes))
    outStream.append(stream.Part(percussion_notes))

    downsampled_midi = midi.translate.streamToMidiFile(outStream)

    # outFile.open('midi_downsampling_step_1/dst_midis/' + filename, "wb")
    # outFile.write()
    # outFile.close()

    downsampled_midi.tracks[0].setChannel(1)
    downsampled_midi.tracks[1].setChannel(10)
    return downsampled_midi

def normalize_prep(downsampled_midi):

    if os.path.exists('preprocessing/notes_dictionary'):
        with open('preprocessing/notes_dictionary', 'rb') as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            output_dictionary = pickle.load(f)
    else:
        print("making new dictionary")
        output_dictionary = []

    downsampled_midi_stream = midi.translate.midiFileToStream(downsampled_midi)
    
    #flat combines all voices(not sure why it wasnt fully flattened before, but had to move on)
    #chordify combines all notes with same offset into a chord for each stream
    piano_stream = downsampled_midi_stream[0].flat.chordify()
    #combine and sychronize the piano and percussion notes and chords together
    #find shortest duration and longest time in each stream to dermine the lowest sample rate
    #which is used to create the synchronized array sizes
    smallest_interval = min([x['durationSeconds'] for x in piano_stream.secondsMap])
    highest_time = piano_stream.highestTime
    if len(downsampled_midi_stream) == 2:
        percussion_stream = downsampled_midi_stream[1].flat.chordify()
        percussion_smallest_interval = min([x['durationSeconds'] for x in percussion_stream.secondsMap])
        smallest_interval = min(smallest_interval,percussion_smallest_interval)
        highest_time = max(highest_time, percussion_stream.highestTime)
    note_array_percussion = [0] * round(highest_time/smallest_interval)
    note_array_piano = [0] * round(highest_time/smallest_interval)
    #put each note or chord into the array based on their offsets
    for i in range(len(piano_stream)):
        note_array_piano[round(piano_stream[i].offset/smallest_interval)] = piano_stream[i]
    if len(downsampled_midi_stream) == 2:
        for i in range(len(percussion_stream)):
            note_array_percussion[round(percussion_stream[i].offset/smallest_interval)] = percussion_stream[i]
    nn_normalized_input = []
    if len(downsampled_midi_stream) == 2:
        for i in range(len(note_array_percussion)):
                #construct the dictionary tuple
                piano_pitches = note_array_to_pitch_string(note_array_piano[i])
                percussion_pitches = note_array_to_pitch_string(note_array_percussion[i])
                if (piano_pitches,percussion_pitches) in output_dictionary:
                    dictionary_index = output_dictionary.index((piano_pitches,percussion_pitches))
                else:
                    output_dictionary.append((piano_pitches,percussion_pitches))
                    dictionary_index = len(output_dictionary) - 1
                
                nn_normalized_input.append(dictionary_index) #turn into float with dictionary index later
    else:
        for i in range(len(note_array_piano)):
            #construct the dictionary tuple
            piano_pitches = note_array_to_pitch_string(note_array_piano[i])
            percussion_pitches = ""
            if (piano_pitches,percussion_pitches) in output_dictionary:
                dictionary_index = output_dictionary.index((piano_pitches,""))
            else:
                output_dictionary.append((piano_pitches,percussion_pitches))
                dictionary_index = len(output_dictionary) - 1
            
            nn_normalized_input.append(dictionary_index) #turn into float with dictionary index later

    with open("preprocessing/notes_dictionary", "wb") as fp:   #Pickling
        pickle.dump(output_dictionary, fp)
    with open("preprocessing/pickled_input_midis/pickled_" + filename, "wb") as fp:   #Pickling
        pickle.dump(nn_normalized_input, fp)

def preprocess(filename):
    filepath = src_directory +"/" + filename

    parsed_midi = midi.MidiFile()
    parsed_midi.open(filepath, "rb")
    parsed_midi.read()
    parsed_midi.close()
    parsed_midi_tracks = parsed_midi.tracks

    piano_tracks = []
    percussion_tracks = []
    #removing single track songs with percussion
    if len(parsed_midi_tracks) == 1 and 10 in parsed_midi_tracks[0].getChannels():
        print("skipping " + str(filename))
    else:
        downsampled_midi = downsample(parsed_midi_tracks)
        nn_normalized_input = normalize_prep(downsampled_midi)

start = time.time()
filenames = os.listdir(src_directory)
total = len(filenames) - 1
count = 0
for filename in filenames:
    if filename.endswith(".mid"):
        count += 1
        sys.stdout.write("\r" + str(count) + "/" + str(total))
        sys.stdout.flush()
        try:
            with Timeout(90):
                preprocess(filename)
        except:
            print("skipping " + str(filename))
        continue
    else:
        continue

end = time.time()
sys.stdout.write("\nDone!\nTime elapsed: " + str(end - start))