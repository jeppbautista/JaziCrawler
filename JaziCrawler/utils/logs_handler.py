import csv
import os

#TODO updating of image counter
#FIX brand_separator

def brand_separator(input,output):
	id = 0
	with open(input) as f, open(output, 'w', newline='') as outfile:
		read = csv.reader(f, delimiter=',')
		
		for row in read:
			try:
				site = row[0]
				category = row[1]
				code = row[2]
				i = 3

				while True:
					if row[i] == '':
						raise IndexError('')

					else:
						writex = csv.writer(outfile, delimiter=',')
						writex.writerow([id, site, category, code, row[i].strip(), '0'])
						i += 1
						id += 1

			except IndexError as e:
				print(e)

def get_filter(category, input):

	with open(input) as f:
		read = csv.reader(f, delimiter=',')

		for row in read:
			try:
				if row[2] == category:
					return row[3].split('/')
			except IndexError as e:
				print(e)


def fetch_all_data(site, type='dataset_logs',):
	ret = []
	if type == "dataset_logs":
		input = "D:/Jazi/JaziCrawler/JaziCrawler/logs/{}_dataset_logs.csv".format(site)

	with open(input) as f:
		read = csv.reader(f, delimiter=',')

		for row in read:
			ret.append(row)

	return ret

