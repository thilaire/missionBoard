from MissionBoard.RGB import RED, FAST
from MissionBoard.EventManager import EventManager
from MissionBoard.Functionality import Functionality


import logging
logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s - %(name)s : %(levelname)s : %(funcName)s - %(message)s', level=logging.DEBUG)


class MissionBoard(EventManager):
	"""class for the main object"""

	def start(self):
		"""start function (initialize the displays)"""
		# init the displays
		# self.AllTheRest_counter.clear()
		# self.LED_OnOff = True
		# self.RGB_Go = RED, FAST
		logger.debug('Start!')
		self.AllTheRest_RGB = RED, FAST
		self.AllTheRest_counter = '01234569'
		self.askATdata()


class AllTheRest(Functionality):
	def __init__(self, EM):
		super(AllTheRest, self).__init__(EM)
		# Panel B2: displays
		self.add('B3_DISP', 'counter', TMindex=4, block=0, size=8)
		self.add('B8_RGB', 'RGB', pos=18, inverted=True)


# create the main object and start it !
if __name__ == '__main__':
	MB = MissionBoard([AllTheRest, ])
	MB.run()
