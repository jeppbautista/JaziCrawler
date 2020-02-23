

class Brand():

	def __init__(self):
		self._brandID = None
		self._brandName = None
		self._brandCode = None

	@property
	def brandID(self):
		return self._brandID

	@brandID.setter
	def brandID(self, value):
		self._brandID = value

	@property
	def brandName(self):
		return self._brandName

	@brandName.setter
	def brandName(self, value):
		self._brandName = value

	@property
	def brandCode(self):
		return self._brandCode

	@brandCode.setter
	def brandCode(self, value):
		self._brandCode = value