# coding=utf-8


import logging
from queue import Queue
from spidev import SpiDev

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
		self._spi.max_speed_hz = 100000     # 122000

		# declare the SPI queue
		self._SPIqueue = Queue()

		# take the IO24 into consideration when AVR wants to communicate
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(24, GPIO.RISING, callback=lambda _: self.sendSPI([0]))    # send 0 to SPI when IO24 is rising


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
					logger.info("Shutdown asked by the ATtiny")
					# import os
					# os.system("sudo shutdown -h now")
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






	def sendSPI(self, data):
		"""Simply add the data in the queue"""
		SPIlogger.debug("send %s in the queue", str(data))
		self._SPIqueue.put_nowait(data)



	def askATdata(self):
		"""
		ask the ATtiny to send its data
		"""
		self.sendSPI([0b11110000])


