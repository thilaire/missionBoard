# coding=utf-8

from MissionBoard.Element import Element
import logging

# logger
logger = logging.getLogger()
SPIlogger = logging.getLogger('Element')


class POT(Element):
	"""
	Potentiometers
	"""

	_all = {}   # list of potentiometers

	def __init__(self, keyname, name, index, event=None, reverse=False):
		# init super class
		super(POT, self).__init__(keyname, name, event)
		# register in the dictionnary of switches
		self._all[index] = self
		self._index = index
		self._value = 255 if reverse else 0
		self.reverse = reverse



	@classmethod
	def checkChanges(cls, index, value):
		"""Check which potentiometer has changed, and notify it"""
		# get the concerned potentiometer
		try:
			Pot = cls._all[index]
		except KeyError:
			logger.debug("An undefined potentiometer has changed (index=%d)", index)
			return  # TODO: should not happen, do something ? Remove the try/except ?
		# assign its new value
		Pot._value = 255-value if Pot.reverse else value
		# notify the Potentiometer that its value changes
		Pot.notify()


	@property
	def value(self):
		"""return the value"""
		return self._value

