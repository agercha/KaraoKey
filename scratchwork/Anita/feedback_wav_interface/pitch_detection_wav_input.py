# aubio pitch detection on a wav file

from aubio import source, pitch
from feedback import *

inputFile = "C_Major_Scale_Fast_piano.wav"

samplerate = 44100
frames = 1024
fftSize = 2048

s = source(inputFile, samplerate, frames)
samplerate = s.samplerate

tolerance = 0.8

aubioPitch = pitch("yinfft", fftSize, frames, samplerate)
aubioPitch.set_unit("Hz")
aubioPitch.set_tolerance(tolerance)

# total number of frames read
total_frames = 0
while True:
    samples, read = s()
    pitch = aubioPitch(samples)[0]
    confidence = aubioPitch.get_confidence()
    if (pitch != 0):
        note, octave, _ = frequency_to_note_data(pitch)
        print(f"{total_frames/float(samplerate)} {pitch}: {note}{octave}")
    total_frames += read
    if read < frames: break
