import subprocess as sp
import pandas as pd
import numpy as np
import time
import matplotlib
import matplotlib.pyplot as plt

font = {'family' : 'serif',
        'weight' : 'bold',
        'size'   : 16}

matplotlib.rc('font', **font)
plt.rc('text', usetex=True)
plt.style.use('fivethirtyeight')

## Checking add method. With some center frequency, will adding something be equivalent to shifting?

sample_rate = 100 # Hz

center_frequency = 20 # Hz

fourier_results = 2/self.fft_length * np.abs(numbers_chunk[:self.fft_length//2])