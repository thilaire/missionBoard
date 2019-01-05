# coding=utf-8


import logging
logger = logging.getLogger("State")


class State:
	"""define a state (of the system)
	The system can change its current state, when certain condition occurs
	a state is a singleton of a class that inherits from States and implement some methods"""

	funcNext = []       # list of functionalities that can make pass to the next state

	def __init__(self, EM):
		self.name = self.__class__.__name__
		self.EM = EM

	def init(self):
		"""actions to perform when the state is activated
		To be inherited"""
		pass

	def isOver(self, func):
		"""define if we can move to the next state
		returns True or False
		To be inherited"""
		return False

	def __eq__(self, other):
		"""Compare a state with a string (is it its name?)"""
		return other == self.name


class Init(State):
	"""State that wait that all the buttons are correctly initialized"""
	def __init__(self, EM):
		"""Build the state
		keep a boolean for each functionality (is this functionality ready?)
		-> can go to the next state when all are ready"""
		# build the State
		super(Init, self).__init__(EM)
		# dictionary that associate a boolean for each functionality
		self._ready = {func: func.isReadyToStart() for func in EM.functionalities}


	def isOver(self, func):
		"""update the boolean for the functionality
		the state is over when all the functionalities are ready to start"""
		ready = func.isReadyToStart()
		self._ready[func] = ready
		logger.info("Not Ready: " + ", ".join(f.__class__.__name__ for f, b in self._ready.items() if not b))
		# return True if all the functionalities are ready
		if ready:
			return all(self._ready.values())
		else:
			return False
