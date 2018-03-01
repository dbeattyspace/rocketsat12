import subprocess as sp
import pandas as pd
import numpy as np
import glob
import time
import matplotlib
import matplotlib.pyplot as plt

font = {'family' : 'serif',
        'weight' : 'bold',
        'size'   : 16}

matplotlib.rc('font', **font)
plt.rc('text', usetex=True)
plt.style.use('fivethirtyeight')
# matplotlib.rcParams['lines.linewidth'] = 1.0

data_dir = 'datalogs/dataset0/'
# date, time, hz_low, hz_high, hz_bin_width, num_samples, dB, dB, ...

files = glob.glob(data_dir + '*')
files.sort()

sweep_df = pd.DataFrame(columns=['file_index', 'time', 'frequency_bin_lower_hz', 'frequency_bin_upper_hz', 'dB'])

for file_index, file_name in enumerate(files):
	with open(file_name, 'r') as f:
		sweep_data_lines = f.readlines()

	for sweep_line in sweep_data_lines:
		sweep_split = sweep_line.replace('\n', '').split(', ')
		# timestamp = time.strptime(sweep_strip[1],'%H:%M:%S')
		timestamp = 1
		low_bin_hz = int(float(sweep_split[2])) 
		high_bin_hz = int(float(sweep_split[3]))
		bin_width_hz = int(float(sweep_split[4]))

		frequency_bin_lower_hz = np.arange(low_bin_hz, high_bin_hz, bin_width_hz)[:-1]
		frequency_bin_upper_hz = np.arange(low_bin_hz, high_bin_hz, bin_width_hz)[1:]
		
		dB_values = np.array(sweep_split[6:]).astype(np.float)
		shape = dB_values.shape

		time_col = np.ones(shape) * timestamp
		file_number_col = (np.ones(shape) * file_index).astype(np.int)

		sample_df = pd.DataFrame({
			'file_index' : file_number_col,
			'time' : time_col,
			'frequency_bin_lower_hz' : frequency_bin_lower_hz,
			'frequency_bin_upper_hz' : frequency_bin_upper_hz,
			'dB' : dB_values,
			})

		sweep_df = sweep_df.append(sample_df)

sweep_df['mean_freq'] = (sweep_df.frequency_bin_lower_hz + sweep_df.frequency_bin_upper_hz) / 2

print(sweep_df)

plt.plot(sweep_df.mean_freq, sweep_df.dB, 'b.')
plt.show()