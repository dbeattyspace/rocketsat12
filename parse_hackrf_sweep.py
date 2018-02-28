import subprocess as sp
import pandas as pd


# date, time, hz_low, hz_high, hz_bin_width, num_samples, dB, dB, ...

print(spectrum_table)

spectrum_df = pd.read_csv(hackrf_parameters['file_name'])

# spectrum_df.columns = ['date', 'time', 'hz_low', 'hz_high', 'hz_bin_width', 'num_samples',]

print(spectrum_df)