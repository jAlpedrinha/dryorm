
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
		raise NotImplementedError()

	def delete(self):
		raise NotImplementedError()

	@classmethod
	def get_by_id(cls, id):
		raise NotImplementedError()


# class Sources(Model):
# 	table = "sources"
# 	fields = ['id','path','ctl_field','auto_source','nrows','min','max','instance_id','transform_script'
# 		,'load_script','extract_script','ddl']

# 	def delete(self):
# 		raise NotImplementedError()

# 	@classmethod
# 	def get_by_id(cls, id):
# 		raise NotImplementedError()



# class SourceNotifications(Model):
# 	table = "source_notifications"
# 	fields = ['id','source_id','notification_key','period','staging_file']

# 	def delete(self):
# 		raise NotImplementedError()

# 	@classmethod
# 	def get_by_id(cls, id):
# 		raise NotImplementedError()


# class StagingFile(Model):
# 	table = 'staging_files'
# 	fields = ['id','source_id','filename','nrows','status','min','max','date','percentage','percentage_date']
# 	def delete(self):
# 		raise NotImplementedError()


# 	@classmethod
# 	def get_by_id(cls, id):
# 		raise NotImplementedError()


# class Version(Model):
# 	fields = ['id', "name", "uptime","enabled","checkpoint","initial_checkpoint",
# 		"host", "username","password","port","db", 'nodes','node_type','private_host','temporary', 'created_at', 
# 		'updated_at', 'public_host']

# 	def delete(self):
# 		raise NotImplementedError()

# 	def get_checkpoint(self):
# 		raise NotImplementedError()

# 	def get_initial_checkpoint(self):
# 		raise NotImplementedError()

# 	def get_export_tables(self):
# 		raise NotImplementedError()

# 	def get_files(self):
# 		raise NotImplementedError()
	
# 	def get_new_files(self):
# 		raise NotImplementedError()

# 	def update_new_files(self):
# 		raise NotImplementedError()
		
# 	@classmethod
# 	def get_by_id(cls, id):
# 		raise NotImplementedError()


# class Checkpoint(Model):
# 	fields= ['id', 'bucket', 'chdate']
	
# 	def delete(self):
# 		raise NotImplementedError()

# 	@classmethod
# 	def get_by_id(cls, id):
# 		raise NotImplementedError()
# 	@classmethod
# 	def get_by_identifier(cls, id):
# 		raise NotImplementedError()


# class ExportTable(Model):
# 	fields= ['id', 'version', 'name', 'script_import', 'ddl']
	
# 	@classmethod
# 	def get_by_id(cls, id):
# 		raise NotImplementedError()
	
# 	@classmethod
# 	def get_by_version(cls, id):
# 		raise NotImplementedError()


# class Configs(Model):
# 	table = "configs"
# 	fields = ['id', 'name', 'value','type']

# 	@classmethod
# 	def create(cls,sf_id, message,identation, level):
# 		raise NotImplementedError()

# class Action(Model):
# 	table = "actions"
# 	fields = ['id', 'type', 'action', 'date', 'status', 'user_id', 'ref_id']

# 	@classmethod
# 	def create(cls,_type,action,ref,user_id=0,status="INIT"):
# 		raise NotImplementedError()



# class Log(Model):
# 	table = "log"
# 	fields = ['id', 'action_id', 'date', 'message', 'level', 'identation']

# 	@classmethod
# 	def create(cls,action,message, level='INFO', identation= 0):
# 		raise NotImplementedError()
