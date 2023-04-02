################################################################################
# feedback_test.py
#
# Run this file to test the frequency to note algorithm. The note_to_freq_data
# was taken from here: https://mixbutton.com/mixing-articles/music-note-to-frequency-chart/
################################################################################
from feedback import *

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


test_frequency_to_note_data()