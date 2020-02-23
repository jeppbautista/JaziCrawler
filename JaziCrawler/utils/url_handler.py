
import csv
import os

def retrieve_unscraped(site):
	#FIX temporary, make file dynamic
	store = []
	counter = 0
	if site == "lazada":
		with open('{}\JaziCrawler\logs\lazada_dataset_logs.csv'.format(os.getcwd())) as f:
			read = csv.reader(f, delimiter=',')

			for row in read:
				if(int(row[4])==0):
					store.append(row)

		return store


def handle_start_urls(site):
	links = retrieve_unscraped(site)
	if site == 'lazada':
		for i in links:
			yield {
				i[2]
			}

			
		#TODO Check all categories not yet scraped (for dataset)
		#TODO Check all categories are up to date (for indexing)
        
	#TODO other sites


