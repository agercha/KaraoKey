################################################################################
# Pitch_detection.py
#
# Aubio pitch detection on a wav file, integrated with note detection algo
################################################################################

import aubio, wave, numpy
from feedback import *
from test import debug

def process_wav_output_pitch(input_wav):

    samplerate = 22050
    frames = 512
    fftSize = 1024

    s = aubio.source(input_wav, samplerate, frames)

    tolerance = 0.8

    aubioPitch = aubio.pitch("yinfft", fftSize, frames, samplerate)
    aubioPitch.set_unit("Hz")
    aubioPitch.set_tolerance(tolerance)

    # total number of frames read
    total_frames = 0
    pitches = []
    pitch_data = []
    while True:
        samples, read = s()
        pitch = aubioPitch(samples)[0]
        if (pitch != 0.0 and pitch < 1000):
            pitches.append(pitch)
            note, octave, deviation = frequency_to_note_data(pitch)
            pitch_data.append((note, octave, deviation)) # 1:1 mapping
            #print(pitch)
        total_frames += read
        if read < frames: break

    debug.print_pitch_note_data(pitches, pitch_data)
    
    # for now, just return the last pitch
    if len(pitches) != 0:
        return float(pitches[-1])
    return 0