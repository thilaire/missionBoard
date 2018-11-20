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
		self._spi.max_speed_hz = int(1e6)     # 122000

		# declare the SPI queue
		self._SPIqueue = Queue()

		# first add a query for all the data
		self.resetATdata()

		# take the IO24 into consideration when AVR wants to communicate
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		# send 0 to SPI when IO24 is rising (only if the queue is empty)
		GPIO.add_event_detect(24, GPIO.RISING, callback=lambda _: self._SPIqueu.empty() and self.sendSPI([0]))


	def runSPI(self):
		"""
		Infinite loop to send every message in the SPI queue to the ATtiny through the SPI
		(a way to send one message at once)
		"""

		# SPI loop
		while True:
			# wait for data
			data = self._SPIqueue.get()
			# send the 1st byte
			SPIlogger.debug("Send %s (unqueue data)", str(data[0]))
			header, = self._spi.xfer([data.pop(0)])
			SPIlogger.debug("Receive Header= %s", str(header))
			# add more byte if the AVR respond and want to send data
			if header&64:
				data.extend([0] * (len(data)%2))    # add an extra 0 so that the number of byte sent is even

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
					logger.info("Shutdown asked by the ATtiny")
					# import os
					# os.system("sudo shutdown -h now")
				else:
					value = recv[1]
					index = header & 3
					if header & 4:
						# data for the TMx8
						SPIlogger.debug("TM %d, value=%d", index, value)
						Switch.checkChanges(index, value)
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


