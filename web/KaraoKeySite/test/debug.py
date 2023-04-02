################################################################################
# debug.py
#
# This file contains all code for debugging-- pretty print statements and
# all that sorts.
################################################################################

def print_pitch_note_data(pitches, pitch_data):
    assert(len(pitches) == len(pitch_data))
    for i in range(len(pitches)):
        pitch = pitches[i]
        note, octave, dev = pitch_data[i]
        print(f'{pitch}Hz: {note}{octave} ({dev} cents)')