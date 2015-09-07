
class BaseModel(object):
	def __init__(self, *args):
		self.__is_dirty = []
		self.__dict = {}
		for key, value in zip(self.fields, args):
			setattr(self, key, value)

	def __setattr__(self, name, value):
		if not '__' in name:
			if name in self.__dict and value != self.__dict[name]:
				if not name in self.__is_dirty:
					self.__is_dirty.append(name)			
			self.__dict[name] = value
		super(BaseModel, self).__setattr__(name, value)

	
	def clean(self):
		self.__is_dirty = []
		
	def is_dirty(self):
		return self.__is_dirty

	@classmethod
	def get_by_id(cls, id):
		if self._pk:
			'SELECT *  from {} where {} = {}'.format(self.table, self._pk, self._param_placeholder)
			row = self.sfetch_one(query, [getattr(self, self._pk)])
			return cls(*row)
		else:
			raise NotImplementedError('Still cant get_by_id without _pk defined')


