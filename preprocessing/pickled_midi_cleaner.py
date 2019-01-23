import os
import pickle
from shutil import copyfile

with open('preprocessing/notes_dictionary', 'rb') as f:
    output_dictionary = pickle.load(f)

dictionary_max = len(output_dictionary) - 1

filenames = os.listdir('preprocessing/pickled_input_midis')
for filename in filenames:
    if filename.endswith(".mid"):
        with open('preprocessing/pickled_input_midis/' + filename, "rb") as fp:
            pickled_values = pickle.load(fp)
        file_is_good = True
        index = 0
        while file_is_good and index != len(pickled_values):
            if pickled_values[index] > dictionary_max:
                file_is_good = False
            index += 1
        if file_is_good:
            copyfile('preprocessing/pickled_input_midis/' + filename, 'preprocessing/clean_pickled_midis/' + filename)
