import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import struct

font = {'family' : 'serif',
        'weight' : 'bold',
		'size'   : 16}

matplotlib.rc('font', **font)
plt.rc('text', usetex=True)
plt.style.use('fivethirtyeight')

file_name = 'output_testing.txt'

with open(file_name, 'rb') as f:
	file_data = f.read()


sample_points = 19200

sample_frequency = 100e6

bytes_per_sample = 4

file_data = file_data[0:sample_points*bytes_per_sample]


float_chunks = [file_data[i:i + bytes_per_sample] for i in range(0, len(file_data), bytes_per_sample)]

float_data = []

for float_chunk in float_chunks:
	float_value = struct.unpack('f', float_chunk)
	float_data.append(float_value)


frequency_bins = np.linspace(0, sample_frequency/2, sample_points/2)

fourier_results = 2/sample_points * np.abs(float_data[:sample_points//2])

plt.axvline(40e6, linewidth=1, color='r')
plt.axvline(35e6, linewidth=1, color='r')
plt.axvline(30e6, linewidth=1, color='r')
plt.axvline(45e6, linewidth=1, color='r')
plt.stem(frequency_bins, fourier_results)
plt.xlabel('Frequency [Hz]')
plt.ylabel('dBFS')
plt.title('4 Sources, {} Bins'.format(sample_points))
plt.tight_layout()
plt.savefig('combined_{}_bins.png'.format(sample_points))
plt.show()



