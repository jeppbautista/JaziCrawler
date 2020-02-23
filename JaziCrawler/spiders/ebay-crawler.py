from bs4 import BeautifulSoup
import requests
import argparse
import os
import random
import urllib.request
import csv

url = requests.get("https://www.ebay.ph/b/Laptops-Netbooks/175672/bn_1648276")
array = []

def write_to_csv(array):
	w_str = ""
	with open ("urlfiles/ebay-urlfile.txt", 'w') as file:
		for i in array:
			w_str = "{}\n{}".format(w_str, i)
		file.write(w_str)

def scrapeItemName(html):
	b = BeautifulSoup(html.text, 'lxml')
	itemName = b.find("div", { 'id':'CenterPanelInternal' })
	return itemName.find('h1').find('span').next_sibling

def scrapeItemPrice(html):
	b = BeautifulSoup(html.text, 'lxml')
	itemPrice = b.find('span', {'id':'prcIsum'}).text

	itemPrice = itemPrice.replace("PHP", "").replace(",","")
	return itemPrice.strip()

def scrapeItemImageURL(main_div):
	imgURL = main_div.find('img',{'id':'icImg'})['src']
	return imgURL

def scrapeImage(html):
	b = BeautifulSoup(html.text, 'lxml')
	main_div = b.find("div", { 'id':'CenterPanelInternal' })

	if not os.path.exists('images'):
		os.makedirs('images')

	image_url = scrapeItemImageURL(main_div)
	image_file = 'images/{}.jpg'.format(uniqid())

	try:
		urllib.request.urlretrieve(image_url, image_file)
	except urllib.error.HTTPError as e:
		try:
			image_file = 'images/{}.png'.format(uniqid())
			urllib.request.urlretrieve(image_url, image_file)
		except urllib.error.HTTPError as ex:	
			print(image_url)

	return image_file

def uniqid():
    from time import time
    return hex(int(time()*10000000))[2:]

def gatherURL(url, array):
	try:
		b = BeautifulSoup(requests.get(url).text, 'lxml')
	except:
		return array

	prod_list = b.find('ul', {'class':'b-list__items_nofooter'})

	end = True

	for items in prod_list.find_all('div', {'class':'s-item__wrapper'}):
		array.append(items.find('a',{'class':'s-item__link'})['href'])
		end = False

	if end == True: return array

	try:

		cur_page = b.find('li', {'class':'ebayui-pagination__li--selected'})
		next_page = cur_page.find_next_sibling('li')
		next_url = next_page.find('a')['href']
	except Exception as e:
		return array

	return gatherURL(next_url, array)	

# s = gatherURL("https://www.ebay.ph/b/Laptops-Netbooks/175672/bn_1648276", array)
# write_to_csv(s)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
	    '--url',
	    type=str,
	    default='https://www.ebay.ph/b/Laptops-Netbooks/175672/bn_1648276',
	)
	parser.add_argument(
		'--category',
		type=str,
		default='NULL'
	)
	parser.add_argument(
		'--run',
		type=str,
		default='gatherURL',
		help='gatherURL or scrapeURL'
	)

	FLAGS, unparsed = parser.parse_known_args()
	array = []
	if FLAGS.run == 'gatherURL':
		s = gatherURL(FLAGS.url, array)
		write_to_csv(s)

	with open ("urlfiles/ebay-urlfile.txt", "r") as file, open("csv_data/ebay-data.csv","a") as out_file:
		for line in file:
			url = file.readline()
			print(url)
			try:
				html = requests.get(url)
				name = scrapeItemName(html)
				price = scrapeItemPrice(html)
				imgPath = scrapeImage(html)

				arr = [url, name, price, imgPath]
				print(arr)

				writer = csv.writer(out_file, delimiter = ',', lineterminator='\n')
				writer.writerow(arr)
			except requests.exceptions.MissingSchema as e:
				print("Missing URL")
				pass
			except AttributeError as ex:
				pass

			

