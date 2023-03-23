import os

class Config:
	PSQL_USER_NAME = 'postgres'
	PSQL_USER_PASSWORD = 'postgres'
	PSQL_DATABASE = 'work'
	PSQL_HOST = 'localhost'
	PSQL_PORT = '5432'

class Development(Config):
	pass

class Testing(Config):
	pass

class Production(Config):
	pass

config = {
	'development': Development,
	'testing': Testing,
	'production': Production,

	'default': Development
}
