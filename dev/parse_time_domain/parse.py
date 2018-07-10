import pickle

from parse_functions import Header_Info, Time_Data

header_info = Header_Info('50_duty_cycle.txt.hdr')

time_data = Time_Data('50_duty_cycle.txt', header_info)

print(time_data.signal_df)

with open('signal_df.pickle', 'wb+') as f:
	pickle.dump(time_data.signal_df, f)