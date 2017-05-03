"""
Play audio of asteroseismology light curve.
"""

import os
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import kepler_data as kd
import kplr
import wave

id = "5515314"
LC_DIR = "/Users/ruthangus/.kplr/data/lightcurves/{}".format(id.zfill(9))
if not os.path.exists(LC_DIR):
    client = kplr.API()
    star = client.star("{}".format(id))
    star.get_light_curves(fetch=True, short_cadence=False)

x, y, yerr = kd.load_kepler_data(LC_DIR)
y = y/np.var(y)

plt.clf()
plt.plot(x, y, "k.")
plt.savefig("lc")

p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 10.0   # in seconds, may be float
f = 440.0        # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
signal = y

plt.clf()
plt.plot(signal)
plt.xlabel("Time")
plt.ylabel("Flux")
plt.savefig("signal")

samples = (signal).astype(np.float32)

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# play. May repeat with different volume values (if done interactively)
stream.write(volume*samples)

stream.stop_stream()
stream.close()

p.terminate()

# CHUNK = 1024
# FORMAT = pyaudio.paInt16
# CHANNELS = 2
# RATE = 44100
# RECORD_SECONDS = 5

# wf = wave.open("{}.wav".format(id), 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()
