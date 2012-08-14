""" PyAudio Example: Play a wave file in real time"""

from __future__ import division
from pyaudio import PyAudio, paInt16, paContinue, paComplete
from scipy.io.wavfile import read
from time import sleep
import sys

# Your callback will be called every $(blocksize) samples. Small block sizes
# (i.e. <32) can introduce clicking noises if the callback function can not
# return fast enough.
# Long block sizes (i.e. >5000) can introduce clicking noises because portaudio
# has to copy too much data around.
# Generally, you should go as low as possible and avoid doing heavy calculations
# in the callback.
blocksize = 4

if len(sys.argv) != 2:
    print('Plays a wave file.\n\nUsage: %s filename.wav' % sys.argv[0])
    sys.exit(-1)

fs, wave = read(sys.argv[1])
audiolen = len(wave)

pa = PyAudio()

# This function is called every $(blocksize) samples and must process all input
# data and provide all output data. Note that this function is critical for
# performance. No heavy calculations should be done in this function.
def callback(frame_count, input_time, current_time, output_time, in_data):
    played_frames = callback.played_frames
    callback.played_frames = callback.played_frames + frame_count
    if callback.played_frames < audiolen:
        return(wave[played_frames:played_frames+frame_count], paContinue)
    else:
        return(wave[played_frames:audiolen], paComplete)

callback.played_frames = 0

stream = pa.open(format=paInt16,
                 channels=min(wave.shape),
                 frames_per_buffer=blocksize,
                 rate=fs,
                 output=True,
                 stream_callback=callback)

# pretty output
while stream.is_active():
    sys.stdout.write('\rPlaying frame %i/%i (%.2f%%)   '
                 % (callback.played_frames, audiolen,
                    callback.played_frames/audiolen*100))
    sys.stdout.flush()
    sleep(0.1)

sys.stdout.write('\r%s\r' % (' '*40))
sys.stdout.flush()

stream.close()
pa.terminate()
