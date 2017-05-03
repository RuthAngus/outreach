import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from math import log2, pow

plotpar = {'axes.labelsize': 18,
           'font.size': 10,
           'legend.fontsize': 18,
           'xtick.labelsize': 18,
           'ytick.labelsize': 18,
           'text.usetex': True}
plt.rcParams.update(plotpar)


def freq2note(freq):
    A4 = 440
    C0 = A4*pow(2, -4.75)
    name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    return name[n] + str(octave)


def convert_to_frequency(nu_max, dnu):
    Sun_f = 440.0  # A
    Sun_f = 261.625565  # Middle C
    Sun_f = 523.251  # High C
    real_sun_freq = 1/5/60
    print(real_sun_freq)
    print("Wavelength scaled down by", 1/(real_sun_freq / Sun_f)/1000,
          "thousand")
    nm = nu_max/real_sun_freq * Sun_f
    dn = dnu/real_sun_freq * Sun_f
    return nm, nm - dn, nm + dn


def make_star_audio(nu_max, dnu, duration):
    p = pyaudio.PyAudio()

    volume = 0.5     # range [0.0, 1.0]
    fs = 44100       # sampling rate, Hz, must be integer
    f = 440.0        # sine frequency, Hz, may be float

    nm, f2, f3 = convert_to_frequency(nu_max, dnu)
    print("Freq =", nm, "Hz")

    # generate samples, note conversion to float32 array
    freqs = np.arange(fs*duration)
    signal = np.sin(2*np.pi*freqs*nm/fs) + \
        .5*np.sin(2*np.pi*freqs*f2/fs) + \
        .5*np.sin(2*np.pi*freqs*f3/fs) + \
        np.random.randn(len(freqs)) * .01

    plt.clf()
    plt.plot(signal[:1000])
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
    return nm


if __name__ == "__main__":
    nm = make_star_audio(1./5/60, 1./5/60/10, 10.)
    print("Note = ", freq2note(nm))
    nm = make_star_audio(1000*1e-6, 50*1e-6, 5.)
    print("Note =", freq2note(nm))
