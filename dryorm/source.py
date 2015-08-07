


class SourceDao(object):
	
	def get_notifications(self, source_id, old_max, instance_id):
		raise NotImplementedError()

	def truncate_or_create(self, name, ddl):
		raise NotImplementedError()

	def extract_source(source_id, table_name, control_field, minimum, maximum= None):
		raise NotImplementedError()
