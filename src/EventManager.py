# coding=utf-8

import asyncio
import logging
import threading

logger = logging.getLogger()

class EventManager:
	_listOfEvents = []

	def __init__(self, fct):
		self._loop = asyncio.new_event_loop()
		asyncio.set_event_loop(self._loop)
		self._queue = asyncio.Queue(loop=self._loop)
		self._fct = fct
		self._listOfEvents.append(self)


	def runLoop(self):
		"""run the asyncio loop associated"""
		self._loop.run_until_complete(self._proceedQueue())
		# should never happened
		self._loop.close()


	async def _proceedQueue(self):
		logger.debug("Launch _proceedQueue %s", self._fct.__name__)
		while True:
			btn = await self._queue.get()
			logger.debug("Receive '%s' in '%s' queue", str(btn), self._fct.__name__)
			self._fct(btn)


	def notify(self, btn):
		"""Simply add the object in the Event Queue
		the put_nowait is done in the same thread as the loop with call_soon_threadsafe
		addEvent is called by a RPi.GIPIO callback, that is in another thread, see
		https://raspberrypi.stackexchange.com/questions/54514/implement-a-gpio-function-with-a-callback-calling-a-asyncio-method
		and
		https://stackoverflow.com/questions/32889527/is-there-a-way-to-use-asyncio-queue-in-multiple-threads
		"""
		logger.debug("addEvent: btn=%s", str(btn))
		self._loop.call_soon_threadsafe(self._queue.put_nowait(btn))


	@classmethod
	def runAll(cls):
		threads = [threading.Thread(target=e.runLoop, daemon=True) for e in cls._listOfEvents]
		[t.start() for t in threads]

