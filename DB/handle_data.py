import os
from os import path
from os import listdir
from os.path import isfile, join
import imp
import sys
import csv
from ast import literal_eval


from db import Database
from dao import DAO
from db_models.item import Item
from db_models.brand import Brand
from db_models.category import Category

CATEGORY = 1
LOGO = 0

def get_highest_value(d1):  
    v=list(d1.values())
    k=list(d1.keys())
    return k[v.index(max(v))]

def classify(imgPath, mode):
	imgPath = os.path.realpath("../JaziCrawler/spiders/{}".format(imgPath))
	classifier_path = os.path.realpath(".../classifier/label_image.py")

	test = imp.load_source("label_image", classifier_path)
	if mode == CATEGORY:
		dictionary = literal_eval(test.run(imgPath))
	elif mode == LOGO:
		dictionary = literal_eval(test.run(imgPath, model='logo'))

	return get_highest_value(dictionary)



# mypath = os.path.realpath('../JaziCrawler/spiders/images/')
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# for image in onlyfiles:
# 	print(image)

# cat = classify('D:/Jazi/classifier/training/laptop/DE599ELAA4GLTMANPH-9590535.jpg', CATEGORY)
# #logo = classify('D:/Jazi/classifier/training/laptop/DE599ELAA4GLTMANPH-9590535.jpg', LOGO)

# print(cat)

def insert_csv_to_db(csvfile, siteName='Ebay'):
	db = Database()
	dao = DAO(db)

	item_ = Item()
	brand_ = Brand()
	category_ = Category()

	with open(csvfile, 'r') as file:
		f = csv.reader(file,delimiter = ',')
		for row in f:
			try:

				item_.category = classify(item_.imagePath, CATEGORY)
				if item_.category is None:
					raise ValueError("Category cannot be Null")

				item_.site = siteName
				item_.itemName = row[1]
				item_.itemPrice = row[2]
				item_.url = row[0]
				item_.imagePath = row[3]
				item_.brand = 'NULL'
				brand_.brandName = 'NULL'

				category_.catName = item_.category
				category_.catCode = ''

				dao.insert_item(item=item_, brand=brand_, category=category_)
			except Exception as e:
				print("Error{}".format(e) )
				pass
			

if __name__ == "__main__":

	insert_csv_to_db(os.path.realpath("../JaziCrawler/spiders/csv_data/ebay-data.csv"))