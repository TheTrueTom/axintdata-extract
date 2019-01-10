#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    AXINTDATA LIMITED SET EXTRACT TOOL
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Tool to gather some AXINTDATA in a specified folder
    :copyright: 2018 - GLINCS-AXINT, see AUTHORS for more details
    :license: Proprietary and confidential, see LICENSE for more details
"""

import os, datetime, re, csv, time

AXINT_DATA_ORIGIN = "AXINTDATA"
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

	return SensorData(date, values, probe, sensor)

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
				if len(list(open(os.path.join(origin, folder, file)))) == 16392: # 16392 = nombre de lignes d'un fichier avec 4 histogrammes complets
					all_sensor_data.append(extract_data_from_file(os.path.join(origin, folder, file), file, date))
				else:
					print("ERROR :: File " + file + " is incomplete")

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
			print("Error :: Data from " + data.probe + "_" + data.sensor + " for date " + data.date.strftime("%d-%m-%Y_%Hh") + " is corrupted")

	return clean_datalist

def output_CSV(path, datalist, sort):
	if sort == 'date':
		date_set = set()

		for data in datalist:
			date_set.add(data.date)

		for date in date_set:
			new_datalist = [x for x in datalist if x.date == date]
			
			filename = date.strftime("%d-%m-%Y_%Hh.csv")

			file = open(os.path.join(path, filename), 'w')
			out = csv.writer(file, lineterminator='\n', delimiter=',', quotechar="\"", quoting=csv.QUOTE_ALL)

			sensor_probe_list = ['Chan']

			for data in new_datalist:
				sensor_probe_list.append("Value " + data.probe + "_" + data.sensor)

			out.writerow(sensor_probe_list)

			for i in range(0,4096):
				row = [i]

				for data in new_datalist:
					row.append(data.value[i])

				out.writerow(row)
	else:
		detector_set = set()

		for data in datalist:
			detector_set.add(data.probe + '_' + data.sensor)

		for detector in detector_set:
			new_datalist = [x for x in datalist if x.probe + '_' + x.sensor == detector]
			
			filename = data.probe + '_' + data.sensor + '.csv'

			file = open(os.path.join(path, filename), 'w')
			out = csv.writer(file, lineterminator='\n', delimiter=',', quotechar="\"", quoting=csv.QUOTE_ALL)

			sensor_probe_list = ['Chan']

			for data in new_datalist:
				sensor_probe_list.append(data.date.strftime("%d-%m-%Y_%Hh"))

			out.writerow(sensor_probe_list)

			for i in range(0,4096):
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

	#output_CSV(OUTPUT_FOLDER, clean_data, 'date')
	output_CSV(OUTPUT_FOLDER, clean_data, 'sensor')
	print("Impression CSV -> OK")