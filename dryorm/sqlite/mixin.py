import sqlite3
from settings import settings
from dryorm.mixin import Mixin

class SqliteMixin(Mixin):
	_param_placeholder = '?'
	_connection = None	
	@staticmethod
	def connect():
		if not SqliteMixin._connection:
			SqliteMixin._connection = sqlite3.connect(settings['METADATA'])
			print settings['METADATA']
		return SqliteMixin._connection

	@property
	def connection(self):
		if not self._connection:
			self._connection = SqliteMixin.connect()
		return self._connection

	