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

from gnuradio_output_functions import Header_Info, GNUradio_FFT_Data, GNUradio_time_Data

file_name = 'output_testing.txt'
fft_length = 19200

header_info = Header_Info(file_name + '.hdr')

gnuradio_data = GNUradio_FFT_Data(file_name, header_info, fft_length)

print(gnuradio_data.spectral_density_df)

spectral_density_df = gnuradio_data.spectral_density_df

plt.plot(spectral_density_df.frequency_bin, spectral_density_df.dBFS, alpha=0.1)
plt.show()

import sys; sys.exit(0)

# plt.axvline(40e6, linewidth=1, color='r')
# plt.axvline(35e6, linewidth=1, color='r')
# plt.axvline(30e6, linewidth=1, color='r')
# plt.axvline(45e6, linewidth=1, color='r')
# plt.stem(frequency_bins, fourier_results)
# plt.xlabel('Frequency [Hz]')
# plt.ylabel('dBFS')
# plt.title('4 Sources, {} Bins'.format(sample_points))
# plt.tight_layout()
# plt.savefig('combined_{}_bins.png'.format(sample_points))
# plt.show()



