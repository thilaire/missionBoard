# coding=utf-8

"""
Describe how the different buttons/displays are connected
Define the different event loop (callbacks)
"""
import pygame
import logging
from pygame.mixer import Sound
from time import sleep

from MissionBoard.RGB import RGB
from MissionBoard import EventManager
from MissionBoard.State import Init
from MissionBoard.config import SoundPathSpeech
from Elec import Electricity, Light
from Misc import Laser, FuelPump, Gates, WaterPump, Oxygen
from Flight import Phase, Flight, AllTheRest, Turbo,  CountDown as Counter, FlightLoop
from Phases import Phase1, Tanks, Phase2, WarmUp, Phase3, CountDown, TakeOff

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
		# self.AllTheRest_Go = RED, FAST


# add an init method to the Init state (that display 'Init')
def displayInit(self):
	self.EM.CountDown_counter = '- Init -'
	sleep(0.1)
	Sound(SoundPathSpeech + "Initialization.wav").play()


Init.init = displayInit


# create the main object and start it !
if __name__ == '__main__':
	func = [Laser, Light, Gates, Turbo, Electricity, FuelPump, WaterPump, Oxygen, Phase, Flight, FlightLoop, AllTheRest, Counter]
	# states = [Init, Phase1, Tanks, Phase2, WarmUp, Phase3, CountDown]
	states = [Init, TakeOff]
	MB = MissionBoard(func, states)
	MB.run()
