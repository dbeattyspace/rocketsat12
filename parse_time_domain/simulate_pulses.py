import matplotlib.pyplot as plt
import numpy as np
from math import *
import seaborn as sns
import pandas as pd
import scipy.signal as signal


sns.set()
sns.set_context('poster')

font = {'family' : 'serif',
        'weight' : 'bold',
        'size'   : 16}

plt.rc('text', usetex=True)

## Hoping to use this as a method of comparison to see what the signal should look like

time_span = .1
sample_rate = 20e6

t = np.linspace(0, time_span, time_span * sample_rate)

PRF = 1000
duty_cycle = 0.1

# Actually at 2890 MHz or whatever, but HackRF mixes down to  MHz-ish
wave_frequency = 5e6

wave = np.cos(2 * np.pi * wave_frequency * t)

## Creating one second of pulse pattern and duplicating

samples_per_pulse = sample_rate / PRF

on_samples = round(samples_per_pulse * duty_cycle)
off_samples = round(samples_per_pulse * (1 - duty_cycle))

pulse = np.repeat([1, 0], [on_samples, off_samples])

pulse_pattern = np.tile(pulse, int(PRF * time_span))

## Apply pattern to wave

pulsed_wave = wave * pulse_pattern

frequencies = np.linspace(4.8e6, 5.2e6, 1000)

periodogram = signal.lombscargle(t, pulsed_wave, frequencies, normalize=False)
periodogram = 20 * np.log10(periodogram)

plt.subplot(2, 1, 1)
plt.plot(t, pulsed_wave, marker='.', linestyle='None', alpha=1.0)
plt.plot(t, wave, marker='.', linestyle='None', alpha=0.005)

plt.subplot(2, 1, 2)
plt.plot(frequencies, periodogram)
plt.xlabel('Frequency [ Hz ]')
plt.ylabel('Power [ dB ]')
plt.tight_layout()
plt.show()