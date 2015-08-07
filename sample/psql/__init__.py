from dryorm import settings

local_settings = {
	'db' : 'psql',
	'host': '192.168.2.16',
	'user' : 'postgres',
	'password' : '',
	'port' : 5432,
	'database' : 'metadata'
}

print "Settings:" , settings.settings
settings.settings=local_settings

print settings.settings

myset = settings.settings