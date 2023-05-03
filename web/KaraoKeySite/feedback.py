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

    ### Parameters:
        frequency: the frequency in Hz that we'd like to get the note data from.
    ### Return value:
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

def get_note_accuracy(input_note:str, target_note:str):
    '''
    Given an input note and a target note to hit, calculates an 
    accuracy score based on how close the input note was to the target
    note.

    This function is used for instantaneous feedback generation. 

    ### Parameters:
        input_note: the note that the user sang at. Input note comes from \
                    frequency_to_note_data.
        target_note: the target note the user is aiming to sing. Target note \
                    also comes from frequency_to_note_data.

    ### Return value:
        Score ranging from [0, NOTE_WEIGHTING] reflecting how close the input \
        note was to the target frequency.
    '''
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
    
    return round(note_accuracy, 2)

def get_accuracy_score(input_freq:float, target_freq:float):
    '''
    Given an input frequency and a target frequency to hit, calculates an 
    accuracy score based on how close the input frequency was to the target
    frequency.

    This function is used for instantaneous feedback generation. 

    ### Parameters:
        input_freq: the frequency in Hz that the user sang at. Input freq comes\
                    from the pitch detection algorithm.
        target_freq: the target frequency in Hz that the user is aiming to sing\
                     at. Target frequency also comes from the PDA.

    ### Return value:
        Score ranging from [0, 1] reflecting how close the input frequency was
        to the target frequency.
    '''

    if (input_freq == 0 or target_freq == 0):
        # print(f'Zero input: input_freq={input_freq}, target_freq={target_freq}')
        return int(input_freq == target_freq)

    input_note, input_octave, input_cents_deviation = frequency_to_note_data(input_freq)
    target_note, target_octave, target_cents_deviation = frequency_to_note_data(target_freq)
    
    note_accuracy = get_note_accuracy(input_note, target_note)
    cents_accuracy = 30 * (1-(abs(input_cents_deviation - target_cents_deviation) / 100)) if note_accuracy else 0
    accuracy_score = note_accuracy + cents_accuracy

    user_feedback_str = f"usr: {input_note}{input_octave} ({input_cents_deviation:.2f})".ljust(16)
    tgt_feedback_str = f"tgt: {target_note}{target_octave} ({target_cents_deviation:.2f})".ljust(18)
    # print(f'{user_feedback_str} {tgt_feedback_str}', end="")
    # print(f"note accuracy: {note_accuracy}, cents accuracy: {cents_accuracy}, score={accuracy_score:.2f}%")
    return accuracy_score

def get_sharp_or_flat(input_freq, target_freq, accuracy_score):
    '''
    Given an input frequency, target frequency to hit, and accuracy score, 
    returns qualitative feedback.

    This function is used for instantaneous feedback generation. 

    ### Parameters:
        input_freq: the frequency in Hz that the user sang at. Input freq comes\
                    from the pitch detection algorithm.
        target_freq: the target frequency in Hz that the user is aiming to sing\
                     at. Target frequency also comes from the PDA.
        accuracy_score: accuracy score 

    ### Return value:
        Qualitative instantaneous feedback.
    '''
    # Either input or target freq was 0
    if accuracy_score == 0: return 0

    _, _, input_cents_deviation = frequency_to_note_data(input_freq)
    _, _, target_cents_deviation = frequency_to_note_data(target_freq)

    relative = 0
    if (accuracy_score >= NOTE_WEIGHTING and 
        (abs(input_cents_deviation - target_cents_deviation) <= 7)):
        relative = 0
    else:
        if input_freq > target_freq:
            relative = 1
        else:
            relative = -1

    return relative

def get_qualitative_feedback(input_freq, target_freq, accuracy_score):
    '''
    Given an input frequency, target frequency to hit, and accuracy score, 
    returns qualitative feedback.

    This function is used for instantaneous feedback generation. 

    ### Parameters:
        input_freq: the frequency in Hz that the user sang at. Input freq comes\
                    from the pitch detection algorithm.
        target_freq: the target frequency in Hz that the user is aiming to sing\
                     at. Target frequency also comes from the PDA.
        accuracy_score: accuracy score 

    ### Return value:
        Qualitative instantaneous feedback.
    '''
    # Either input or target freq was 0
    if accuracy_score == 0: return ""

    relative = get_sharp_or_flat(input_freq, target_freq, accuracy_score)

    if relative == 0:
        accuracy_feedback = "Perfect! On pitch."
    elif relative == -1:
        accuracy_feedback = "You are flat."
    else:
        accuracy_feedback = "You are sharp."

    return accuracy_feedback
def feedback_from_res(input_json_filepath:str, user_freqs):

    # this will probably need to be modified once we actually have the actual
    # file directory.
    with open(input_json_filepath) as f:
        test_data = json.load(f)
    
    total_scores = []
    num_outer_chunks = len(test_data)
    user_ind = 0
    # loop over all the partitions of the song
    for outer_index in range(num_outer_chunks):
        outer_chunk = test_data[outer_index]
        # num_inner_chunks = outer_chunk["length"]

        # obtain list of target and user frequencies
        target_freqs = outer_chunk["target"]
        # user_freqs = outer_chunk["user"]

        # loop over all the inner frequencies contained in each outer chunk
        for inner_index in range(len(target_freqs)):
            target_freq = target_freqs[inner_index]
            if user_ind < len(user_freqs): 
                user_freq = user_freqs[user_ind]
            else:
                user_freq = 0
            score = get_accuracy_score(target_freq, user_freq)
            if (score != 0): total_scores.append(score) # hmmmm...
            user_ind += 1
    
    # print(outer_index, inner_index, user_ind)
    # assert(False)
    print(sum(total_scores) / len(total_scores))
    return sum(total_scores) / len(total_scores)

def get_progression(scores):
    '''
    Given an input list of scores, returns a value in [-1, 0, +1] representing 
    how the user is progressing through the song.

    Parameters:
        scores: an array of floats representing scores. This information should\
                be generated by the instantanous feedback mechanism.
    Return value:
        A number in [-1, 0, +1]. 
        -1 represents the user's performance is getting worse. 
        0 represents the user's performance is holding steady
        +1 represents the user's performance is improving.
    '''
    COMP_LENGTH = 15 # COMP_LENGTH determines how volatile the progression score will
                     # swing around. 
    RECENT_SCORES_LENGTH = COMP_LENGTH//3 

    if len(scores) < COMP_LENGTH:
        return ""


    # the scores that we will compare the most recently sung scores to
    comparison_scores = scores[-COMP_LENGTH:]
    score_average = sum(scores)/len(scores)

    recent_scores = scores[-RECENT_SCORES_LENGTH:]
    recent_score_average = sum(recent_scores)/len(recent_scores)

    comparison_ratio = recent_score_average/score_average

    if comparison_ratio >= 1:
        return "Keep it up-- You're improving!"
    elif comparison_ratio >= 0.75:
        return "Holding steady."
    else:
        return "You can do this!"