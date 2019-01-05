# coding=utf-8


import logging
from queue import Queue
from spidev import SpiDev
from time import sleep
import RPi.GPIO as GPIO

from MissionBoard.Element import Element
from MissionBoard.POT import POT
from MissionBoard.Switches import Switch

# logger
logger = logging.getLogger()
SPIlogger = logging.getLogger('SPI')


# SPI rate and delay
speed_hz = int(1e6)


class ATBridge:
	"""
	Main object (contains interfaces to buttons, displays, etc.)
	"""

	def __init__(self):
		"""
		Init the driver with the AT tiny (through the SPI)
		"""
		# save itself to ELement
		Element.setEM(self)

		# open SPI connection
		self._spi = SpiDev()
		self._spi.open(0, 0)
		self._spi.max_speed_hz = speed_hz     # int(1e5) or 122000

		# declare the SPI queue
		self._SPIqueue = Queue()

		# first add a query for all the data
		self.resetATdata()

		# take the IO24 and IO16 into consideration when AVR wants to communicate
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(16, GPIO.IN)

		# send 0 to SPI when IO24 is rising (only if the queue is empty)
		def IO24Rising(_):
			SPIlogger.debug("IO24 is rising")
			if self._SPIqueue.empty():
				self.sendSPI([0])
		GPIO.add_event_detect(24, GPIO.RISING, callback=IO24Rising)
		#GPIO.add_event_detect(24, GPIO.RISING, callback=lambda _: self._SPIqueue.empty() and self.sendSPI([0]))


	def runSPI(self):
		"""
		Infinite loop to send every message in the SPI queue to the ATtiny through the SPI
		(a way to send one message at once)
		"""

		# SPI loop
		while True:
			# wait for data
			data = self._SPIqueue.get()
			SPIlogger.debug("GET data=%s"%str(data))
			# send the data, get the data back from the AT
			SPIlogger.debug("Send %s (unqueue data)", str(data))
			#recv = self._spi.xfer(data, speed_hz, delay_usec)
			# send the data byte per byte (once in a row is too fast, AVR does not have time to store data in its buffer)
			recv=[]
			for d in data:
				# wait unti IO16 is low
				while GPIO.input(16):
					#SPIlogger.debug("Has to wait for IO16")
					sleep(1e-4)
				# send one byte
				recv.extend(self._spi.xfer([d]))
				#sleep(1e-4)
			SPIlogger.debug("Receive data = %s", str(recv))

			# find a significative header
			rec = iter(recv)
			while True:
				try:
					header = next(b for b in rec if b&64)       # find first header
				except StopIteration:
					# nothing more to do, no data send by the ATtiny, break the loop
					break
				else:
					# a header has been sent, get the next data
					try:
						value = next(rec)
					except StopIteration:
						# ask for a new byte if needed
						value, = self._spi.xfer([0])
						SPIlogger.debug("Send one more byte (0) and receive back = %d", value)

					# treat received data
					if header & 128:
						# change GPIO24 in output
						GPIO.setup(24, GPIO.OUT)
						GPIO.output(24, 1)
						# shutdown ask
						logger.critical("Shutdown asked by the ATtiny")
						# import os
						# os.system("sudo shutdown -h now")
					else:
						index = header & 3
						if header & 4:
							# data for the TMx8
							SPIlogger.debug("TM %d, value=%d", index, value)
							Switch.checkChanges(index, value)
						else:
							if index == 3:
								# rocket switch
								SPIlogger.debug("Rocket switch TM %d, value=%d", index+4, value)
								Switch.checkChanges(index+4, value)
							else:
								# data for the Potar
								SPIlogger.debug("Pot %d, value=%d", index, value)
								POT.checkChanges(index, value)



			# sleep a µs
			sleep(1e-3)     #TODO: we can decrease it... 1e-3s is the required sleep if we constantly send data to the AT (to avoid buffer overflow)




	def sendSPI(self, data):
		"""Simply add the data in the queue"""
		self._SPIqueue.put_nowait(data)
		if isinstance(data, list):
			strdata = ", ".join(str(d)+'(0b{0:08b})'.format(d) if i == 0 else str(d) for i, d in enumerate(data))
		else:
			strdata = str(data)+'(0b{0:08b})'.format(data)
		SPIlogger.debug("Put [%s] in the queue (content=%s)", strdata, str(list(self._SPIqueue.queue)))


	def resetATdata(self):
		"""
		ask the ATtiny to send its data
		"""
		self.sendSPI([0b11110000])


