import matplotlib.pyplot as plt
import numpy as np
from math import *
import seaborn as sns
import pandas as pd
import pickle

sns.set()
sns.set_context('poster')

font = {'family' : 'serif',
        'weight' : 'bold',
        'size'   : 16}

plt.rc('text', usetex=True)

with open('signal_df.pickle', 'rb') as f:
	signal_df = pickle.load(f)

# print(signal_df)

plt.plot(signal_df.strength[~signal_df.noise_floor], marker='.', linestyle='None')
plt.plot(signal_df.strength[signal_df.noise_floor], marker='.', linestyle='None')
plt.xlabel('Time')
plt.ylabel('Strength')
plt.legend(['Outliers', 'Noise Floor'])
plt.tight_layout()
plt.savefig('pulse.png', dpi=200)
plt.close()