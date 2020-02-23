from bs4 import BeautifulSoup
import requests
import argparse
import os
import random
import urllib.request
import csv

data = requests.get("https://goods.ph")
b = BeautifulSoup(data.text, 'lxml')

def scrapeItemName(html):
	b = BeautifulSoup(html.text, 'lxml')
	itemName = b.find("div", { 'class':'product-title' })
	return itemName.find('h1').text.strip()

def scrapeItemPrice(html):
	b = BeautifulSoup(html.text, 'lxml')
	itemPrice = b.find('span', {'class':'price01'})
	itemPrice = itemPrice.text.strip().replace("\u20b1","")

	return itemPrice.replace(",","") 

def scrapeItemImageURL(html):
	b = BeautifulSoup(html.text, 'lxml')
	itemImage = b.find('img', {'class':'spic'})['src']

	return itemImage

def scrapeImage(html):
	if not os.path.exists('images'):
		os.makedirs('images')

	image_url = scrapeItemImageURL(html)
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

	root = "https://www.goods.ph"
	end = True

	prod_list = b.find('div', {'class':'product-list'})
	for item in prod_list.find_all('div', {'class':'item'}):
		array.append("{}{}".format(root, item.find('a')['href']))
		end = False

	if end == True:
		return array

	cur_page = b.find('a',{'class':'cur'})
	next_page = cur_page.find_next_sibling('a')
	next_url = "{}{}".format(root, next_page['href'])

	return gatherURL(next_url, array)

def write_to_csv(array):
	w_str = ""
	with open ("urlfile.txt", 'w') as file:
		for i in array:
			w_str = "{}\n{}".format(w_str, i)
		file.write(w_str)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
	    '--url',
	    type=str,
	    default='https://www.goods.ph/category/online-shopping-mobiles-161.html',
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

	with open ("urlfile.txt", "r") as file, open("goods-data.csv","a") as out_file:
		for line in file:
			url = file.readline()
			print(url)
			try:
				html = requests.get(url)
				name = scrapeItemName(html)
				price = scrapeItemPrice(html)
				imgPath = scrapeImage(html)
			except requests.exceptions.MissingSchema as e:
				print("Missing URL")
				pass

			arr = [url, name, price, imgPath]
			print(arr)

			writer = csv.writer(out_file, delimiter = ',', lineterminator='\n')
			writer.writerow(arr)


