import sqlite3

class DAO():

	def __init__(self, db):
		self.db = db._db_connection_
		self.cursor = db._cursor_
		self.script = ""
		self.item_model = None
		self.category_model = None
		self.brand_model = None

	def insert_item(self, **kwargs):
		item_model = kwargs['item']
		cat_model = kwargs['category']
		brand_model = kwargs['brand']

		self.insert_itemDetails(item=item_model)
		item_model.siteID = self.retrieve_ID(table='Site_List', column='siteName', where=item_model.site)
		item_model.itemID = self.retrieve_ID(table='Item_Details', column='ItemName', where=item_model.itemName)
		cat_model.catID = self.retrieve_ID(table='Category_List', column='CategoryName', where=cat_model.catName)
		brand_model.brandID = self.retrieve_ID(table='Brand_List', column='BrandName', where=brand_model.brandName)
		self.insert_linking_table(item=item_model, brand=brand_model, category=cat_model)
		self.insert_siteData(item=item_model)


	def insert_itemDetails(self, **kwargs):
		model = kwargs['item']
		self.script = "INSERT INTO Item_Details (itemName, itemPrice) VALUES ( ?, ?)"
		self.cursor.execute(self.script, (model.itemName, model.itemPrice))
		self.db.commit()
		self.log('Successfully Inserted to Item_Details')
		return self.current_id()


	def insert_linking_table(self, **kwargs):
		item_model = kwargs['item']
		cat_model = kwargs['category']
		brand_model = kwargs['brand']

		self.script = "INSERT INTO item_cat_brand (itemID, categoryID, brandID) VALUES (?, ?, ?)"
		self.cursor.execute(self.script, (item_model.itemID, cat_model.catID, brand_model.brandID))
		self.db.commit()
		self.log('Successfully Inserted to Item_Cat_Brand')

	def insert_siteData(self, **kwargs):
		item_model = kwargs['item']

		self.script = "INSERT INTO item_SiteData (itemID, url, siteID, imagePath) VALUES (?, ?, ?, ?)"
		self.cursor.execute(self.script, (item_model.itemID, item_model.url, item_model.siteID, item_model.imagePath))
		self.db.commit()
		self.log('Successfully Inserted to Item_SiteData')

	def retrieve_ID(self, **kwargs):
		table = kwargs['table']
		where = kwargs['where']
		col = kwargs['column']
		self.script = "SELECT * FROM {} WHERE {} = '{}' LIMIT 1"
		self.cursor.execute(self.script.format(table, col, where))
		ret = self.cursor.fetchall()
		return ret[0][0]

	def retrieve_images_for(self, category):
		self.script = "SELECT * FROM view_full_item WHERE categoryName = '{}'"
		self.cursor.execute(self.script.format(category))
		ret = self.cursor.fetchall()
		return ret
		
	def current_id(self):
		self.script = "SELECT last_insert_rowid()"
		self.cursor.execute(self.script)
		ret = self.cursor.fetchall()

	def log(self, msg):
		print("Database Log: ",msg)