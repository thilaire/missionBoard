# coding=utf-8

import logging
from MissionBoard.ATBridge import ATBridge
from MissionBoard.State import Init

logger = logging.getLogger()


class EventManager(ATBridge):
	"""Main Class to deal with the different loops, queue, state and bridge with the AT tiny"""
	def __init__(self, loops, states):
		"""Create the main object"""
		super(EventManager, self).__init__()
		# create the different loops (on object per class given), store them as attribute
		self.functionalities = []
		for cls in loops:
			func = cls(self)
			self.functionalities.append(func)
			setattr(self.__class__, cls.__name__, func)
		# store the states
		self._states = [s(self) for s in states]
		self.state = self._states[0]
		self.isInitState = isinstance(self.state, Init)     # True if we start with Init State
		self._currentState = 0


	@property
	def stateName(self):
		"""return current state name"""
		return self.state.name


	def nextState(self):
		"""change to the next state"""
		# increase the state
		prevState = self.state.name
		self._currentState += 1
		try:
			self.state = self._states[self._currentState]
			self.isInitState = isinstance(self.state, Init)  # True if we start with Init State
		except IndexError:
			raise ValueError("Cannot go to next state")
		logger.debug("We move from '%s' state to '%s' state", prevState, self.state.name)
		# update the displays
		self.state.init()


	def manageState(self, func):
		"""check if we need to move to another state"""
		logger.debug("State=%s", self.stateName)
		if self.isInitState or func.__class__ in self.state.funcNext:
			# we need to check
			if self.state.isOver(func):
				self.nextState()


	def start(self):
		"""fct to be overloaded
		will be run when everything is ready"""
		pass


	def run(self):
		"""run the loops, the start method and they the (endless) SPI loop"""
		# run the loops (one per thread)
		[l.run() for l in self.functionalities]
		# start the object
		self.start()
		# and run the SPI loop
		self.runSPI()
