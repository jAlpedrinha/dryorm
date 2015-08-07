from settings import settings
import psycopg2

class PsqlMixin(object):
	_param_placeholder = '%s'
	_connection = None	
	@staticmethod
	def connect():
		PsqlMixin._connection = psycopg2.connect(**settings['connection'])
		PsqlMixin._connection.autocommit = True
		return PsqlMixin._connection

	@property
	def connection(self):
		self._connection = PsqlMixin.connect()
		return self._connection

	def save(self):
		if not self.is_dirty():
			return 
		query = 'Update {} set {} where id = %s'
		setstr = ','.join(['{} = %s'.format(field) for field in self.is_dirty()])
		query = query.format(self.table, setstr)
		params = [getattr(self, field) for field in self.is_dirty()]
		params.append(self.id)
		self.exec_and_commit(query,params)
		self.clean()
	
	def exec_and_commit(self,query,params=[]):
		return PsqlMixin._exec_and_commit(self.connection, query, params)

	@classmethod
	def sexec_and_commit(cls,query,params=[]):
		return PsqlMixin._exec_and_commit(cls.connect(), query, params)

	@staticmethod
	def _exec_and_commit(connection, query, params):
		cursor = connection.cursor()
		cursor.execute(query,tuple(params))
		cursor.close()

	@classmethod
	def sinsert(cls,query,params=[]):
		return PsqlMixin._insert(cls.connect(), query, params)

	@staticmethod
	def _insert(connection, query, params):
		cursor = connection.cursor()
		query += " RETURNING id;"
		cursor.execute(query,params)
		rowid = cursor.fetchone()
		if rowid:
			rowid = rowid[0]
		cursor.close()
		return rowid

	def fetch_one(self,query,params=[]):
		return PsqlMixin._get_one(self.connection, query, params)

	@classmethod
	def sfetch_one(cls,query,params=[]):
		return PsqlMixin._get_one(cls.connect(), query, params)

	@staticmethod
	def _get_one(connection, query, params):
		cursor = connection.cursor()
		cursor.execute(query,tuple(params))
		row = cursor.fetchone()
		if row:
			cursor.close()
			return row
		else:
			return None
	
	def fetch_all(self,query,params=[]):
		return PsqlMixin._get_all(self.connection, query, params)
		
	@classmethod
	def sfetch_all(cls,query,params=[]):
		return PsqlMixin._get_all(cls.connect(), query, params)

	@staticmethod
	def _get_all(connection, query, params):
		cursor = connection.cursor()
		cursor.execute(query,tuple(params))
		rows = cursor.fetchall()
		if rows:
			cursor.close()
			return rows
		else:
			return []

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
		id = cls.sinsert(query,my_args)
		return cls.get_by_id(id)