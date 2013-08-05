import sqlite3
import os
import time

OUTPUT_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = "example.db"
class Database(object):
	__shared_state = {} #Borg design pattern, shared state
	def __init__(self):
		self.__dict__ = self.__shared_state
		self.filename = os.path.join(OUTPUT_ROOT, OUTPUT_FILE)
		if not os.path.isfile(self.filename):
			self.createDatabase(self.filename)
		else:
			self._db = sqlite3.connect(self.filename)
			self._db.row_factory = sqlite3.Row
			self.cursor = self._db.cursor()
	def createDatabase(self, filename):
		print 'Creating Database in', self.filename
		self._db = sqlite3.connect(self.filename)
		self._db.row_factory = sqlite3.Row
		self.cursor = self._db.cursor()
		#build database
		self.cursor.executescript("""
			--database schema

			CREATE TABLE IF NOT EXISTS mytable (
				field1 TEXT,
				field2 INTEGER
			);
		""")
		self.commit()
	
	def execute(self, sql, *params):
		return self.cursor.execute(sql, params)
	def fetchone(self):
		return self.cursor.fetchone()
	def fetchall(self):
		return self.cursor.fetchall()
	def lastrowid(self):
		return self.cursor.lastrowid
	def commit(self):
		self._db.commit()
	def close(self):
		self.commit()
		self._db.close()
db = Database() #single instance

def getDbFilename():
	return db.filename

def commit():
	db.commit()

def close():
	db.close() 

def main():
	pass
if __name__ == '__main__':
	main()