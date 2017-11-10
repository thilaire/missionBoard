# coding=utf-8

from Element import Element
from time import sleep

class SSD(Element):
	"""
	Seven-Segment display
	"""
	def __init__(self, keyname, name, TMindex, block):
		super(SSD, self).__init__(keyname, name)
		self._TMindex = TMindex
		self._block = block
		self._value = ''

	def runCheck ( self ):
		"""
		prints '0.0.0.0' to '9.9.9.9' to test the SSD
		"""
		input('Checking SSD %s'%str(self))
		for i in range(10):
			print('.',end='')
			self.set((str(i)+'.')*4)
			sleep(1)
		self.set('')
		print('Done')

	def __get__(self, instance, owner):
		return self._value

	def __set__(self, instance, value):
		self.set(value)

	def set(self, value):
		"""set the value of the SSD"""
		self._value = value
		self._TMB.segments[self._TMindex * 8 + self._block] = value

