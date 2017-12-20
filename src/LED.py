# coding=utf-8

from Element import Element
from time import sleep


class LED(Element):
	"""
	class for a LED
	Store its information (TMindex and index) and its state
	"""

	def __init__(self, keyname, name, TMindex, index):
		super(LED, self).__init__(keyname, name)
		self._TMindex = TMindex
		self._index = index
		self._isOn = False  # the led is off at the beginning

	def runCheck(self):
		input('Checking LED %s'%str(self))
		self.set(False)
		print('.',end='')
		sleep(1)
		self.set(True)
		print('.',end='')
		sleep(1)
		self.set(False)
		print('Done')

	def __get__(self, obj, objtype):
		return self._isOn

	def set(self, value):
		"""set the value of the LED"""
		self._TMB.leds[self._TMindex * 8 + self._index] = value
		self._isOn = value

	def __set__(self, obj, value):
		self.set(value)