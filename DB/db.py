import sqlite3

class Database():
	_db_connection_ = None
	_cursor_ = None

	def __init__(self):
		self._db_connection_ = sqlite3.connect('D:/Jazi/JaziCrawler/data/mydb')
		self._cursor_ = self._db_connection_.cursor()


	def __del__(self):
		self._db_connection_.close()
		print("Database Instance closed")

	@property
	def db_connection(self):
		return self._db_connection_

	@db_connection.setter
	def db_connection(self, value):
		self._db_connection_ = value

	@property
	def cursor(self):
		return self._cursor_

	@cursor.setter
	def cursor(self, value):
		self._cursor_ = value

def foobar():
	print("foo")