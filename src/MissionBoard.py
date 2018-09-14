# coding=utf-8

"""
Describe how the different buttons/displays are connected
Define the different event loop (callbacks)
"""
import pygame
import logging

from MissionBoard.RGB import RED, FAST, SLOW, BLUE, RGB
from MissionBoard import EventManager

from Elec import Electricity, Light
from Misc import Laser, FuelPump, Gates, WaterPump, Oxygen
from Flight import Phase, AllTheRest, Turbo
from Phases import Phase1, Tanks

# init logger
logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s - %(name)s : %(levelname)s : %(funcName)s - %(message)s', level=logging.DEBUG)

# init pygame (for the sound)
pygame.init()


class MissionBoard(EventManager):
	"""class for the main object"""

	def start(self):
		"""start function (initialize the displays)"""
		# global states
		self.electricity = 10       # level of electricity

		# init the displays
		RGB.turnOff()
		# self.AllTheRest_counter.clear()
		# self.AllTheRest_altitude.clear()
		# self.AllTheRest_position.clear()
		# self.AllTheRest_direction.clear()

		# self.AllTheRest_counter.clear()

		# self.LED_OnOff = True
		self.RGB_Go = RED, FAST
		logger.debug('Start!')
		# self.AllTheRest_counter = '01234567'
		self.AllTheRest_altitude = '76543210'
		self.AllTheRest_position = '1-2-3-40'
		self.AllTheRest_direction = '0123'
		# self.LVL_oxygen = 7

		self.askATdata()


# create the main object and start it !
if __name__ == '__main__':
	func = [Laser, Light, Gates, Turbo, Electricity, FuelPump, WaterPump, Oxygen, Phase, AllTheRest]
	states = [Phase1, Tanks]
	MB = MissionBoard(func, states)
	MB.run()
