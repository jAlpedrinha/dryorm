from settings import settings
print settings

print 'db' in settings


db = settings['db']

if db == "sqlite":
	from sqlite import SqliteModel as Model
	
	
elif db == "psql":
	from psql import PsqlModel as Model
