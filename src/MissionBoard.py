# coding=utf-8

from re import compile
from spidev import SpiDev
import RPi.GPIO as GPIO
import asyncio
import types
import logging



#import uvloop
#asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())



# import UI elements (Leds, Buttons, Switches, etc.)
from Element import Element
from LED import LED
from Display import DISP
from PushButton import PB
from RGB import RGB
from Switches import Switch, SW2, SW3
from POT import POT

# list of possible elements
#dictOfElements = {x.__name__: x for x in Element.__subclasses__()} # SW2 is not a subclass of Element
dictOfElements = {'LED': LED, 'DISP': DISP, 'PB': PB, 'RGB': RGB, 'SW2': SW2, 'SW3': SW3, 'POT': POT}

# simple regex for Pxx_YYY_zzz or Pxx_YYY where P is `T` or `B`
regElement = compile("[TB](\d+)_([A-Z0-9]+)(_([A-Za-z0-9]+))?")

logger = logging.getLogger()
SPIlogger = logging.getLogger('SPI')

class MissionBoard:
	"""
	Main object (contains interfaces to buttons, displays, callbacks, etc.)
	"""

	def __init__(self):
		# save itself to ELement
		Element.setMB(self)

		# open SPI connection
		self._spi = SpiDev()
		self._spi.open(0,0)
		self._spi.max_speed_hz = 100000 #122000

		# prepare the asyncio loop and the queues
		self._loop = asyncio.get_event_loop()
		self._SPIqueue = asyncio.Queue(loop=self._loop)
		self._EventQueue = asyncio.Queue(loop=self._loop)

		# take the IO24 into consideration when AVR wants to communicate
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		def sendZeroSpi(x):
			logger.debug('IO24 Rising!')
			self._loop.call_soon_threadsafe(self._SPIqueue.put_nowait, [0])


		GPIO.add_event_detect(24, GPIO.RISING, callback=sendZeroSpi)      # send 0 into SPIQueue in a threadsafe way, see addEvent


	def runCheck(self):
		"""
		check the system, item per item
		"""
		for e in Element.getAll():
			e.runCheck()


	def run(self, fct):
		"""
		Main loop (manage the different queues)
		"""
		self._loop.run_until_complete(asyncio.gather(self._proceedSPIQueue(), self._manageEvents(), fct()))
		# should never happened
		self._loop.close()



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
			if hasattr(self, name):
				raise ValueError("An element with the same name (%s) already exists", name)
			# add this as an attribute
			setattr(self.__class__, elementType+'_'+name, dictOfElements[elementType](keyname, name, **args))
			logger.debug("Add `%s_%s` to MissionBoard",elementType,name)
		else:
			if 'pos' not in args:
				args['pos'] = 0
			for n in name:
				# check the name
				if hasattr(self, n):
					raise ValueError("An element with the same name (%s) already exists", name)
				# add this as an attribute
				setattr(self.__class__, elementType+'_'+n, dictOfElements[elementType](keyname, n, **args ))
				args['pos'] += 1
				logger.debug("Add `%s_%s` to MissionBoard", elementType, n)



	def sendSPI(self, data):
		"""Simply add the data in the queue"""
		SPIlogger.debug("send %s", str(data))
		self._SPIqueue.put_nowait(data)


	async def _proceedSPIQueue(self):
		"""
		Infinite loop to send every message in the SPI queue to the ATtiny through the SPI
		(a way to send one message at once)
		"""
		while True:
			# wait for data
			data = await self._SPIqueue.get()
			# send the 1st byte
			SPIlogger.debug("Send %s", str(data[0]))
			header, = self._spi.xfer([data.pop(0)])
			SPIlogger.debug("Receive Header= %s", str(header))
			# add more byte if the AVR respond and want to send data
			data.extend([0] * ((header>>4) - len(data)))
			if data:
				SPIlogger.debug("Send %s", str(data))
				recv = self._spi.xfer(data)
				SPIlogger.debug("Receive data %s", str(recv))

				# manage the data sent back
				if header&4:
					Potval = recv[0]
					index = header&3
					SPIlogger.debug("Pot %d, value=%d",index,Potval)
					POT.checkChanges(index, Potval)
				if header&8:
					TMval = recv[(header>>4)-1]
					index = header&3
					SPIlogger.debug("TM %d, value=%d",index,TMval)
					Switch.checkChanges(index, TMval)


	async def _manageEvents(self):
		"""
		Infinite loop to manage the events in the Event Queue
		(the queue contains directly the PB objects)
		"""
		while True:
			# wait for event
			event = await self._EventQueue.get()
			# process the event
			logger.debug("Event %s",str(event))
			await event.onChange()


	def addEvent(self, obj):
		"""Simply add the object in the Event Queue
		the put_nowait is done in the same thread as the loop with call_soon_threadsafe
		addEvent is called by a RPi.GIPIO callback, that is in another thread, see
		https://raspberrypi.stackexchange.com/questions/54514/implement-a-gpio-function-with-a-callback-calling-a-asyncio-method
		and
		https://stackoverflow.com/questions/32889527/is-there-a-way-to-use-asyncio-queue-in-multiple-threads
		"""
		self._loop.call_soon_threadsafe(self._EventQueue.put_nowait, obj)


	def askATdata(self):
		"""
		ask the ATtiny to send its data
		"""
		self.sendSPI([0b11110000])



# decorator onChange !
def onChange(obj):
	def fc_wrapper(func):
		# see https://stackoverflow.com/questions/972/adding-a-method-to-an-existing-object-instance
		# for solutions to "Add a Method to an Existing Object Instance"
		setattr(obj, 'onChange', types.MethodType(func, obj))
	return fc_wrapper