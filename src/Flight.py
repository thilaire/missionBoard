# coding=utf-8

"""
Flight functionalities
(Phases, )
"""

import logging
from pygame.mixer import Sound
import RPi.GPIO as GPIO

from MissionBoard.RGB import RED, YELLOW, FAST, BLACK, BLUE, NOBLINK
from MissionBoard import Functionality


logger = logging.getLogger()
SoundPath = "../sound/"



class Phase(Functionality):
	"""Manage the three rocket buttons for the takeoff phases"""
	def __init(self, EM):
		"""Create the buttons, LED, etc."""
		super(Phase, self).__init__(EM)
		# elements
		self.add('B6_SW2_1', 'phase1', TMindex=7, pin=7)
		self.add('B6_SW2_2', 'phase2', TMindex=7, pin=5)
		self.add('B6_SW2_3', 'phase3', TMindex=7, pin=6)
		# sounds


	def onEvent(self, e):
		"""Manage the buttons changes"""
		if self.EM.state == 'Init':
			if (not self.phase1) and (not self.phase2) and (not self.phase3):
				self.EM.nextState()
		elif self.EM.state == 'Phase1':
			if self.phase1:
				self.EM.nextState()
		elif self.EM.state == 'Phase2':
			if self.phase2:
				self.EM.nextState()
		elif self.EM.state == 'Phase3':
			if self.phase3:
				self.EM.nextState()





class Turbo(Functionality):
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




class AllTheRest(Functionality):
	def __init__(self, EM):  # self.add('T2_DISP_1', 'altitude', TMindex=6, block=0, size=8)
		super(AllTheRest, self).__init__(EM)
		self.add('T2_DISP_1', 'altitude', TMindex=6, block=0, size=8)
		# self.add('T2_DISP_2', 'speed', TMindex=1, size=4)
		self.add('T2_DISP_3', 'position', TMindex=5, block=0, size=8)

		# Panel T4: attitude
		# self.add('T2_DISP_1', 'roll', TMindex=2, size=4)
		# self.add('T2_DISP_2', 'yaw', TMindex=3, size=4)
		self.add('T4_DISP_3', 'direction', TMindex=7, block=0, size=4)

		# Panel T6: levels
		self.add('T8_SW2_6', 'computer', values=['backup', 'main'], TMindex=6, pin=3)

		# Panel T9: keyboard
		# TODO:

		# Panel B1: start/mode
		self.add('B1_SW3', 'gameMode', values=['computer', 'spaceship', 'games'], TMindex=4, pins=[0, 1])
		self.add('B1_LED', 'OnOff', TMindex=4, index=1)

		# Panel B2: displays
		self.add('B3_DISP', 'counter', TMindex=4, block=0, size=8)

		# Panel B4: pilot
		self.add('B4_LED', 'manual', TMindex=4, index=0)
		self.add('B4_POT_0', 'roll', index=0)
		self.add('B4_POT_1', 'yaw', index=1)
		self.add('B4_POT_0', 'speed', index=2)

		# Panel B5: flight mode
		self.add('B5_SW3', 'mode', values=['landing', 'orbit', 'takeoff'], TMindex=4, pins=[2, 3])
		self.add('B5_SW2', 'autoPilot', values=['manual', 'auto'], TMindex=4, pin=4)


		# Panel B7: Joystick
		self.add('B7_PB_UP', 'Up', gpio=7)
		self.add('B7_PB_DOWN', 'Down', gpio=5)
		self.add('B7_PB_LEFT', 'Left', gpio=12)
		self.add('B7_PB_RIGHT', 'Right', gpio=6)

		# Panel B8: commands

		# Panel B9: audio
		self.add('B9_SW3', 'Com', values=['Off', 'COM1', 'COM2'], TMindex=4, pins=[5, 6])

	def isReadyToStart(self):
		"""Returns True if all the buttons are ready to start"""
		return True
