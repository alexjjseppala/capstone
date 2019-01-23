import os
import pickle
from shutil import copyfile

#go through clean_pickled_midis

filenames = os.listdir('preprocessing/clean_pickled_midis')
for filename in filenames:
    if filename.endswith(".mid") and filename.startswith("pickled_"):
        #MOVE found midis from src_midis to used_src_midis
        os.rename("preprocessing/src_midis/" + str(filename[8:]), "preprocessing/used_src_midis/" + str(filename[8:]))