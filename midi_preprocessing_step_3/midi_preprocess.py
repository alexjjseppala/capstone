from music21 import *
import os
import sys
import time
import numpy as np
import pickle

directory = "midi_downsampling_step_1/dst_midis"

start = time.time()
filenames = os.listdir(directory)
total = len(filenames) - 1
count = 0
for filename in filenames:
    sys.stdout.write("\r" + str(count) + "/" + str(total))
    count += 1
    sys.stdout.flush()
    if filename.endswith(".mid"):
        parsed_midi = converter.parse('midi_downsampling_step_1/dst_midis/' + filename)

        #flat combines all voices(not sure why it wasnt fully flattened before, but had to move on)
        #chordify combines all notes with same offset into a chord for each stream
        piano_stream = parsed_midi[0].flat.chordify()

        percussion_stream = parsed_midi[1].flat.chordify()

        #combine and sychronize the piano and percussion notes and chords together

        #find shortest duration and longest time in each stream to dermine the lowest sample rate
        #which is used to create the synchronized array sizes
        piano_smallest_interval = min([x['durationSeconds'] for x in piano_stream.secondsMap])
        percussion_smallest_interval = min([x['durationSeconds'] for x in percussion_stream.secondsMap])
        smallest_interval = min(piano_smallest_interval,percussion_smallest_interval)

        highest_time = max(piano_stream.highestTime, percussion_stream.highestTime)

        note_array_percussion = [0] * round(highest_time/smallest_interval)
        note_array_piano = [0] * round(highest_time/smallest_interval)

        #put each note or chord into the array based on their offsets
        for i in range(len(piano_stream)):
            note_array_piano[round(piano_stream[i].offset/smallest_interval)] = piano_stream[i]
        for i in range(len(percussion_stream)):
            note_array_percussion[round(percussion_stream[i].offset/smallest_interval)] = percussion_stream[i]

        with open(r"make_notes_dictionary_step_2/notes_dictionary", "rb") as input_file:
            notes_dictionary = pickle.load(input_file)

        nn_normalized_input = []

        for i in range(len(note_array_percussion)):
            piano_pitches = ""
            if not note_array_piano[i] == 0 and not note_array_piano[i].isRest:
                for pitch in range(len(note_array_piano[i].pitches)):
                    piano_pitches += note_array_piano[i].pitches[pitch].nameWithOctave
                    piano_pitches += " "
            percussion_pitches = ""
            if not note_array_percussion[i] == 0 and not note_array_percussion[i].isRest:
                for pitch in range(len(note_array_percussion[i].pitches)):
                    percussion_pitches += note_array_percussion[i].pitches[pitch].nameWithOctave
                    percussion_pitches += " "
            nn_normalized_input.append(notes_dictionary.index((piano_pitches,percussion_pitches)) / float(len(notes_dictionary)))
        
        with open("make_notes_dictionary_step_3/pickled_input_midis/pickled" + filename, "wb") as fp:   #Pickling
            pickle.dump(nn_normalized_input, fp)
        #printing for testing
        # for i in range(len(note_array_percussion)):
        #     print(str(note_array_piano[i]) + " " + str(note_array_percussion[i]) + " = " + str(nn_normalized_input[i]) + " = " + str(notes_dictionary[int(nn_normalized_input[i] * len(notes_dictionary))]) + "\n")
            # if note_array_piano[i] != 0:
            #     print()
        #insert normalizing code here using the notes found in the chosen downsampled dataset



        continue
    else:
        continue

end = time.time()
sys.stdout.write("\nDone!\nTime elapsed: " + str(end - start))