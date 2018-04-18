import pandas as pd
import numpy as np
import glob
import matplotlib
import matplotlib.pyplot as plt
import time
import seaborn as sns

sns.set()
sns.set_context('poster')

font = {'family' : 'serif',
        'weight' : 'bold',
        'size'   : 16}

matplotlib.rc('font', **font)
plt.rc('text', usetex=True)

# plt.style.use('fivethirtyeight')
# matplotlib.rcParams['lines.linewidth'] = 1.0

# This is a really dumb way to do this, but it works
# Note: will break if your recording time spans midnight
class Time_Logger:
	def __init__(self,):
		pass

	def init_time(self, start_time):
		self.start_time = self.convert_to_seconds_since_midnight(start_time)

	def convert_to_seconds_since_midnight(self, time_str):
		time_obj = time.strptime(time_str,'%H:%M:%S')

		seconds = time_obj.tm_hour * 3600 + time_obj.tm_min * 60 + time_obj.tm_sec

		return seconds

	def get_difference(self, new_time):
		new_time = self.convert_to_seconds_since_midnight(new_time)
		return int(new_time - self.start_time)

#data_dir = 'datalogs/dataset18/'
data_dir = 'datalogs/panorama/'

files = glob.glob(data_dir + '*')
files.sort()

sweep_df = pd.DataFrame(columns=['file_index', 'time', 'frequency_bin_lower_hz', 'frequency_bin_upper_hz', 'dB'])
# date, time, hz_low, hz_high, hz_bin_width, num_samples, dB, dB, ...

time_initialized = False
time_logger = Time_Logger()

for file_index, file_name in enumerate(files):
	with open(file_name, 'r') as f:
		sweep_data_lines = f.readlines()

	for sweep_line in sweep_data_lines:
		sweep_split = sweep_line.replace('\n', '').split(', ')
		
		if not time_initialized:
			time_logger.init_time(sweep_split[1])
			time_initialized = True

		try:
			timestamp = time_logger.get_difference(sweep_split[1])
			low_bin_hz = int(float(sweep_split[2])) 
			high_bin_hz = int(float(sweep_split[3]))
			bin_width_hz = int(float(sweep_split[4]))
		except: 
			print('Frowny')
			continue

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
noise_floor = sweep_df.dB.mean()
signal_sigma = sweep_df.dB.std()


plt.plot(sweep_df.mean_freq / 1e6, sweep_df.dB, 'b.', alpha=0.1)
plt.xlabel('Frequency [ MHz ]')
plt.ylabel('Strength [ dB ]')
plt.tight_layout()
plt.savefig('signal_stength.png', dpi=200)
plt.show()
# plt.show()

# signal_median = sweep_df.groupby('mean_freq').median().dB

signal_df = sweep_df[(sweep_df.dB > (sweep_df.dB.mean() + 2 * sweep_df.dB.std()))  \
                     & (abs(sweep_df.mean_freq - 2.890e9) < 200e3)]

plt.plot(sweep_df.mean_freq / 1e6, sweep_df.dB, 'b.', alpha=0.1)
plt.plot(signal_df.mean_freq / 1e6, signal_df.dB, 'r.', alpha=0.1)
plt.xlabel('Frequency [ MHz ]')
plt.ylabel('Strength [ dB ]')
plt.tight_layout()
plt.savefig('signal_region.png', dpi=200)
plt.show()

plt.plot(signal_df.time, signal_df.dB, 'b.')
plt.xlabel('Time [ seconds ]')
plt.ylabel('Strength [ dB ]')
plt.tight_layout()
plt.savefig('signal_times.png', dpi=200)
plt.show()
