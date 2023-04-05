# aubio pitch detection on a wav file

from aubio import source, pitch

# inputFile = "C_Major_Scale_Fast/C_Major_Scale_Fast_piano.wav"
inputFile = "../Anna/hbdmyvocals.wav"

samplerate = 44100
# frames = 1024
frames = 200
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
    print(f"{total_frames/float(samplerate)} {pitch} {confidence}")
    total_frames += read
    if read < frames: break
