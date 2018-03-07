import subprocess as sp
import numpy as np
import time

frequencies = np.array([2865e6, 2870e6, 2875e6, 2950e6], dtype=np.int)

cmd = 'hackrf_transfer -f {:d} -c 100'

while True:
	for freq in frequencies:
		print('Transmitting on {:2E}'.format(freq))
		cmd_instance = cmd.format(freq)
		try:
			sp.run(cmd_instance, shell=True, timeout=5)
		except sp.TimeoutExpired:
			# This is supposed to happen
			continue