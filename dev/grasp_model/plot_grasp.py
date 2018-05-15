import matplotlib.pyplot as plt
import numpy as np
from math import *
import seaborn as sns
import pandas as pd

sns.set()
sns.set_context('poster')

font = {'family' : 'serif',
        'weight' : 'bold',
        'size'   : 16}

# matplotlib.rc('font', **font)
plt.rc('text', usetex=True)
# plt.style.use('fivethirtyeight')

azimuth = []
gain_db = []

with open('ticra-export.dat') as f:
	for line in f.readlines():
		try:
			azimuth.append(float(line.split()[0]))
			gain_db.append(float(line.split()[1]))
		except IndexError:
			continue

gain_df = pd.DataFrame({'gain_db': gain_db}, index=azimuth)

# Error of 0.2 deg
# On average the angle difference between each index is 0.09 deg
# So 0.2 deg is the difference of 2 indices, ish

gain_shift_from_pointing_error = (gain_df.gain_db - gain_df.gain_db.shift(2))


plt.plot(gain_df, 'b.', markersize=5)
# plt.plot(pd.rolling_mean(gain_df, 20), 'g.')
# plt.plot(gain_shift_from_pointing_error, 'r.')
plt.title('GRASP Model')
plt.xlabel('Azimuth Angle [${}^\circ$]')
plt.ylabel('Gain[ dB ]')
# plt.legend('')
plt.tight_layout()
plt.savefig('antenna_pattern.png', dpi=200)
plt.show()
# plt.close()

