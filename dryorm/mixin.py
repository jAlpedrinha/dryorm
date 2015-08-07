
class Mixin(object):
	_connection = None	
	@staticmethod
	def connect():
		raise NotImplementedError()

	@property
	def connection(self):
		raise NotImplementedError()

	def save(self):
		raise NotImplementedError()
	
	def exec_and_commit(self,query,params):
		raise NotImplementedError()

	@classmethod
	def sexec_and_commit(cls,query,params):
		raise NotImplementedError()

	@staticmethod
	def _exec_and_commit(connection, query, params):
		raise NotImplementedError()

	@classmethod
	def sinsert(cls,query,params):
		raise NotImplementedError()

	@staticmethod
	def _insert(connection, query, params):
		raise NotImplementedError()

	def fetch_one(self,query,params):
		raise NotImplementedError()

	@classmethod
	def sfetch_one(cls,query,params):
		raise NotImplementedError()

	@staticmethod
	def _get_one(connection, query, params):
		raise NotImplementedError()

	@classmethod
	def sfetch_all(cls,query,params=[]):
		raise NotImplementedError()

	@staticmethod
	def _get_all(connection, query, params):
		raise NotImplementedError()
