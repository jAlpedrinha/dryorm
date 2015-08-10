from settings import settings
import psycopg2
from dryorm.mixin import Mixin
class PsqlMixin(Mixin):
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

	@staticmethod
	def _adjust_params(params):
		return tuple(params)
		