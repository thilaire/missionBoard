# coding=utf-8


import logging

from MissionBoard.EventManager import EventManager
from MissionBoard.Functionality import Functionality
from MissionBoard.State import Init
# init logger
logger = logging.getLogger()
logging.basicConfig(format='%(name)s : %(levelname)s : %(funcName)s - %(message)s', level=logging.INFO)



class Test(Functionality):
	def __init__(self, EM):
		"""create the buttons, LED, etc."""
		super(Test, self).__init__(EM)
		# displays
		self.add('T2_DISP_1', 'altitude', TMindex=6, block=0, size=8)
		self.add('B3_DISP', 'counter', TMindex=4, block=0, size=8)


class MissionBoard(EventManager):
	"""class for the main object"""

	def start(self):
		"""start function (initialize the displays)"""
		# global states
		logger.info('Start!')

		# self.Test_counter.clear()
		# self.Test_altitude.clear()

		self.Test_altitude = '76543210'
		self.Test_counter = '1-2-3-40'
		for i in range(100):
			self.Test_counter = str((i*17)%10)*8;
		logger.info('Done')

def displayInit(self):
	logger.warning("JHLKHJMLKJMLJKMLKLM")
	self.EM.Flight_counter = '- Init -'


Init.init = displayInit





# create the main object and start it !
if __name__ == '__main__':
	func = [Test]
	states = [Init]
	MB = MissionBoard(func, states)
	MB.run()
