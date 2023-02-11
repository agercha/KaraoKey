# pyaudio + aubio demo

import aubio
import numpy as np
import pyaudio

p = pyaudio.PyAudio()

frames = 1024 # computationally expensive the lower we go
sampleRate = 44100 # standard sample rate for recording music (samples/sec)
stream = p.open(format = pyaudio.paFloat32,
                channels = 1,
                rate = sampleRate,
                input = True, # using mic input
                frames_per_buffer = frames) 

'''
20 Hz is accepted as the lower limit of human hearing, which leads to a 
Fast Fourier Transform size of 2205. 

However, this number must be a multiple of 2, so we use 2048 to keep computing
power. Additionally, we don't expect many users to reach this lower limit. 
'''
fftSize = 2048
aubioPitch = aubio.pitch("yin", fftSize, frames, sampleRate)
aubioPitch.set_unit("Hz") # make sure output is in Hz
aubioPitch.set_tolerance(0.9) # had to set this value

print("*** starting recording")
while True:
    try:
        audiobuffer = stream.read(frames)
        signal = np.frombuffer(audiobuffer, dtype=aubio.float_type)

        signalPitch = aubioPitch(signal)[0]
        confidence = aubioPitch.get_confidence()

        if (signalPitch != 0.0):
            print(f"{signalPitch} / {confidence}")
    except KeyboardInterrupt:
        print("*** Ctrl+C pressed, exiting")
        break

print("*** done recording")
stream.stop_stream()
stream.close()