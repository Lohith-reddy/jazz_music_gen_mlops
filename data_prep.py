import glob
import pickle
import numpy
from music21 import converter, instrument, note, chord
from tensorflow.keras.utils import np_utils
import os
import yaml


def get_notes():
    """ Get all the notes and chords from the midi files """
    notes = []

    for file in os.listdir('midi_data'):
        midi = converter.parse(file)

        print("Parsing %s" % file)

        notes_to_parse = None

        try: # file has instrument parts
            s2 = instrument.partitionByInstrument(midi)
            notes_to_parse = s2.parts[0].recurse() 
        except: # file has notes in a flat structure
            notes_to_parse = midi.flat.notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

    with open('processed/notes', 'wb') as filepath:
        pickle.dump(notes, filepath)    # we want to cache the notes to fetch them during inference

    return notes

def prepare_sequences(notes, n_vocab, sequence_length):
    """ Prepare the sequences used by the Neural Network """
    sequence_length = sequence_length

    # get all pitch names
    pitchnames = sorted(set(item for item in notes))

     # create a dictionary to map pitches to integers
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))

    network_input = []
    network_output = []

    # create input sequences and the corresponding outputs
    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append(note_to_int[sequence_out])

    n_patterns = len(network_input)

    # reshape the input into a format compatible with LSTM layers
    network_input = numpy.reshape(network_input, (n_patterns, sequence_length, 1))
    # normalize input
    network_input = network_input / float(n_vocab)

    network_output = np_utils.to_categorical(network_output)

    return (network_input, network_output)

def save_files(n_vocab, network_input, network_output):
    # save the input and output files
    if not os.path.exists('processed'):
        os.makedirs('processed')

    numpy.save('processed/network_input.npy', network_input)
    numpy.save('processed/network_output.npy', network_output)

    # save the n_vocab file
    with open('processed/n_vocab', 'wb') as filepath:
        pickle.dump(n_vocab, filepath)

if __name__ == '__main__':

    
    with open('config.yaml', 'r') as config_file:
            config = yaml.safe_load(config_file)

    sequence_length = config['sequence_length']

    notes = get_notes()
    # get amount of pitch names
    n_vocab = len(set(notes))

    network_input, network_output = prepare_sequences(notes, n_vocab,sequence_length)

    save_files(n_vocab, network_input, network_output) 
    

    

    

