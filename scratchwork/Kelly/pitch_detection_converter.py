######################################################
# Converts .ogg to .wav file                         #
# Performs pitch detection on newly formed .wav file #
######################################################

import time
from aubio import source, pitch
from pydub import AudioSegment

start = time.time()
inputFileOgg = "happybirthday.ogg"
inputFileWav = "happybirthday.wav"

song = AudioSegment.from_file(inputFileOgg)
song.export(inputFileWav, format="wav")

samplerate = 44100
frames = 1024 # HOP SIZE
fftSize = 2048

s = source(inputFileWav, samplerate, frames)
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
    print(pitch)
    '''output = "\n" + str(samples)
    output += "\n" + str(pitch)
    print(read)'''
    total_frames += read
    if read < frames: break


print("time", time.time() - start)
