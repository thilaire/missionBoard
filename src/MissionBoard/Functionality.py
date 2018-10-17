# coding=utf-8

from operator import itemgetter
import logging
from threading import Thread
from time import time
from queue import Queue, Empty
from re import compile

# import UX elements (Leds, Buttons, Switches, etc.)
from MissionBoard.Element import Element

from MissionBoard.LED import LED
from MissionBoard.Display import DISP, LVL
from MissionBoard.PushButton import PB
from MissionBoard.RGB import RGB
from MissionBoard.Switches import SW2, SW3
from MissionBoard.POT import POT


# dictionary of possible elements
dictOfElements = {'LED': LED, 'DISP': DISP, 'PB': PB, 'RGB': RGB, 'SW2': SW2, 'SW3': SW3, 'POT': POT, 'LVL': LVL}

# simple regex for Pxx_YYY_zzz or Pxx_YYY where P is `T` or `B`

regElement = compile("[TB](\d+)_([A-Z0-9]+)(_([A-Za-z0-9]+))?")


logger = logging.getLogger()


class Functionality:
	"""Threaded loop to manage queue and worker function"""

	def __init__(self, EM):
		self._queue = Queue()           # queue of event
		self.EM = EM                   # event manager
		self._timers = {}               # dictionary: timerName -> duration (in seconds)
		self._lastEventTime = 0         # time of the last event

	def isReadyToStart(self):
		"""method called to wait for all the loops to be ready
		must be overloaded by inherited classes"""
		return False

	def onEvent(self, e):
		"""method called when an event (timer, button) occurs
		is overload by inherited class"""
		pass

	def notify(self, btn):
		"""Simply add the object in the Event Queue"""
		logger.debug("addEvent: btn=%s", str(btn))
		self._queue.put_nowait(btn)

	@property
	def name(self):
		return self.__class__.__name__

	def waitEvents(self):
		"""threaded loop that waits for the event in the queue
		 (or wait for some time), and then launch the function"""
		logger.debug("Launch waitEvent '%s'", self.name)
		# loop (wait for a button change or a timer)
		self._lastEventTime = time()
		while True:
			timer, timeout = self.minTimer()
			try:
				btn = self._queue.get(timeout=timeout)
				logger.debug("Receive '%s' in '%s' queue", str(btn), self.name)
				self._queue.task_done()  # useless, here
			except Empty:
				logger.debug("Timeout '%s' (%ds) in '%s' queue", timer, timeout, self.name)
				btn = timer
				del self._timers[timer]     # remove that timer
			# update the remaining timers (if some still exist)
			self.updateTimers()
			# call the fct with the button, or with the type of the delay event
			logger.info("Run `%s` event (because of %s", self.name, str(btn) if isinstance(btn, Element) else "Timer "+btn)
			self.onEvent(btn)
			# check if we move to another state
			self.EM.manageState(self)

	def run(self):
		"""run the threaded loop """
		logger.info("Start the functionality %s", self.name)
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
		# if name in self._timers:
		#   raise ValueError("A timer with the same name ('%s') already exist in %s", name, self.onEvent.__name__)
		# -> if the timer already exists, its duration is replaced
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
		# create the element and add it as an attribute to the class, and to the ATBridge
		element = dictOfElements[elementType](keyname, name, **args)
		setattr(self.__class__, name, element)
		setattr(self.EM.__class__, type(self).__name__+'_'+name, element)
		logger.info("Element `%s` (%s) is added to %s", keyname, name, type(self).__name__)

