from dryorm import Model
from datetime import datetime

class PsqlSources(Model):
	table = "sources"
	fields = ['id','path','ctl_field','auto_source','nrows','min','max','instance_id','transform_script'
		,'load_script','extract_script','ddl']

	def delete(self):
		query = """Delete from {} where id = %s""".format(self.table)
		self.exec_and_commit(query, [self.id])
	
	def update_source(self):
		current_query = "SELECT min(min),max(max) from staging_files where source_id= %s"
		update_query = 'UPDATE sources set max = %s, min = %s where id = %s'
		minimum, maximum = self.fetch_one(current_query,[self.id])
		self.exec_and_commit(update_query,[maximum, minimum,self.id])

	def update_count(self):
		query = "Select sum(nrows),count(id) from staging_files where source_id = %s"
		row = self.fetch_one(query, [self.id])
		print "SUM", row
		count = 0
		if row:
			count= row[0]
		self.nrows= count
		self.save()


	@classmethod
	def get_sources(cls, auto_sources = None):
		query = """SELECT *
			from sources"""
		if auto_sources:
			query += " where auto_source = %s"
		rows = cls.sfetch_all(query, [auto_sources])
		if rows:
			return [cls(*row) for row in rows]
		return []

	@classmethod
	def get_by_id(cls, id):
		row = cls.sfetch_one("SELECT * from {} where id = %s".format(cls.table), [id])
		if row:
			return cls(*row)
		return None


class PsqlVersion(Model):
	table = 'versions'
	fields = ['id', "name", "uptime","enabled","checkpoint","initial_checkpoint",
			"host", "username","password","port","db", 'nodes','node_type','private_host','temporary', 'created_at', 
			'updated_at', 'public_host']
	def __init__(self,*args, **kwargs):
		super(PsqlVersion, self).__init__(*args,**kwargs)
		self.enabled = bool(self.enabled)

	def get_host(self):
		from conf import settings
		if 'publicly_accessible' not in settings()['redshift_create_cluster'] or settings()['redshift_create_cluster']['publicly_accessible']:
			return self.public_host
		else:
			return self.private_host
			
	def get_checkpoint(self):
		return PsqlCheckpoint.get_by_id(self.checkpoint)

	def get_initial_checkpoint(self):
		return PsqlCheckpoint.get_by_id(self.initial_checkpoint)

	def get_export_tables(self):
		return PsqlExportTable.get_by_version(self.id)

	def get_old_checkpoint(self):
		if self.checkpoint and self.checkpoint != self.initial_checkpoint:
			return self.checkpoint

	def update_version_snapshot(self, checkpoint):
		new_cp = PsqlCheckpoint.create(checkpoint)
		old = self.get_old_checkpoint()
		if old:
			old = PsqlCheckpoint.get_by_id(old)
			old.delete()
		if not self.initial_checkpoint:
			self.initial_checkpoint = new_cp.id
		self.checkpoint = new_cp.id
		self.save()

	def get_files(self):
		query = """
			select staging_file_id
			from version_sources
			where version_id = %s
		"""
		rows = self.fetch_all(query, [self.id])
		if rows:
			return rows
		return []

	def get_new_files(self):
		query = """
			select staging_file_id
			from version_sources
			where version_id = %s and is_new= true
		"""
		rows = self.fetch_all(query, [self.id])
		if rows:
			return rows
		return []

	def update_new_files(self):
		query = """
			update version_sources
			set is_new=false
			where version_id = %s and is_new= true
		"""
		self.exec_and_commit(query, [self.id])

	def delete(self):
		query = """Delete from versions where id = %s"""
		self.exec_and_commit(query, [self.id])


	@classmethod
	def get_all(cls):	
		rows = cls.sfetch_all("""SELECT * from versions""")
		if rows:
			return [cls(*row) for row in rows]
		return []

	@classmethod
	def get_by_id(cls, id):		
		row = cls.sfetch_one("""SELECT * from versions where id = %s""", [id])
		if row:
			return cls(*row)
		return None



class PsqlConfigs(Model):
	table = "configs"
	fields = ['id', 'name', 'value','type']

	@classmethod
	def create(cls,name, value, _type=None):
		query = """
			INSERT INTO {} (name,value,type)
			VALUES (%s, %s ,%s, %s)"""

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
		row = cls.sfetch_one("SELECT * from {} where name = %s".format(cls.table), [name])
		if row:
			return cls(*row)
		return None

	@classmethod
	def get_by_id(cls, id):	
		row = cls.sfetch_one("SELECT * from {} where id = %s".format(cls.table), [id])
		if row:
			return cls(*row)
		return None
