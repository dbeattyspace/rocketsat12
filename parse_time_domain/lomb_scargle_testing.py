import matplotlib.pyplot as plt
import numpy as np
from math import *
import seaborn as sns
import pandas as pd
import scipy.signal as signal
import pickle

sns.set()
sns.set_context('poster')

font = {'family' : 'serif',
        'weight' : 'bold',
        'size'   : 16}

# matplotlib.rc('font', **font)
plt.rc('text', usetex=True)
# plt.style.use('fivethirtyeight')

# with open('strengths.pickle', 'rb') as f:
	# [strengths, phase] = pickle.load(f)

# sample_rate = 20e6

# max_time = len(strengths) / sample_rate 

# times = np.linspace(0, max_time, len(strengths))

# reduction = 10000
# times = times[::reduction]
# strengths = strengths[::reduction]
# phase = phase[::reduction]

# frequencies = np.linspace(1, 5e6, 500)

## Simulate what NEXRAD might look like



freq = 2e3

t = np.linspace(0, 20, 20 * freq * 2)

x = np.sin(freq * t)

pulse_width = .1

duty_cycle = 0.50


frequencies = np.linspace(0.1, freq * 3, 100)

periodogram = signal.lombscargle(t, x, frequencies)

plt.plot(frequencies, periodogram)
plt.show()