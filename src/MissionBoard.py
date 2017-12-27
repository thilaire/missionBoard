# coding=utf-8

from re import compile
try:
	from spidev import SpiDev
except ImportError:
	pass
from Element import Element
from LED import LED
#from SSD import SSD
#from PushButton import PB
from RGB import RGB
import asyncio

# list of possible elements
dictOfElements = {x.__name__: x for x in Element.__subclasses__()}


# simple regex for Pxx_YYY_zzz or Pxx_YYY
regElement = compile("P(\d+)_([A-Z0-9]+)(_([A-Za-z0-9]+))?")


class MissionBoard:
	"""
	Main object (contains interfaces to buttons, displays, callbacks, etc.)
	"""

	def __init__(self):
		# save itself to ELement
		Element.setMB(self)

		# open SPI connection
		try:
			self._spi = SpiDev()
			self._spi.open(0,0)
		except NameError:
			pass
		self._loop = asyncio.get_event_loop()
		self._SPIqueue = asyncio.Queue(loop=self._loop)


	def runCheck(self):
		"""
		check the system, item per item
		"""
		for e in Element.getAll():
			e.runCheck()


	def run(self, fct):
		"""
		Main loop (manage the different loops
		"""
		self._loop.run_until_complete(asyncio.gather(self._proceedSPIQueue(), fct()))

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
		# create the object and add it has an attribute
		# (of the class, we have a singleton here; and it's the way to do with Python)
		if isinstance(name, str):
			# check the name
			if hasattr(self, name):
				raise ValueError("An element with the same name (%s) already exists", name)
			# add this as an attribute
			setattr(self.__class__, elementType+'_'+name, dictOfElements[elementType](keyname, name, **args))
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



	def sendSPI(self, data):
		"""Simply add the data in the queue"""
		print("sendSPI: send " + str(data))
		self._SPIqueue.put_nowait(data)


	async def _proceedSPIQueue(self):
		while True:
			print("_proceedSPIQueue: wait for data")
			# wait for data
			data = await self._SPIqueue.get()
			# process the item
			try:
				self._spi.xfer(data)
			except AttributeError:
				await asyncio.sleep(0.1)
			print("_proceedSPIQueue: received " +str(data))
