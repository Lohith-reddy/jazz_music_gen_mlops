import yaml
import pickle
import numpy
import os
from music21 import converter, instrument, note, chord
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import BatchNormalization as BatchNorm
#from tensorflow.keras.utils import np_utils
from tensorflow.python.keras import utils
from tensorflow.keras.callbacks import ModelCheckpoint
import sys


def read_pickle_file(file_path):
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        return data

def create_network(network_input, n_vocab,loss= "categorical_crossentropy",optimizer= "rmsprop"):
    """ create the structure of the neural network """
    model = Sequential()
    model.add(LSTM(
        512,
        input_shape=(network_input.shape[1], network_input.shape[2]),
        recurrent_dropout=0.3,
        return_sequences=True
    ))
    model.add(LSTM(512, return_sequences=True, recurrent_dropout=0.3,))
    model.add(LSTM(512))
    model.add(BatchNorm())
    model.add(Dropout(0.3))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(BatchNorm())
    model.add(Dropout(0.3))
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))
    model.compile(loss=loss, optimizer=optimizer)

    return model



def train(model, network_input, network_output, epochs=200, batch_size=128, validation_split=0.2):
    """ train the neural network """
    filepath = "artifacts/weights-improvement-{epoch:02d}-{loss:.4f}-bigger.h5"
    checkpoint = ModelCheckpoint(
        filepath,
        monitor='loss',
        verbose=0,
        save_best_only=True,
        mode='min'
    )
    callbacks_list = [checkpoint]

    # Split the data into training and validation sets
    network_input_train, network_input_val, network_output_train, network_output_val = train_test_split(network_input, network_output, test_size=validation_split)

    # Include validation_data in the fit method
    model.fit(network_input_train, network_output_train, epochs=epochs, batch_size=batch_size, callbacks=callbacks_list, validation_data=(network_input_val, network_output_val))
if __name__ == '__main__':

    if not os.path.exists('artifacts'):
        os.makedirs('artifacts')
    args = sys.argv[1:]    

    with open('config.yaml', 'r') as config_file:
            config = yaml.safe_load(config_file)

    loss = config['model_loss_function']
    optimizer = config['model_optimizer']
    epochs = config['epochs'] 
    batch_size = config['batch_size']   
    n_vocab = read_pickle_file('processed/n_vocab.pickle')
    network_input = numpy.load('processed/network_input.npy')
    network_output = numpy.load('processed/network_output.npy')

    model = create_network(network_input, n_vocab, loss, optimizer)

    train(model, network_input, network_output, epochs, batch_size)