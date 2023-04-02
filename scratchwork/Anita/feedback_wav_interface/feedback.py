'''
feedback.py (anitama)

This file contains the code for generating feedback based on the user's 
input vocals for the web app, KaraoKey.
'''

import numpy as np

# Constants
NOTE_NAMES = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
A4_FREQ = 440.0
SEMITONES_PER_OCTAVE = 12

NOTE_WEIGHTING = 70
CENT_WEIGHTING = 100 - NOTE_WEIGHTING

def frequency_to_note_data(frequency):
    # equations from https://newt.phys.unsw.edu.au/jw/notes.html#:~:text=In%20equal%20temperament%2C%20where%20all%20note_num%20have%20the,then%20f%20n%20%3D%202%20n%2F12%20%2A440%20Hz.

    # get the number of semitones between the input freq and A4
    distance = 12 * np.log2(frequency / A4_FREQ)

    # get the nearest note's name and octave number
    note_index = int(round(distance)) % SEMITONES_PER_OCTAVE
    note_name = NOTE_NAMES[note_index]
    octave_num = int(4 + np.floor((round(distance) + 9) / 12))

    # get deviation in cents from the nearest note
    cents_deviation = 100 * ((distance - note_index) % 1)
    
    return (note_name, octave_num, cents_deviation)

def get_accuracy_score(input_freq:float, target_freq:float):
    input_note, input_octave, input_cents_deviation = frequency_to_note_data(input_freq)
    target_note, target_octave, target_cents_deviation = frequency_to_note_data(target_freq)
    
    # calcuate note accuracy
    note_accuracy = 0
    if (input_note == target_note):
        # we sang exactly the right note
        note_accuracy = NOTE_WEIGHTING
    else:
        # we didn't sing exactly the right note, let's find how far off they were
        input_note_index = NOTE_NAMES.index(input_note)
        target_note_index = NOTE_NAMES.index(target_note)
        deviation = abs(input_note_index - target_note_index)
        if (deviation == 1 or deviation == 11):
            # we were a half step off
            note_accuracy = NOTE_WEIGHTING / 2
         
    
    cents_accuracy = 30 * (1-(abs(input_cents_deviation - target_cents_deviation) / 100)) if note_accuracy else 0
    accuracy_score = note_accuracy + cents_accuracy

    print(f"Singer's Note: {input_note}{input_octave}, Deviation: {input_cents_deviation} cents")
    print(f"Target Note: {target_note}{target_octave}, Deviation: {target_cents_deviation} cents")
    print(f"Note Accuracy: {note_accuracy}, Cents Accuracy: {cents_accuracy}")
    print(f"\nThe singer's accuracy_score is: {accuracy_score:.2f}%\n")
    
    return accuracy_score

def test_frequency_to_note_data():
    print("Testing frequency_to_note_data...", end="")
    note_to_freq_data = '''\
C 16.35 32.70 65.41 130.81 261.63 523.25 1046.50 2093.00 4186.01
C#/Db 17.32 34.65 69.30 138.59 277.18 554.37 1108.73 2217.46 4434.92
D 18.35 36.71 73.42 146.83 293.66 587.33 1174.66 2349.32 4698.63
D#/Eb 19.45 38.89 77.78 155.56 311.13 622.25 1244.51 2489.02 4978.03
E 20.60 41.20 82.41 164.81 329.63 659.25 1318.51 2637.02 5274.04
F 21.83 43.65 87.31 174.61 349.23 698.46 1396.91 2793.83 5587.65
F#/Gb 23.12 46.25 92.50 185.00 369.99 739.99 1479.98 2959.96 5919.91
G 24.50 49.00 98.00 196.00 392.00 783.99 1567.98 3135.96 6271.93
G#/Ab 25.96 51.91 103.83 207.65 415.30 830.61 1661.22 3322.44 6644.88
A 27.50 55.00 110.00 220.00 440.00 880.00 1760.00 3520.00 7040.00
A#/Bb 29.14 58.27 116.54 233.08 466.16 932.33 1864.66 3729.31 7458.62
B 30.87 61.74 123.47 246.94 493.88 987.77 1975.53 3951.07 7902.13
'''
    for line in note_to_freq_data.splitlines():
        expected_note = line.split()[0]
        for freq in line.split()[1:]:
            output_note, _, _ = frequency_to_note_data(float(freq))
            # Use membership check for C#/Db case.
            if (output_note not in expected_note):
                print(f'[{freq} Hz]: expected-{expected_note}, output-{output_note}')
                assert(False)
    
    print("Passed!")