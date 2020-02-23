
class Category():

	def __init__(self):
		self._catID = None
		self._catName = None
		self._catCode = None

	@property
	def catID(self):
		return self._catID

	@catID.setter
	def catID(self, value):
		self._catID = value

	@property
	def catName(self):
		return self._catName

	@catName.setter
	def catName(self, value):
		self._catName = value

	@property
	def catCode(self):
		return self._catCode

	@catCode.setter
	def catCode(self, value):
		self._catCode = value