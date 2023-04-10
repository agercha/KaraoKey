################################################################################
# feedback.py
#
# This file contains the code for generating the instantaeious feedback based 
# on the user's input vocals for the web app, KaraoKey.
#
# For post song feedback, look to post_song_feedback.py
# 
# Test functions can be found in feedback_tests.py
################################################################################

import numpy as np
import json, os

# Constants
NOTE_NAMES = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
A4_FREQ = 440.0
SEMITONES_PER_OCTAVE = 12

NOTE_WEIGHTING = 70
CENT_WEIGHTING = 100 - NOTE_WEIGHTING

def frequency_to_note_data(frequency):
    '''
    Given an input frequency, calculates the note, octave, and deviation in
    cents. This is absolute note detection, instead of relative note detection.

    Parameters:
        frequency: the frequency in Hz that we'd like to get the note data from.
    Return value:
        Tuple: (note_name, octave_num, cents_deviation)
        note_name: the canonical name of the nearest note to the input\
                   frequency, ranging from A to G#.
        octave_num: the octave in which the user sang at.
        cents_deviation: the deviation in cents from the nearest note to the \
                         input frequency.  
    '''

    if (frequency == 0): return (-1, -1, -1)    # we cannot parse zero freqs
    
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
    '''
    Given an input frequency and a target frequency to hit, calculates an 
    accuracy score based on how close the input frequency was to the target
    frequency.

    This function is used for instantaneous feedback generation. 

    Parameters:
        input_freq: the frequency in Hz that the user sang at. Input freq comes\
                    from the pitch detection algorithm.
        target_freq: the target frequency in Hz that the user is aiming to sing\
                     at. Target frequency also comes from the PDA.

    Return value:
        Score ranging from [0, 1] reflecting how close the input frequency was
        to the target frequency.
    '''

    if (input_freq == 0 or target_freq == 0):
        print(f'Zero input: input_freq={input_freq}, target_freq={target_freq}')
        return input_freq == target_freq

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
            note_accuracy = NOTE_WEIGHTING * 0.7
         
    cents_accuracy = 30 * (1-(abs(input_cents_deviation - target_cents_deviation) / 100)) if note_accuracy else 0
    accuracy_score = note_accuracy + cents_accuracy

    user_feedback_str = f"usr: {input_note}{input_octave} ({input_cents_deviation:.2f})".ljust(16)
    tgt_feedback_str = f"tgt: {target_note}{target_octave} ({target_cents_deviation:.2f})".ljust(18)
    print(f'{user_feedback_str} {tgt_feedback_str}', end="")
    print(f"note accuracy: {note_accuracy}, cents accuracy: {cents_accuracy}, score={accuracy_score:.2f}%")
    return accuracy_score

def json_post_frequency_feedback(input_json_filepath:str):
    '''
    Given an input json file containing 1:1 mappings of user and target\
    frequencies, calculates an accuracy score. 

    Parameters:
        input_json_file: a 1:1 mapping of user to target freqeuencies. Expects
        a format of:
            [{
                "length": int
                "target": [array, of, floats]
                "user": [array, of, floats]
                "lyrics" : "string"
            }]
        
    Return value:
        A comprehensive score ranging from [0, 1] reflecting how accurately the 
        user was singing to the target frequency.
    '''

    # this will probably need to be modified once we actually have the actual
    # file directory.
    with open(input_json_filepath) as f:
        test_data = json.load(f)
    
    total_scores = []
    num_outer_chunks = len(test_data)
    # loop over all the partitions of the song
    for outer_index in range(num_outer_chunks):
        outer_chunk = test_data[outer_index]
        # num_inner_chunks = outer_chunk["length"]

        # obtain list of target and user frequencies
        target_freqs = outer_chunk["target"]
        user_freqs = outer_chunk["user"]

        # loop over all the inner frequencies contained in each outer chunk
        for inner_index in range(len(user_freqs)):
            target_freq = target_freqs[inner_index]
            user_freq = user_freqs[inner_index]
            score = get_accuracy_score(target_freq, user_freq)
            if (score != 0): total_scores.append(score) # hmmmm...

    print(sum(total_scores) / len(total_scores))
    return sum(total_scores) / len(total_scores)


def get_progression(scores):
    '''
    Given an input list of scores, returns a value in [-1, 0, +1] representing 
    how the user is progressing through the song

    Parameters:
        scores: an array of floats representing scores. This information should
                be generated by the instantenous feedback mechanism.
    Return value:
        A number in [-1, 0, +1]. 
        -1 represents the user's performance is getting worse. 
        0 represents the user's performance is holding steady
        +1 represents the user's performance is improving.
    '''
    COMP_LENGTH = 15 # COMP_LENGTH determines how volatile the progression score will
                 # swing around. 
    RECENT_SCORES_LENGTH = COMP_LENGTH//2 

    if len(scores) < COMP_LENGTH:
        return 0

    comparison_scores = scores[-COMP_LENGTH:]
    score_average = sum(scores)/len(scores)

    recent_scores = scores[-RECENT_SCORES_LENGTH:]
    recent_score_average = sum(recent_scores)/len(recent_scores)

    comparison_ratio = recent_score_average/score_average

    if comparison_ratio >= 1:
        return 1    # doing better
    elif comparison_ratio >= 0.75:
        return 0    # holding steady
    else:
        return -1   # getting worse