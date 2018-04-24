import pickle

from parse_functions import Header_Info, Time_Data

header_info = Header_Info('pulses_from_wav.txt.hdr')

time_data = Time_Data('pulses_from_wav.txt', header_info)

print(time_data.signal_df)

with open('signal_df.pickle', 'wb+') as f:
	pickle.dump(time_data.signal_df, f)