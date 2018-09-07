# coding=utf-8

from operator import itemgetter
import logging
from threading import Thread
from time import time
from queue import Queue, Empty
from re import compile

# import UX elements (Leds, Buttons, Switches, etc.)
from LED import LED
from Display import DISP, LVL
from PushButton import PB
from RGB import RGB
from Switches import SW2, SW3
from POT import POT

# dictionary of possible elements
dictOfElements = {'LED': LED, 'DISP': DISP, 'PB': PB, 'RGB': RGB, 'SW2': SW2, 'SW3': SW3, 'POT': POT, 'LVL': LVL}

# simple regex for Pxx_YYY_zzz or Pxx_YYY where P is `T` or `B`

regElement = compile("[TB](\d+)_([A-Z0-9]+)(_([A-Za-z0-9]+))?")


logger = logging.getLogger()


class ThreadedLoop:
	"""Threaded loop to manage queue and worker function"""

	def __init__(self, EM):
		self._queue = Queue()           # queue of event
		self.EM = EM                   # element manager
		self._timers = {}               # dictionary: timerName -> duration (in seconds)
		self._lastEventTime = 0         # time of the last event

	def onEvent(self, e):
		"""method called when an event (timer, button) occurs
		is overload by inherited class"""
		pass

	def notify(self, btn):
		"""Simply add the object in the Event Queue"""
		logger.debug("addEvent: btn=%s", str(btn))
		self._queue.put_nowait(btn)

	def waitEvents(self):
		"""threaded loop that waits for the event in the queue
		 (or wait for some time), and then launch the function"""
		logger.debug("Launch waitEvent '%s'", self.__class__.__name__)
		self._lastEventTime = time()
		while True:
			timer, timeout = self.minTimer()
			try:
				btn = self._queue.get(timeout=timeout)
				logger.debug("Receive '%s' in '%s' queue", str(btn), self.__class__.__name__)
				self._queue.task_done()  # useless, here
			except Empty:
				logger.debug("Timeout '%s' (%ds) in '%s' queue", timer, timeout, self.__class__.__name__)
				btn = timer
				del self._timers[timer]     # remove that timer
			# update the remaining timers (if some still exist)
			self.updateTimers()
			# call the fct with the button, or with the type of the delay event
			self.onEvent(btn)


	def run(self):
		"""run the threaded loop """
		t = Thread(target=self.waitEvents, daemon=True)
		t.start()


	def minTimer(self):
		"""compute the minimum time to wait (according to the timers)
		Returns None if there are no time"""
		return min(self._timers.items(), key=itemgetter(1)) if self._timers else (0, None)


	def updateTimers(self):
		"""update the timers (decrease the duration of all the timers)
		(most of the time, the dictionary of timers is empty)"""
		delta = time()-self._lastEventTime
		for timer in self._timers:
			self._timers[timer] -= delta
			if self._timers[timer] < 0:       # should not happen, except if two timers with same duration are launched
				self.onEvent(timer)
		self._lastEventTime = time()


	def runTimer(self, name, duration):
		"""add a timer (duration in seconds)"""
		if name in self._timers:
			raise ValueError("A timer with the same name ('%s') already exist in %s", name, self.onEvent.__name__)
		self._timers[name] = duration


	def add(self, keyname, name, **args):
		"""
		Declares a new element
		Parameters:
			- keyname: name following the IO convention (ie 'Px_yyy_zzz')
				-> the element type (LED, PB, etc.) is determined from the keyname
			- name: name of the element (used for the attribute)
			- args: arguments used to determine the elements (TMindex, etc.)
		"""
		# get the element Type
		m = regElement.search(keyname)
		if not m:
			raise ValueError("The keyname %s doesn't follow the pattern `Pxx_YYY_zzz` or `Pxx_YYY`", keyname)
		elementType = m.group(2)    # panel, elementType, number = m.group(1,2,4)
		if elementType not in dictOfElements:
			raise ValueError("The name of the element does not correspond to an existing type")
		# check if it's a switch that can send an event
		if elementType in ('SW2', 'SW3', 'POT', 'PB'):
			args['event'] = self
		# create the object and add it has an attribute
		# (of the class, we have a singleton here; and it's the way to do with Python)
		# check the name
		if hasattr(self, name) or hasattr(self.EM, type(self).__name__+'_'+name):
			print(name)
			print(type(self).__name__+'_'+name)
			raise ValueError("An element with the same name (%s) already exists", name)
		# create the element and add it as an attribute to the class, and to the ElementManager
		element = dictOfElements[elementType](keyname, name, **args)
		setattr(self.__class__, name, element)
		setattr(self.EM.__class__, type(self).__name__+'_'+name, element)
		logger.debug("Element `%s` (%s) is added to %s", keyname, name, type(self).__name__)

