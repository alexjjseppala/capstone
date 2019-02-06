from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation
from keras.utils import np_utils
from keras import backend
from keras.callbacks import ModelCheckpoint
import pickle
import numpy
import os

# Get song ints
def getSongInts(directory):
    with open(directory + "/" + "pickled_ZZs_song.mid", "rb") as fp:
        songIntList = pickle.load(fp)
    return songIntList


# Get Sequence
def getSequencesFromFile(fileToExtractSeqences, seqLength, directory):
    sequences = []
    sequenceOutput = []
    with open(directory + "/" + fileToExtractSeqences, "rb") as fp:
        songIntList = pickle.load(fp)
        for i in range(0, len(songIntList) - 100 ):
            sequenceOutput.append(songIntList[i + seqLength])
            sequences.append(songIntList[i:i + seqLength])
    return sequences, sequenceOutput


def testSequenceAccuracy(sequencesToTest, directory):
    
    songInts = getSongInts(directory)
    start = 0
    stop = 100
    for sequence in sequencesToTest:
        print(sequence[0] == songInts[start:stop])
        start += 1
        stop += 1

def buildNetwork(network_input, n_vocab):
    """ create the structure of the neural network """
    model = Sequential()
    model.add(LSTM(
        512,
        input_shape=(network_input.shape[1], network_input.shape[2]),
        return_sequences=True
    ))
    model.add(Dropout(0.3))
    model.add(LSTM(512, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(512))
    model.add(Dense(256))
    model.add(Dropout(0.3))
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='rmsprop')

    return model

def train(model, network_input, network_output):
    """ train the neural network """
    filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
    checkpoint = ModelCheckpoint(
        filepath,
        monitor='loss',
        verbose=0,
        save_best_only=True,
        mode='min'
    )
    callbacks_list = [checkpoint]

    model.fit(network_input, network_output, epochs=200, batch_size=64, callbacks=callbacks_list)

sequenceLength = 100
sequenceList = []
sequenceOutputList = []
midiDir = "C:/Users/a-sho/Documents/AQueensWork/4thyear/ELEC498/code/PickledMidis"

for filename in os.listdir(midiDir):
    if filename.endswith(".mid"):
        newSequences, newOutputs = getSequencesFromFile(filename, sequenceLength, midiDir)
        for seq in newSequences:
            sequenceList.append(seq)
        for out in newOutputs:
            sequenceOutputList.append(out)
            
sequenceList = numpy.reshape(sequenceList, (len(sequenceList), sequenceLength, 1))
#sequenceOutputList = sequenceOutputList[0:(int(len(sequenceOutputList)/4))]
#sequenceOutputList = backend.sparse_categorical_crossentropy(sequenceOutputList)

with open('notes_dictionary', "rb") as fp:
    notesDictionary = pickle.load(fp)
    notesLength = len(set(notesDictionary))

model = buildNetwork(sequenceList, notesLength)

train(model, sequenceList, sequenceOutputList)


print("")

        
 
        
