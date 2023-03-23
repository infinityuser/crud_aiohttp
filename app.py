from aiohttp import web
from aiohttp_session import setup
from aiohttp_session import SimpleCookieStorage

from config import config
import asyncpg

async def create_app(config_name):
	app = web.Application()
	app['config'] = config[config_name]
	setup(app, SimpleCookieStorage())

	app['db_conn'] = await asyncpg.connect(
		user=app['config'].PSQL_USER_NAME,
		password=app['config'].PSQL_USER_PASSWORD,
		database=app['config'].PSQL_DATABASE,
		host=app['config'].PSQL_HOST,
		port=app['config'].PSQL_PORT
	)

	from views.user import User
	app.router.add_view('/api/user', User)
	from calls.index import index
	app.router.add_get('/', index)
	return app

if __name__ == '__main__':
	web.run_app(create_app('default'))
