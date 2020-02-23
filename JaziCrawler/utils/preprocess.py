try:
	from JaziCrawler.utils.logs_handler import fetch_all_data
except ImportError as e:
	from logs_handler import fetch_all_data

import re

def assign_category(url):
	index = 0
	if "lazada" in url:
		index = 3
		data = fetch_all_data("lazada")
	reg = re.search(r'&q(.*)&',url)
	try:
		query = reg.group(1)
	except Exception as e:
		query = ""
	
	cat = url.split('/')[index].lower()

	for row in data:
		if query in row[2] and cat in row[2]:
			return row[1]

def filter_out(site, category, itemName):

	data = fetch_all_data(site)
	for row in data:
		if row[2]==category:
			filters = row[3].split('/')

			for x in filters:
				if x[0:1] != "!": 
					if x.lower() in itemName.lower():
						print()
						try:
							print("{} is disregarded".format(itemName))
						except:
							print("Unicode Error")
						print()
						return True
				else:
					x = x[1:]	
					if x.lower() not in itemName.lower():
						print()
						try:
							print("{} is disregarded".format(itemName))
						except:
							print("Unicode Error")
						print()
						return True
	return False


