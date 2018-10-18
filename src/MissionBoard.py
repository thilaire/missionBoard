# coding=utf-8

"""
Describe how the different buttons/displays are connected
Define the different event loop (callbacks)
"""
import pygame
import logging

from MissionBoard.RGB import RED, FAST, SLOW, BLUE, RGB
from MissionBoard import EventManager
from MissionBoard.State import Init
from Elec import Electricity, Light
from Misc import Laser, FuelPump, Gates, WaterPump, Oxygen
from Flight import Phase, Flight, AllTheRest, Turbo
from Phases import Phase1, Tanks

# init logger
logger = logging.getLogger()
logging.basicConfig(format='%(name)s : %(levelname)s : %(funcName)s - %(message)s', level=logging.DEBUG)

# init pygame (for the sound)
pygame.init()


class MissionBoard(EventManager):
	"""class for the main object"""

	def start(self):
		"""start function (initialize the displays)"""
		# global states
		logger.info('Start!')
		self.electricity = 10       # level of electricity

		# init the displays
		RGB.turnOff()
		# self.AllTheRest_counter.clear()
		# self.AllTheRest_altitude.clear()
		# self.AllTheRest_position.clear()
		# self.AllTheRest_direction.clear()

		# self.LED_OnOff = True
		self.RGB_Go = RED, FAST

		self.Flight_altitude = '76543210'
		self.Flight_position = '1-2-3-40'
		self.Flight_direction = '0123'
		self.Oxygen_level = 7




# add an init method to the Init state (that display 'Init')
def displayInit(self):
	logger.warning("JHLKHJMLKJMLJKMLKLM")
	self.EM.Flight_counter = '- Init -'

Init.init = displayInit


# create the main object and start it !
if __name__ == '__main__':
	func = [Laser, Light, Gates, Turbo, Electricity, FuelPump, WaterPump, Oxygen, Phase, Flight, AllTheRest]
	states = [Init, Phase1, Tanks]
	MB = MissionBoard(func, states)
	MB.run()
