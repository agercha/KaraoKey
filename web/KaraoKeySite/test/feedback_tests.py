################################################################################
# feedback_test.py
#
# Run this file to test all algorithms related to feedback-- note detection algo,
# feedback generation.
################################################################################

import json, time, os
import sys
sys.path.insert(0, '..')
from feedback import *

def test_frequency_to_note_data():
    '''
    Test cases for note detection. Looks at all the known note-frequencies pairings
    for each note in 9 octaves and compares that to the actual output of the 
    note detection algorithm.

    If tests fail, outputs (Hz, expected note, actual note), then crashes.
    '''

    print("Testing frequency_to_note_data...", end="")
    # The note_to_freq_data was taken from here: 
    # https://mixbutton.com/mixing-articles/music-note-to-frequency-chart/
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

def test_frequency_feedback():
    '''
    Dummy tests for the feedback algorithm. Reads from dummy_data2's target and 
    user frequencies. 
    '''

    start_time = time.time()

    input_file = "/static/KaraoKeySite/dummy_data2.json"

    # get current working directory
    path = os.getcwd()
    with open(os.path.abspath(os.path.join(path, os.pardir)) + input_file, "r") as f:
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
            total_scores.append(score) # hmmmm...

    duration = time.time() - start_time
    print(f'duration={duration}')

    print(sum(total_scores) / len(total_scores))
    return sum(total_scores) / len(total_scores)


def test_note_detection_accuracy():
    '''
    Dummy tests for the accuracy algorithm. Reads from dummy_data2's target freqs.
    '''
    start_time = time.time()

    input_file = "/static/KaraoKeySite/dummy_data2.json"

    # get current working directory
    path = os.getcwd()
    with open(os.path.abspath(os.path.join(path, os.pardir)) + input_file, "r") as f:
        test_data = json.load(f)
    
    count = 0
    num_outer_chunks = len(test_data)
    # loop over all the partitions of the song
    for outer_index in range(num_outer_chunks):
        outer_chunk = test_data[outer_index]
        # obtain list of target and user frequencies
        target_freqs = outer_chunk["target"]
        # loop over all the inner frequencies contained in each outer chunk
        for inner_index in range(len(target_freqs)):
            target_freq = target_freqs[inner_index]
            note_name, octave_num, _ = frequency_to_note_data(target_freq)
            print(f'{note_name}{octave_num}')
            count += 1
    duration = time.time() - start_time
    print(duration)

def test_instantaenous_feedback():
    '''
    Dummy tests for the feedback algorithm. Reads from dummy_data2's target and 
    user frequencies. 
    '''

    input_file = "/static/KaraoKeySite/dummy_data2.json"

    # get current working directory
    path = os.getcwd()
    with open(os.path.abspath(os.path.join(path, os.pardir)) + input_file, "r") as f:
        test_data = json.load(f)
    

    feedback_dict = \
        {
            "feedback" : [],
            "scores" : []
        }
    res = [feedback_dict.copy(), feedback_dict.copy(), feedback_dict.copy(), feedback_dict.copy()]

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
            feedback = get_qualitative_feedback(user_freq, target_freq, score)
            res[outer_index]["feedback"].append(feedback)
            res[outer_index]["scores"].append(score)

    return res

def demo_feedback():
    res = test_instantaenous_feedback()
    res = json.dumps(res)
    return res