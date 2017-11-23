# coding=utf-8

from Element import Element
from time import sleep
import GPIO

class PB(Element):
	"""
	Seven-Segment display
	"""
	def __init__(self, keyname, name, pin):
		super(PB, self).__init__(keyname, name)
		self._pin = pin
		self._value = False
		# configure the pin for input
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin, GPIO.IN)


	def runCheck ( self ):
		"""
		check the push button
		"""
		input('Checking PushButton %s'%str(self))

		# PB is now high/low
		# wait until change
		# PB is now low/high

		print('Done')

	def __get__(self, instance, owner):
		self._value = GPI.input(self._pin)
		return self._value

	def __set__(self, instance, value):
		raise AttributeError("A PushButton cannot be set")


