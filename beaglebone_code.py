import subprocess as sp
import os



i = 0
while os.path.exists('datalogs/dataset{}/'.format(i)):
    i += 1

save_dir = 'datalogs/dataset{}/'.format(i)

os.mkdir(save_dir)

hackrf_sweep_cmd_template = 'hackrf_sweep -f {freq_min_MHz}:{freq_max_MHz} -w {fft_bin_width_Hz}  -1  >| {file_name}'

file_name_template = save_dir + 'hackrf_sweep_output{}.txt'

hackrf_parameters = {
	'freq_min_MHz' : 2800,
	'freq_max_MHz' : 2810,
	'fft_bin_width_Hz' : 100000,
}


file_index = 0

while True:
	hackrf_parameters['file_name'] = file_name_template.format(file_index)

	hackrf_sweep_cmd = hackrf_sweep_cmd_template.format(**hackrf_parameters)

	# Might want to change this to Popen at some point, read that it's better about blocking
	sp.run(hackrf_sweep_cmd, shell=True)

	file_index += 1
