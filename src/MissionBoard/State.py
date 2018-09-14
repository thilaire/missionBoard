# coding=utf-8


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

	def isOver(self):
		"""define if we can move to the next state
		returns True or False
		To be inherited"""
		return False

