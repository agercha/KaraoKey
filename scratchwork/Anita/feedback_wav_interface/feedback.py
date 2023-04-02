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