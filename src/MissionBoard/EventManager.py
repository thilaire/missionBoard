# coding=utf-8

import logging
from MissionBoard.ATBridge import ATBridge

logger = logging.getLogger()


class EventManager(ATBridge):
	"""Main Class to deal with the different loops, queue, state and bridge with the AT tiny"""
	def __init__(self, loops, states):
		"""Create the main object"""
		super(EventManager, self).__init__()
		# create the different loops (on object per class given), store them as attribute
		self._loops = []
		for cls in loops:
			func = cls(self)
			self._loops.append(func)
			setattr(self.__class__, cls.__name__, func)
		# store the states
		self._states = [s(self) for s in states]
		self._currentState = 0


	@property
	def state(self):
		"""current state"""
		return self._states[self._currentState]


	def nextState(self):
		"""change to the next state"""
		# increase the state
		prevState = self.state.name
		self._currentState += 1
		if self._currentState >= len(self._states):
			raise ValueError("Cannot go to next state")
		logger.debug("We move from '%s' state to '%s' state", prevState, self.state.name)
		# update the displays
		self.state.init()


	def manageState(self, func):
		"""check if we need to move to another state"""
		if func.__class__ in self._states[self._currentState].funcNext:
			# we need to check
			if self.state.isOver():
				self.nextState()


	def start(self):
		"""fct to be overloaded
		will be run when everything is ready"""
		pass


	def run(self):
		"""run the loops, the start method and they the (endless) SPI loop"""
		# run the loops (one per thread)
		[l.run() for l in self._loops]
		# start the object
		self.start()
		# and run the SPI loop
		self.runSPI()
