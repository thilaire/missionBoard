# coding=utf-8

from re import compile
from spidev import SpiDev
import RPi.GPIO as GPIO
from queue import Queue
import logging



# import UX elements (Leds, Buttons, Switches, etc.)
from Element import Element
from EventManager import EventManager
from LED import LED
from Display import DISP, LVL
from PushButton import PB
from RGB import RGB
from Switches import Switch, SW2, SW3
from POT import POT

# list of possible elements
#dictOfElements = {x.__name__: x for x in Element.__subclasses__()} # SW2 is not a subclass of Element
dictOfElements = {'LED': LED, 'DISP': DISP, 'PB': PB, 'RGB': RGB, 'SW2': SW2, 'SW3': SW3, 'POT': POT, 'LVL': LVL}

# simple regex for Pxx_YYY_zzz or Pxx_YYY where P is `T` or `B`
regElement = compile("[TB](\d+)_([A-Z0-9]+)(_([A-Za-z0-9]+))?")

# logger
logger = logging.getLogger()
SPIlogger = logging.getLogger('SPI')


class ElementManager:
	"""
	Main object (contains interfaces to buttons, displays, callbacks, etc.)
	"""

	def __init__(self):
		# save itself to ELement
		Element.setEM(self)

		# open SPI connection
		self._spi = SpiDev()
		self._spi.open(0,0)
		self._spi.max_speed_hz = 100000 #122000

		# declare the SPI queue
		self._SPIqueue = Queue()

		# take the IO24 into consideration when AVR wants to communicate
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		def sendZeroSpi(x):
			logger.debug('IO24 Rising!')
			self.sendSPI([0])
		GPIO.add_event_detect(24, GPIO.RISING, callback=sendZeroSpi)


	def runCheck(self):
		"""
		check the system, item per item
		"""
		for e in Element.getAll():
			e.runCheck()


	def run(self, fct):
		"""
		Infinite loop to send every message in the SPI queue to the ATtiny through the SPI
		(a way to send one message at once)
		"""
		while True:
			# wait for data
			data = self._SPIqueue.get()
			# send the 1st byte
			SPIlogger.debug("Send %s", str(data[0]))
			header, = self._spi.xfer([data.pop(0)])
			SPIlogger.debug("Receive Header= %s", str(header))
			# add more byte if the AVR respond and want to send data
			data.extend([0] * ((header >> 4) - len(data)))
			if data:
				SPIlogger.debug("Send %s", str(data))
				recv = self._spi.xfer(data)
				SPIlogger.debug("Receive data %s", str(recv))

				# treat received data
				if header & 128:
					# change GPIO24 in output
					GPIO.setup(24, GPIO.OUT)
					GPIO.output(24, 1)
					# shutdown ask
					logger.debug("Shutdown asked by the ATtiny")
					import os
					os.system("sudo shutdown -h now")
				else:
					if header & 4:
						Potval = recv[0]
						index = header & 3
						SPIlogger.debug("Pot %d, value=%d", index, Potval)
						POT.checkChanges(index, Potval)
					if header & 8:
						TMval = recv[(header >> 4) - 1]
						index = header & 3
						SPIlogger.debug("TM %d, value=%d", index, TMval)
						Switch.checkChanges(index, TMval)



	def add(self, keyname, name, **args):
		"""
		Declares a new element
		Parameters:
			- keyname: name following the IO convention (ie 'Px_yyy_zzz')
				-> the element type (LED, PB, etc.) is determined from the keyname
			- name: name of the element
			- args: arguments used to determine the elements (TMindex, etc.)
		"""
		# get the element Type
		m = regElement.search(keyname)
		if not m:
			raise ValueError("The keyname %s doesn't follow the pattern `Pxx_YYY_zzz` or `Pxx_YYY`", keyname)
		elementType = m.group(2)    # panel, elementType, number = m.group(1,2,4)
		if elementType not in dictOfElements:
			raise ValueError("The name of the element does not correspond to an existing type")
		# create the object and add it has an attribute
		# (of the class, we have a singleton here; and it's the way to do with Python)
		if isinstance(name, str):
			# check the name
			if hasattr(self, elementType+'_'+name):
				raise ValueError("An element with the same name (%s) already exists", name)
			# add this as an attribute
			setattr(self.__class__, elementType+'_'+name, dictOfElements[elementType](keyname, name, **args))
			logger.debug("Add `%s_%s` to ElementManager", elementType, name)
		else:
			if 'pos' not in args:
				args['pos'] = 0
			for n in name:
				if n:
					# check the name
					if hasattr(self, elementType+'_'+n):
						raise ValueError("An element with the same name (%s) already exists", name)
					# add this as an attribute
					setattr(self.__class__, elementType+'_'+n, dictOfElements[elementType](keyname, n, **args ))
					args['pos'] += 1
					logger.debug("Add `%s_%s` to ElementManager", elementType, n)



	def sendSPI(self, data):
		"""Simply add the data in the queue"""
		SPIlogger.debug("send %s", str(data))
		self._SPIqueue.put_nowait(data)



	def askATdata(self):
		"""
		ask the ATtiny to send its data
		"""
		self.sendSPI([0b11110000])


