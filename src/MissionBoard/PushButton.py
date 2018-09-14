# coding=utf-8

from MissionBoard.Element import Element
import RPi.GPIO as GPIO


class PB(Element):
	"""
	Push Button class
	"""
	def __init__(self, keyname, name, gpio, event=None, edge=GPIO.FALLING):
		super(PB, self).__init__(keyname, name, event)
		self._gpio = gpio
		self._value = False

		# configure the pin for input, with pull-up
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(gpio, edge, callback=lambda x: self.notify(), bouncetime=500)


	@property
	def value(self):
		"""Get the value"""
		self._value = GPIO.input(self._gpio)
		return self._value



