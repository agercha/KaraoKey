################################################################################
# Pitch_detection.py
#
# Aubio pitch detection on a wav file, integrated with note detection algo
################################################################################

import aubio, wave, numpy, time
from KaraoKeySite.feedback import *
from KaraoKeySite.test import debug
from pydub import AudioSegment


def pitch_detect_from_file(input_ogg):
    inputFileWav = "happybirthday.wav"
    song = AudioSegment.from_file(input_ogg)
    song.export(inputFileWav, format="wav")

    samplerate = 44100
    frames = 1024 # HOP SIZE
    fftSize = 2048

    s = aubio.source(inputFileWav, samplerate, frames)
    samplerate = s.samplerate

    tolerance = 0.8

    aubioPitch = aubio.pitch("yinfft", fftSize, frames, samplerate)
    aubioPitch.set_unit("Hz")
    aubioPitch.set_tolerance(tolerance)
    # total number of frames read
    all_pitches = []
    total_frames = 0
    while True:
        samples, read = s()
        pitch = aubioPitch(samples)[0]
        all_pitches.append(pitch)
        # confidence = aubioPitch.get_confidence()
        # print(pitch)
        total_frames += read
        if read < frames: break
    
    return all_pitches


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