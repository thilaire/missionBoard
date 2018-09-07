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
from Misc import Laser, FuelPump, Gates


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

		# self.add('T2_DISP_1', 'altitude', TMindex=6, block=0, size=8)
		# # self.add('T2_DISP_2', 'speed', TMindex=1, size=4)
		# self.add('T2_DISP_3', 'position', TMindex=5, block=0, size=8)
		# self._altitude = 0
		# self._position = 0
		# self._speed = 0
		#
		# # Panel T4: attitude
		# # self.add('T2_DISP_1', 'roll', TMindex=2, size=4)
		# # self.add('T2_DISP_2', 'yaw', TMindex=3, size=4)
		# self.add('T4_DISP_3', 'direction', TMindex=7, block=0, size=4)
		#
		# # Panel T6: levels
		# self.add('T6_LVL_1', 'fuel_rocket', TMindex=7, number=0)
		# self.add('T6_LVL_2', 'fuel_spaceship', TMindex=7, number=1)
		# self.add('T6_LVL_3', 'oxygen', TMindex=7, number=2)
		# self.add('T6_SW3_1', 'water_pump', values=['off', 'toilets', 'bathroom'], TMindex=5, pins=[3, 2])
		# self.add('T6_SW3_2', 'fuel_pump', values=['off', 'spaceship', 'rocket'], TMindex=5, pins=[4, 5])
		#
		# # Panel T8: buttons 2
		#
		# self.add('T8_SW2_6', 'computer', values=['backup', 'main'], TMindex=6, pin=3)
		#
		# # Panel T9: keyboard
		# # TODO:
		#
		# # Panel B1: start/mode
		# self.add('B1_SW3', 'gameMode', values=['computer', 'spaceship', 'games'], TMindex=4, pins=[0, 1])
		# # self.add('B1_LED','OnOff', TMindex=4, index=1)
		#
		# # Panel B2: displays
		# #self.add('B2_RGB',
		# #	['oxygen', 'electricity', 'takeoff', 'overspeed', 'gate1', 'automaticPilot', 'orbit', 'x', 'gate2',
		# #		'landing', 'alarm', 'y'], pos=1, inverted=[5])
		# self.add('B3_DISP', 'counter', TMindex=4, block=0, size=8)
		#
		# # Panel B3: laser
		#
		# # Panel B4: pilot
		# self.add('B4_LED', 'manual', TMindex=4, index=0)
		# self.add('B4_POT_0', 'roll', index=0)
		# self.add('B4_POT_1', 'yaw', index=1)
		# self.add('B4_POT_0', 'speed', index=2)
		#
		# # Panel B5: flight mode
		# self.add('B5_SW3', 'mode', values=['landing', 'orbit', 'takeoff'], TMindex=4, pins=[2, 3])
		# self.add('B5_SW2', 'autoPilot', values=['manual', 'auto'], TMindex=4, pin=4)
		#
		# # Panel B6: lift-off
		# self.add('B6_SW2_1', 'phase1', TMindex=7, pin=7)
		# self.add('B6_SW2_2', 'phase2', TMindex=7, pin=5)
		# self.add('B6_SW2_3', 'phase3', TMindex=7, pin=6)
		#
		# # Panel B7: Joystick
		# self.add('B7_PB_UP', 'Up', gpio=7)
		# self.add('B7_PB_DOWN', 'Down', gpio=5)
		# self.add('B7_PB_LEFT', 'Left', gpio=12)
		# self.add('B7_PB_RIGHT', 'Right', gpio=6)
		#
		# # Panel B8: commands
		# self.add('B8_PB_0', 'RocketEngine', gpio=4)
		# self.add('B8_PB_1', 'SpaceshipEngine', gpio=18)
		# self.add('B8_PB_2', 'Parachute', gpio=27)
		# self.add('B8_PB_3', 'Brake', gpio=17)
		# self.add('B8_PB_4', 'Unhook', gpio=14)
		# self.add('B8_PB_5', 'OxygenPump', gpio=3)
		# self.add('B8_PB_7', 'LandingGear', gpio=15)
		# self.add('B8_PB_8', 'Go', gpio=22)
		# #self.add('B8_RGB',
		# #	['rocketEngine', 'spaceshipEngine', 'parachute', 'brake', 'landingGear', 'laser', 'oxygenPump', 'unhook',
		# #		'Go'], pos=13, inverted=[18, 19])
		#
		# # Panel B9: audio
		# self.add('B9_SW3', 'Com', values=['Off', 'COM1', 'COM2'], TMindex=4, pins=[5, 6])



	def start(self):
		"""start function (initialize the displays)"""
		# init the display
		RGB.turnOff()
		# self.DISP_counter.clear()
		self.askATdata()
		# self.LED_OnOff = True
		# self.RGB_Go = RED, FAST
		logger.debug('Start!')
		# self.DISP_counter = '01234567'
		# self.DISP_altitude = '01234567'
		# self.LVL_oxygen = 7


# create the main object and start it !
if __name__ == '__main__':
	MB = MissionBoard([Laser, Light, Gates, Turbo, Electricity, FuelPump])
	MB.run()
