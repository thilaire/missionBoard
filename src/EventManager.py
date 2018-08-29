# coding=utf-8


import logging
import threading
from queue import Queue

logger = logging.getLogger()




class EventManager:
	"""Encompass queue and worker function
	TODO: maybe not necessary to put it in one class..."""
	_listOfEvents = []

	def __init__(self, fct):
		self._queue = Queue()
		self._fct = fct
		self._listOfEvents.append(self)


	def waitEvent(self):
		logger.debug("Launch waitEvent %s", self._fct.__name__)
		while True:
			btn = self._queue.get()
			logger.debug("Receive '%s' in '%s' queue", str(btn), self._fct.__name__)
			self._fct(btn)
			self._queue.task_done()     # useless, here


	def notify(self, btn):
		"""Simply add the object in the Event Queue
		the put_nowait is done in the same thread as the loop with call_soon_threadsafe
		addEvent is called by a RPi.GIPIO callback, that is in another thread, see
		https://raspberrypi.stackexchange.com/questions/54514/implement-a-gpio-function-with-a-callback-calling-a-asyncio-method
		and
		https://stackoverflow.com/questions/32889527/is-there-a-way-to-use-asyncio-queue-in-multiple-threads
		"""
		logger.debug("addEvent: btn=%s", str(btn))
		self._queue.put_nowait(btn)


	@classmethod
	def runAll(cls):
		threads = [threading.Thread(target=e.runLoop, daemon=True) for e in cls._listOfEvents]
		[t.start() for t in threads]

