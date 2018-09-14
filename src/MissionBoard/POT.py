# coding=utf-8

from MissionBoard.Element import Element


class POT(Element):
	"""
	Potentiometers
	"""

	_all = {}   # list of potentiometers

	def __init__(self, keyname, name, index, event=None):
		# init super class
		super(POT, self).__init__(keyname, name, event)
		# register in the dictionnary of switches
		self._all[index] = self
		self._index = index
		self._value = 0



	@classmethod
	def checkChanges(cls, index, value):
		"""Check which potentiometer has changed, and notify it"""
		# get the concerned potentiometer
		try:
			Pot = cls._all[index]
		except KeyError:
			print("INDEX="+str(index))
			return  # TODO: should not happen, do something ? Remove the try/except ?
		# assign its new value
		Pot._value = value
		# notify the Potentiometer that its value changes
		Pot.notify()


	@property
	def value(self):
		return self._value
