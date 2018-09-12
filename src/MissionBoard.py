# coding=utf-8

"""
Describe how the different buttons/displays are connected
Define the different event loop (callbacks)
"""
import pygame
import logging

from RGB import RED, YELLOW, GREEN, ORANGE, FAST, SLOW, BLACK, BLUE, RGB, NOBLINK
from ElementManager import ElementManager
from ThreadedLoop import ThreadedLoop
from Elec import Electricity, Light
from Misc import Laser, FuelPump, Gates, WaterPump, Oxygen, AllTheRest

from time import sleep

logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s - %(name)s : %(levelname)s : %(funcName)s - %(message)s', level=logging.DEBUG)

pygame.init()



class Turbo(ThreadedLoop):
	"""Manage the turbo"""
	def __init__(self, EM):
		"""create the buttons, LED, etc."""
		super(Turbo, self).__init__(EM)
		self.add('T7_SW2_1', 'gas', TMindex=6, pin=7)
		self.add('T7_LED_1', 'LED_gas', TMindex=5, index=0)
		self.add('T7_SW2_2', 'boost', TMindex=6, pin=6)
		self.add('T7_LED_2', 'LED_boost', TMindex=5, index=7)

	def onEvent(self, e):
		"""Manage changes for the turbo buttons"""
		# adjust the LEDs according to the switches
		logger.debug("onEvent Turbo %s", e)
		if e is self.gas:
			self.LED_gas = e.value
		if e is self.boost:
			logger.debug(self.LED_boost)
			self.LED_boost = e.value
			logger.debug(self.LED_boost)



class MissionBoard(ElementManager):
	"""class for the main object"""
	def __init__(self, loops):
		super(MissionBoard, self).__init__(loops)
		# global states
		self.electricity = 10       # level of electricity

		self.state = 'ground'   # ground, takeoff, orbit or landing


	def start(self):
		"""start function (initialize the displays)"""
		# init the displays
		RGB.turnOff()
		# self.AllTheRest_counter.clear()
		#self.AllTheRest_altitude.clear()
		#self.AllTheRest_position.clear()
		#self.AllTheRest_direction.clear()

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
	MB = MissionBoard([Laser, Light, Gates, Turbo, Electricity, FuelPump, WaterPump, Oxygen, AllTheRest])
	MB.run()
