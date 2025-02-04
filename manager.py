from asyncio import Queue
from threading import Lock
from typing import Dict, Tuple
import asyncio

from client import Client 

class ClientManager():
	"""	A class to manage the clients. It should be used in a setting 
		where multiple clients are connected to the server. It is a singleton
		so that the clients can be accessed from anywhere in the code.
	"""
	_clients : Dict[str,Client] = {}
	_lock : Lock = Lock()
	_instance = None
	_dict_lock : Lock = Lock()
	_client_queue : Queue = Queue()
	
	def __init__(self):
		self._eventloop = asyncio.new_event_loop()
		self._eventloop.call_soon(self._run)

	def __call__(self, **_):
		with self._lock:
			if self._instance is None:
				_instance = self.__init__()
			return _instance
	
	def add_client(self, client_id_tuple : Tuple[str, Client]):
		self._client_queue.put(client_id_tuple)

	def remove_client(self, id):
		try:
			client = self._clients.pop(id)
			client.stop()
		except KeyError:
			pass

	def get_client(self, id) -> Client | None:
		return self._clients.get(id)

	def stop(self):
		self._eventloop.stop()

	def run(self):
		self._eventloop.run_forever()

	async def _run(self):
		# Run trough the queue, add the clients to the clients dict and start them
		while not self._client_queue.empty():
			client_id, client = await self._client_queue.get()
			self._clients[client_id] = client
			asyncio.create_task(client.run())
		await asyncio.sleep(0.1)	