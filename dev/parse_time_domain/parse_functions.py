import subprocess as sp
import re
import pandas as pd
import struct
import numpy as np

class Header_Info:
	def __init__(self, file_name):
		self.file_name = file_name

		self.read_file_data()
		self.define_headers_list()

	def read_file_data(self,):
		gnuradio_command = 'gr_read_file_metadata -D {}'.format(self.file_name)
		gnuradio_function_output = sp.run(gnuradio_command, shell=True, stdout=sp.PIPE).stdout.decode()
		
		self.file_data = gnuradio_function_output

	def define_headers_list(self,):
		self.file_output_header_list = self.file_data.split('\n\n\n\n')

		self.headers = []

		for file_output_header in self.file_output_header_list:
			if len(file_output_header) == 0:
				continue
			self.define_header_dictionary(file_output_header)

	def define_header_dictionary(self, file_output_header):
		header_dict = dict()

		header_dict['header_number'] = self.get_header_number(file_output_header)
		header_dict['sample_rate_sps'] = self.get_sample_rate(file_output_header)
		header_dict['data_type_size_bytes'] = self.get_data_type_size(file_output_header)
		header_dict['data_type'] = self.get_data_type(file_output_header)
		header_dict['data_length_bytes'] = self.get_data_length(file_output_header)
		header_dict['seconds_since_start'] = self.get_seconds_since_start(file_output_header)

		if header_dict['data_length_bytes'] == 0:
			return

		self.headers.append(header_dict)


	def get_header_number(self, output_str):
		relevant_line = re.search('HEADER \d*', output_str).group()

		header_number = int(relevant_line.split(' ')[-1])

		return header_number

	def get_sample_rate(self, output_str):
		relevant_line = re.search('Sample Rate: \d*.\d*', output_str).group()

		sample_rate = float(relevant_line.split(':')[-1])

		return sample_rate

	def get_data_type_size(self, output_str):
		relevant_line = re.search('Item size: \d*', output_str).group()

		data_type_size_bytes = int(relevant_line.split(':')[-1])

		return data_type_size_bytes

	def get_data_type(self, output_str):
		relevant_line = re.search('Data Type: \w*', output_str).group()

		data_type = relevant_line.split(':')[-1].strip()

		return data_type

	def get_data_length(self, output_str):
		relevant_line = re.search('Size of Data: \d* bytes', output_str).group()

		data_length_bytes = int(relevant_line.split(' ')[-2])

		return data_length_bytes

	def get_seconds_since_start(self, output_str):
		relevant_line = re.search('Seconds: \d*.\d*', output_str).group()

		seconds_since_start = float(relevant_line.split(':')[-1])

		return seconds_since_start


class Time_Data:
	def __init__(self, file_name, header_info):
		self.file_name = file_name
		self.header_info = header_info

		self.signal_df = pd.DataFrame()

		self.load_file_data()
		self.populate_df()

	def load_file_data(self):
		with open(self.file_name, 'rb') as f:
			self.file_data = f.read()

	def populate_df(self):
		self.file_byte_index = 0

		self.define_struct_format()

		for header in self.header_info.headers:
			self.load_header_chunk_only_outliers(header)
			# self.load_header_chunk(header)


	def define_struct_format(self):
		# Making the assumption here that all files are same type
		# It would be super weird if they weren't
		# Add a check if feeling paranoid, I guess?

		sample_header = self.header_info.headers[0]

		# If working with more data types, add more options here
		if sample_header['data_type'] == 'float':
			format_character = 'f'
		else:
			Exception('Unknown data type')

		datapoints_in_file = int(sample_header['data_length_bytes'] / sample_header['data_type_size_bytes'])

		self.struct_format = '{}{}'.format(datapoints_in_file, format_character)

	def load_header_chunk_only_outliers(self, header):
		# Time vector
		samples = header['data_length_bytes'] / header['data_type_size_bytes']
		time = np.linspace(0, samples / header['sample_rate_sps'], samples) + header['seconds_since_start'] 


		# Want the outliers from signal strengths
		# Also want a sampling of other points that are the same as the mean 
		strength_chunk = self.unpack_from_bytes(header)

		signal_mu = strength_chunk.mean()
		signal_sigma = 5 * strength_chunk.std()

		outlier_indices = (strength_chunk > (signal_mu + signal_sigma)) | (strength_chunk < (signal_mu - signal_sigma)) 
		reduction = 1000
		random_indices = np.zeros(strength_chunk.shape, dtype=np.bool)
		random_indices[::reduction] = True

		strength_chunk[random_indices] = signal_mu

		indices_to_keep = outlier_indices | random_indices

		strength = strength_chunk[indices_to_keep]

		header_number = np.ones(strength.shape) * header['header_number']

		time = time[indices_to_keep]

		chunk_df = pd.DataFrame({
			'strength' : strength,
			'header_number' : header_number, 
			'noise_floor' : random_indices[indices_to_keep],
			}, index=time)

		print(header_number[0])

		self.signal_df = self.signal_df.append(chunk_df)

	def unpack_from_bytes(self, header):
		chunk_start_index = self.file_byte_index
		chunk_end_index = chunk_start_index + header['data_length_bytes']
		self.file_byte_index = chunk_end_index

		bytes_chunk = self.file_data[chunk_start_index:chunk_end_index]

		numbers_chunk = struct.unpack(self.struct_format, bytes_chunk)

		return np.array(numbers_chunk)