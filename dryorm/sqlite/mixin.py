import sqlite3
from settings import settings


class SqliteMixin(object):
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

	def save(self):
		if not self.is_dirty():
			return 
		query = 'Update {} set {} where id = ?'
		setstr = ','.join(['{} = ?'.format(field) for field in self.is_dirty()])
		query = query.format(self.table, setstr)
		params = [getattr(self, field) for field in self.is_dirty()]
		params.append(self.id)
		self.exec_and_commit(query,params)
		self.clean()
	
	def exec_and_commit(self,query,params):
		return SqliteMixin._exec_and_commit(self.connection, query, params)

	@classmethod
	def sexec_and_commit(cls,query,params):
		return SqliteMixin._exec_and_commit(cls.connect(), query, params)

	@staticmethod
	def _exec_and_commit(connection, query, params):
		cursor = connection.cursor()
		cursor.execute(query,params)
		cursor.close()
		connection.commit()

	@classmethod
	def sinsert(cls,query,params):
		return SqliteMixin._insert(cls.connect(), query, params)

	@staticmethod
	def _insert(connection, query, params):
		cursor = connection.cursor()
		cursor.execute(query,params)
		rowid = cursor.lastrowid
		cursor.close()
		connection.commit()
		return rowid

	def fetch_one(self,query,params):
		return SqliteMixin._get_one(self.connection, query, params)

	@classmethod
	def sfetch_one(cls,query,params):
		return SqliteMixin._get_one(cls.connect(), query, params)

	@staticmethod
	def _get_one(connection, query, params):
		cursor = connection.cursor()
		cursor.execute(query,params)
		row = cursor.fetchone()
		if row:
			cursor.close()
			return row
		else:
			return None
	
	def fetch_all(self,query,params):
		return SqliteMixin._get_all(self.connection, query, params)
		
	@classmethod
	def sfetch_all(cls,query,params=[]):
		return SqliteMixin._get_all(cls.connect(), query, params)

	@staticmethod
	def _get_all(connection, query, params):
		cursor = connection.cursor()
		cursor.execute(query,params)
		rows = cursor.fetchall()
		if rows:
			cursor.close()
			return rows
		else:
			return None

	@classmethod
	def create(cls,*args, **kwargs):
		query = """
			INSERT INTO {} ({})
			VALUES ({})"""

		if not args and not kwargs:
			print "No args"
			raise Exception("No args")
		if not kwargs:
			query = query.format(cls.table, ",".join(cls.fields), ",".join(cls._param_placeholder*len(cls.fields)))
			my_args = list(args)
		else:
			query = query.format(cls.table, ",".join(kwargs.keys()), ",".join(cls._param_placeholder*len(kwargs.keys())))
			my_args = list(kwargs.values())
		print query, my_args
		id = cls.sinsert(query,my_args)
		return cls.get_by_id(id)