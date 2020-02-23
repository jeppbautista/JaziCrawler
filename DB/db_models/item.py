
class Item():

	def __init__(self):
		self._itemID = None
		self._itemName = None
		self._itemPrice = None
		self._url = None
		self._siteID = None
		self._site = None
		self._imagePath = None
		self._category = None
		self._brand = None

	@property
	def itemID(self):
		return self._itemID

	@itemID.setter
	def itemID(self, value):
		self._itemID = value

	@property
	def itemName(self):
		return self._itemName

	@itemName.setter
	def itemName(self, value):
		self._itemName = value

	@property
	def itemPrice(self):
		return self._itemPrice

	@itemPrice.setter
	def itemPrice(self, value):
		self._itemPrice = value

	@property
	def url(self):
		return self._url

	@url.setter
	def url(self, value):
		self._url = value

	@property
	def siteID(self):
		return self._siteID

	@siteID.setter
	def siteID(self, value):
		self._siteID = value

	@property
	def site(self):
		return self._site

	@site.setter
	def site(self, value):
		self._site = value

	@property
	def imagePath(self):
		return self._imagePath

	@imagePath.setter
	def imagePath(self, value):
		self._imagePath = value

	@property
	def category(self):
		return self._category

	@category.setter
	def category(self, value):
		self._category = value

	@property
	def brand(self):
		return self._brand

	@brand.setter
	def brand(self, value):
		self._brand = value