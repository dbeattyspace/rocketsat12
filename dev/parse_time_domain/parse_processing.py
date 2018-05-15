import matplotlib.pyplot as plt
import numpy as np
from math import *
import seaborn as sns
import pandas as pd
import pickle
import scipy.signal as signal

sns.set()
sns.set_context('poster')

font = {'family' : 'serif',
        'weight' : 'bold',
        'size'   : 16}

plt.rc('text', usetex=True)

with open('signal_df.pickle', 'rb') as f:
	signal_df = pickle.load(f)

# print(signal_df)

plt.subplot(2, 1, 1)
plt.plot(signal_df.strength[~signal_df.noise_floor], marker='.', linestyle='None')
plt.plot(signal_df.strength[signal_df.noise_floor], marker='.', linestyle='None')
plt.xlabel('Time')
plt.ylabel('Strength')
plt.legend(['Outliers', 'Noise Floor'])
# plt.tight_layout()
# plt.savefig('pulse.png', dpi=200)
# plt.show()

frequencies = np.linspace(4.8e6, 5.2e6, 1000)

periodogram = signal.lombscargle(signal_df.index[~signal_df.noise_floor], signal_df.strength[~signal_df.noise_floor], frequencies, normalize=False)
periodogram = 20 * np.log10(periodogram)

plt.subplot(2, 1, 2)
plt.plot(frequencies, periodogram)
plt.xlabel('Frequency [ Hz ]')
plt.ylabel('Power [ dB ]')
plt.tight_layout()
plt.show()