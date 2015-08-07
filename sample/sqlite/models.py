from dryorm import Model
from datetime import datetime


class SqliteSources(Model):
	table = "sources"
	fields = ['id','path','ctl_field','auto_source','nrows','min','max','instance_id','transform_script'
		,'load_script','extract_script','ddl']

	def delete(self):
		raise NotImplementedError()
	
	def update_source(self):
		current_query = "SELECT min,max from sources where id= ?"
		update_query = 'UPDATE sources set max = ?, min = ? where id = ?'
		# old_min, old_max = self.fetch_one(current_query,[self.id])
		# if minimum and old_min and minimum > old_min:
		# 	minimum = old_min
		# if maximum and old_max and maximum < old_max:
		# 	maximum = old_max
		# self.exec_and_commit(update_query,[maximum, minimum,self.id])

	@classmethod
	def get_sources(cls, auto_sources = None):
		query = """SELECT *
			from sources"""
		if auto_sources:
			query += " where auto_source = ?"
		print query
		rows = cls.sfetch_all(query, [auto_sources])
		if rows:
			return [cls(*row) for row in rows]
		return []

	@classmethod
	def get_by_id(cls, id):
		row = cls.sfetch_one("SELECT * from {} where id = ?".format(cls.table), [id])
		return cls(*row)


class SqliteVersion(Model):
	table = 'versions'

	def __init__(self,*args, **kwargs):
		super(SqliteVersion, self).__init__(*args,**kwargs)
		self.enabled = bool(self.enabled)

	def get_old_checkpoint(self):
		if self.checkpoint and self.checkpoint != self.initial_checkpoint:
			return self.checkpoint

	def get_files(self):
		query = """
			select staging_file_id
			from version_sources
			where version_id = ?
		"""
		rows = self.fetch_all(query, [self.id])
		if rows:
			return rows
		return []

	def delete(self):
		query = """Delete from versions where id = ?"""
		self.exec_and_commit(query, [self.id])

	@classmethod
	def get_by_id(cls, id):		
		row = cls.sfetch_one("""SELECT * from versions where id = ?""", [id])
		return cls(*row)



class SqliteConfigs(Model):
	table = "configs"
	fields = ['id', 'name', 'value','type']

	@classmethod
	def create(cls,name, value, _type=None):
		query = """
			INSERT INTO {} (name,value,type)
			VALUES (?, ? ,?, ?)"""

		if not _type:
			_type = type(value)

		query = query.format(cls.table)
		id = cls.sinsert(query,[name, value, _type])
		return cls.get_by_id(id)
	
	@classmethod
	def get_all(cls):	
		rows = cls.sfetch_all("SELECT * from {} ".format(cls.table))
		if rows:
			return [cls(*row) for row in rows]
		return []

	@classmethod
	def get_by_name(cls, name):	
		row = cls.sfetch_one("SELECT * from {} where name = ?".format(cls.table), [name])
		return cls(*row)

	@classmethod
	def get_by_id(cls, id):	
		row = cls.sfetch_one("SELECT * from {} where id = ?".format(cls.table), [id])
		return cls(*row)

