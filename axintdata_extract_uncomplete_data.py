#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    AXINTDATA LIMITED SET EXTRACT TOOL
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Tool to gather some AXINTDATA in a specified folder
    This version has been modified to proceed extraction on UNCOMPLETE files
    List of modifications : 
    Comment lines 99 100 101 / 115 117 118
    Correction line 157 : len(data.value.keys()) to replace the constant value 4096. 
    :copyright: 2018 - GLINCS-AXINT, see AUTHORS for more details
    :license: Proprietary and confidential, see LICENSE for more details
"""

import os, datetime, re, csv, time

AXINT_DATA_ORIGIN = "C:/AXINTDATA"
EXTRACT_LIST = 'extractlist.txt'

OUTPUT_FOLDER = "AXINTDATA_TREATED"

"""
UTILS PART
"""

class SensorData:
	def __init__(self, date, value, probe, sensor):
		self.date = date
		self.value = value
		self.probe = probe
		self.sensor = sensor

	def integrated_signal(self, start, end):
		value = 0

		for i in range (start, end):
			value += self.value[i]

		return value


def extract_data_from_file(path, file, date):
	values = {}

	with open(path, 'rb') as csvfile:
		for line in csvfile:
			utf8line = line.decode('utf8')

			if utf8line[0] == "	":
				utf8list = utf8line.split("	")
				channel = int(utf8list[5]) * 256 + int(utf8list[4])
				value = int(utf8list[8]) * 256 + int(utf8list[7])

				if channel in values.keys():
					values[channel] += value
				else:
					values[channel] = value

	probe = re.findall(r'DRN[0-9]{4}', file)[0]
	sensor = re.findall(r'DRN[0-9]{4}_[0-9]{2}', file)[0][-2:]

	data = SensorData(date, values, probe, sensor)

	return data

def extract_extract_list(path):
	extract_list = []

	with open(path, "r") as objf:
		for line in objf:
			date = datetime.datetime.strptime(line.strip('\n').strip(" "), "%d/%m/%Y %HH")
			extract_list.append(date)

	return extract_list

def extract_data_from_date_list(extract_list, root_folder):
	# Crée une liste de tous les dossiers AXINDATA présents
	axint_data_files_list = os.listdir(root_folder)

	data = []

	for extract_date in extract_list:
		date_to_extract = extract_date.strftime('%m-%d-%y')
		pattern = r'%s_DRN[0-9]{4}_[0-9]{2}' % date_to_extract

		date_axintdata_folders = [x for x in axint_data_files_list if re.match(pattern, x)]

		data.extend(extract_all_for_date(root_folder, date_axintdata_folders, extract_date))

	return data

def extract_all_for_date(origin, folder_list, date):
	date_to_extract = date.strftime('%m-%d-%y_%Hh')
	pattern = r'%s_DRN[0-9]{4}_[0-9]{2}' % date_to_extract
	all_sensor_data = []

	for folder in folder_list:
		for file in os.listdir(os.path.join(origin, folder)):
			if re.match(pattern, file):
				if len(list(open(os.path.join(origin, folder, file)))) == 16392: # = attention nombre de lignes d'un fichier de 495Ko : 8137
					all_sensor_data.append(extract_data_from_file(os.path.join(origin, folder, file), file, date))
				else:
#					print("ERROR :: File " + file + " is incomplete")
					all_sensor_data.append(extract_data_from_file(os.path.join(origin, folder, file), file, date))

	if len(all_sensor_data) != 0:
		print("Extraction " + date_to_extract + " -> OK ")
	else:
		print("ERROR :: No file found for " + date_to_extract)

	return all_sensor_data

def clean_data(datalist):
	clean_datalist = []

	for data in datalist:
		if len(data.value.keys()) == 4096:
			clean_datalist.append(data)
		else:
			clean_datalist.append(data)
#			print("Error :: Data from " + data.probe + "_" + data.sensor + " for date " + data.date.strftime("%d-%m-%Y_%Hh") + " is corrupted")

	return clean_datalist

def output_CSV(path, datalist, sort, integration_start, integration_end):
	sort_set = set()

	for data in datalist:
		sort_set.add(data.date if sort == 'date' else (data.probe + '_' + data.sensor))

	for sort_element in sort_set:
		new_datalist = []

		if sort == 'date':
			new_datalist = [x for x in datalist if x.date == sort_element]
		else:
			new_datalist = [x for x in datalist if (x.probe + '_' + x.sensor) == sort_element]

		if not os.path.exists(path):
			os.makedirs(path)

		filename = sort_element.strftime("%d-%m-%Y_%Hh.csv") if sort == 'date' else sort_element + '.csv'
		integrated_filename = filename[:-4] + '_integrated.csv'

		file = open(os.path.join(path, filename), 'w')
		integrated_file = open(os.path.join(path, integrated_filename), 'w')

		out = csv.writer(file, lineterminator='\n', delimiter=',', quotechar="\"", quoting=csv.QUOTE_ALL)
		integrated_out = csv.writer(integrated_file, lineterminator='\n', delimiter=',', quotechar="\"", quoting=csv.QUOTE_ALL)

		header_list = ['Chan']

		for data in new_datalist:
			header_list.append(data.probe + "_" + data.sensor if sort == 'date' else data.date.strftime("%d-%m-%Y_%Hh"))

		out.writerow(header_list)
		integrated_out.writerow(header_list)

#		for i in range(1,len(data.value.keys()), 2):
		for i in range(1,4096, 2):			
			row = [i]
			for data in new_datalist:
				row.append(data.value[i])


			out.writerow(row)

if __name__ == '__main__':
	extract_list = extract_extract_list(EXTRACT_LIST)
	print("Liste d'extractions -> OK")

	data = extract_data_from_date_list(extract_list, AXINT_DATA_ORIGIN)
	print("Extraction des données -> OK")

	clean_data = clean_data(data)
	print("Nettoyage des données -> OK")

	#output_CSV(OUTPUT_FOLDER, clean_data, 'date', 1200, 1800)
	output_CSV(OUTPUT_FOLDER, clean_data, 'sensor', 1200, 1800)
	print("Impression CSV -> OK")