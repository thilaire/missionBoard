# coding=utf-8

from Element import Element
from time import sleep
try:
	import GPIO
except ImportError:
	pass

class PB(Element):
	"""
	Seven-Segment display
	"""
	def __init__(self, keyname, name, gpio):
		super(PB, self).__init__(keyname, name)
		self._gpio = gpio
		self._value = False
		try:
			# configure the pin for input, with pull-up
			GPIO.setmode(GPIO.BCM)
			GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD)
			GPIO.add_event_detect(gpio, GPIO.BOTH, callback=lambda: self._MB.addEvent(self), bouncetime=200)
		except NameError:
			pass

	def runCheck(self):
		"""
		check the push button
		"""
		# input('Checking PushButton %s' % str(self.name))
		#
		# print('%s is %s' % 'on' if self else 'off')     # WORK ????
		# v = self._value
		# while (v != self._value):
		# 	sleep(5e-2)
		#
		# # PB is now low/high
		# print('%s is %s' % 'on' if self else 'off')  # WORK ????
		# print('Done')
		pass


	@property
	def value(self):
		"""Get the value"""
		try:
			self._value = GPIO.input(self._gpio)
		except NameError:
			pass

		return self._value



