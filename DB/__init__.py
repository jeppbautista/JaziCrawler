
#TODO dao.py

# file = "../data/sss.txt"

# with open (file, "r") as f:
# 	for line in f:
# 		print(line)
import sqlite3
from db import Database
from dao import DAO
from db_models.item import Item
from db_models.brand import Brand
from db_models.category import Category

db = Database()
dao = DAO(db)

x = dao.retrieve_images_for('laptop')
print(x)
# item_ = Item()
# brand_ = Brand()
# category_ = Category()


# itemName = 'Iphone X'
# itemPrice = 70000.0

# url = 'https://lazada.com.ph/shop-mobiles/iphone/iphoneX'
# imagepath = '../data/category/brand/<itemID>.jpg'

# siteName = 'Lazada'

# brandName = 'apple'

# categoryName = 'mobile'
# categoryCode = 'shop-mobiles'

# item_.site = siteName
# item_.itemName = itemName
# item_.itemPrice = itemPrice
# item_.url = url
# item_.imagePath = imagepath
# item_.brand = brand_
# item_.category = category_

# brand_.brandName = brandName


# category_.catName = categoryName
# category_.catCode = categoryCode

# dao.insert_item(item=item_, brand=brand_, category=category_)

# db.__del__()