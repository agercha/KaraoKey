# aubio pitch detection on a wav file

import aubio, wave, numpy

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
    while True:
        samples, read = s()
        pitch = aubioPitch(samples)[0]
        if (pitch != 0.0 and pitch < 1000):
            pitches.append(pitch)
            #print(pitch)
        total_frames += read
        if read < frames: break
    
    # for now, just return the last pitch
    if len(pitches) != 0:
        return float(pitches[-1])
    return 0
