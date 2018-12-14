# coding=utf-8


import logging

from MissionBoard.EventManager import EventManager
from MissionBoard.Functionality import Functionality
from MissionBoard.State import Init
from MissionBoard.RGB import RED, FAST, SLOW, GREEN

from random import randint, seed

# init logger
logger = logging.getLogger()
logging.basicConfig(format='%(name)s : %(levelname)s : %(funcName)s - %(message)s', level=logging.CRITICAL)

seed()

class Test(Functionality):
	def __init__(self, EM):
		"""create the buttons, LED, etc."""
		super(Test, self).__init__(EM)
		# displays
		self.add('T2_DISP_1', 'altitude', TMindex=6, block=0, size=8)
		self.add('B3_DISP', 'counter', TMindex=4, block=0, size=8)
		self.runTimer("test",1)
		self.add('B8_RGB', 'elec', pos=2)
		self.add('B8_RGB', 'oxy', pos=1)

		self.elec = RED, SLOW
		self.oxy = GREEN, FAST

		self.i = 0

	def onEvent(self, e):
		"""Manage changes"""
		self.counter = "%04d"%self.i + "%04d"%randint(0,9999)
		self.i += 1
		self.runTimer("test", 0.01)



class MissionBoard(EventManager):
	"""class for the main object"""

	def start(self):
		"""start function (initialize the displays)"""
		# global states
		logger.info('Start!')

		# self.Test_counter.clear()
		# self.Test_altitude.clear()

		self.Test_altitude = '76543210'
		# self.Test_counter = '1-2-3-40'
		# for i in range(100):
		# 	self.Test_counter = "".join(str((i*17*j)%10) for j in range(8))
		# 	#self.Test_counter = str(i%10)*8
		logger.info('Done')


def displayInit(self):
	logger.warning("JHLKHJMLKJMLJKMLKLM")
	self.EM.Test_counter = '- Init -'


Init.init = displayInit





# create the main object and start it !
if __name__ == '__main__':
	func = [Test]
	states = [Init]
	MB = MissionBoard(func, states)
	MB.run()
