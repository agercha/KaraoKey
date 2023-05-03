# aubio pitch detection on a wav file

from aubio import source, pitch

inputFile = "don't_stop_believin_vocals.wav"

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

with open("dont_stop_pitches.txt", "w") as f:
    while True:
        samples, read = s()
        pitch = aubioPitch(samples)[0]
        confidence = aubioPitch.get_confidence()
        print(f"{total_frames/float(samplerate)} {pitch} {confidence}")
        f.write(f"{pitch:.2f}, ")
        total_frames += read
        if read < frames: break
