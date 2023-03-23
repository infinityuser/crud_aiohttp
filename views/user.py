from aiohttp import web

import json

def build_query(key, data):
	match key:
		case 'get':
			return 'select * from users where ' + \
				' and '.join([f"{i} = '{j}'" for i, j in data.items()])
		case 'post':
			return 'insert into users(' + \
				', '.join([f'{i}' for i in data.keys()]) + \
				') values(' + \
				', '.join([f"'{j}'" for j in data.values()]) + \
				')'
		case 'put':
			try:
				id = data.pop('id')
			except:
				raise 'NoIdSpecified'
			else:
				return 'update users set ' + \
					', '.join([f"{i} = '{j}'" for i, j in data.items()]) + \
					f' where id = {id}'
		case 'delete':
			return 'delete from users where ' + \
				' and '.join([f"{i} = '{j}'" for i, j in data.items()]) 
		case _:
			raise 'WrongMethod'

async def commit_query(conn, query):
	ret = await conn.execute(query)
	return {'code': 200, 'msg': ret}

class User(web.View):
	async def get(self):
		data = await self.request.json()
		query = build_query('get', data)
		ret = await self.request.app['db_conn'].fetchrow(query)
		ret = {'code': 200, 'msg': dict(ret) if ret != None else None}
		return web.json_response(ret)
	async def post(self):
		data = await self.request.json()
		query = build_query('post', data)
		return web.json_response(await commit_query(self.request.app['db_conn'], query))
	async def put(self):
		data = await self.request.json()
		query = build_query('put', data)
		return web.json_response(await commit_query(self.request.app['db_conn'], query))
	async def delete(self):
		data = await self.request.json()
		query = build_query('delete', data)
		return web.json_response(await commit_query(self.request.app['db_conn'], query))
