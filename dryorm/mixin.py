
class Mixin(object):
	_connection = None	
	_pk = 'id'
	@staticmethod
	def connect():
		raise NotImplementedError()

	@property
	def connection(self):
		raise NotImplementedError()

	@classmethod
	def adjust_params(cls,params):
		return cls._adjust_params(params)
	
	@staticmethod
	def _adjust_params(params):
		return params

	def delete(self):
		if self._pk:
			'Delete from {} where {} = {}'.format(self.table, self._pk, self._param_placeholder)
			self.exec_and_commit(query, [getattr(self, self._pk)])
		else:
			raise NotImplementedError('Still cant delete without _pk defined')

	def save(self):
		if not self.is_dirty():
			return 
		if self._pk:
			query = 'Update {} set {} where {} = ' + self._param_placeholder
			setstr = ','.join(['{} = {}'.format(field, self._param_placeholder) for field in self.is_dirty()])
			query = query.format(self.table, setstr, self._pk)
			params = [getattr(self, field) for field in self.is_dirty()]
			params.append(getattr(self, self._pk))
			self.exec_and_commit(query,params)
			self.clean()
		else:
			raise NotImplementedError('Still cant save without _pk defined')
	
	def exec_and_commit(self,query,params):
		return Mixin._exec_and_commit(self.connection, query, params)

	@classmethod
	def sexec_and_commit(cls,query,params):
		return Mixin._exec_and_commit(cls.connect(), query, params)

	@staticmethod
	def _exec_and_commit(connection, query, params):
		cursor = connection.cursor()
		cursor.execute(query,Mixin.adjust_params(params))
		cursor.close()
		connection.commit()

	@classmethod
	def sinsert(cls,query,params):
		return Mixin._insert(cls.connect(), query, params)

	@staticmethod
	def _insert(connection, query, params):
		cursor = connection.cursor()
		cursor.execute(query,Mixin.adjust_params(params))
		rowid = cursor.lastrowid
		cursor.close()
		connection.commit()
		return rowid

	def fetch_one(self,query,params):
		return Mixin._get_one(self.connection, query, params)

	@classmethod
	def sfetch_one(cls,query,params):
		return Mixin._get_one(cls.connect(), query, params)

	@staticmethod
	def _get_one(connection, query, params):
		cursor = connection.cursor()
		cursor.execute(query,Mixin.adjust_params(params))
		row = cursor.fetchone()
		if row:
			cursor.close()
			return row
		else:
			return None
	
	def fetch_all(self,query,params):
		return Mixin._get_all(self.connection, query, params)
		
	@classmethod
	def sfetch_all(cls,query,params=[]):
		return Mixin._get_all(cls.connect(), query, params)

	@staticmethod
	def _get_all(connection, query, params):
		cursor = connection.cursor()
		cursor.execute(query,Mixin.adjust_params(params))
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
		key = None
		if not args and not kwargs:
			print "No args"
			raise Exception("No args")
		if not kwargs:
			query = query.format(cls.table, ",".join(cls.fields), ",".join([cls._param_placeholder]*len(cls.fields)))
			my_args = list(args)
			if cls._pk in cls.fields:
				key = my_args[cls.fields.index(cls.pk)]
		else:
			query = query.format(cls.table, ",".join(kwargs.keys()), ",".join([cls._param_placeholder]*len(kwargs.keys())))
			my_args = list(kwargs.values())
			if cls._pk in kwargs:
				key = kwargs[cls._pk]
		print query, my_args
		id = cls.sinsert(query,my_args)
		if key:
			return cls.get_by_id(key)
		return cls.get_by_id(id)
