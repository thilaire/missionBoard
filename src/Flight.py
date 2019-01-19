# coding=utf-8

"""
Flight functionalities
(Phases, )
"""

import logging
from pygame.mixer import Sound

from MissionBoard.RGB import RED, GREEN, SLOW, BLACK, CORAL, MAGENTA, FAST
from MissionBoard import Functionality
from MissionBoard.config import SoundPathSpeech, SoundPath

logger = logging.getLogger("Flight")




class Phase(Functionality):
	"""Manage the three rocket buttons for the takeoff phases"""
	def __init__(self, EM):
		"""Create the buttons, LED, etc."""
		super(Phase, self).__init__(EM)
		# elements
		self.add('B6_SW2_1', 'phase1', TMindex=11, pin=1)
		self.add('B6_SW2_2', 'phase2', TMindex=11, pin=2)
		self.add('B6_SW2_3', 'phase3', TMindex=11, pin=3)


	def onEvent(self, e):
		"""Manage the buttons changes"""
		# TODO: sounds
		# TODO: turn on associated LEDs, if one day we connect them
		pass

	def isReadyToStart(self):
		"""Returns True if all the buttons are ready to start"""
		return (not self.phase1.value) and (not self.phase2.value) and (not self.phase3.value)



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
		if e is self.gas:
			self.LED_gas = e.value
		elif e is self.boost:
			self.LED_boost = e.value
		elif e is None:
			self.LED_gas = self.gas.value
			self.LED_boost = self.boost.value

	def isReadyToStart(self):
		"""Returns True if all the buttons are ready to start"""
		return (not self.gas.value) and (not self.boost.value)



class CountDown(Functionality):
	"""Manage the count down"""
	def __init__(self, EM):
		"""create the buttons, LEDs, etc."""
		super(CountDown, self).__init__(EM)
		# display
		self.add('B3_DISP', 'counter', TMindex=4, block=0, size=8)
		self.add('B8_RGB', 'RGB_Go', pos=21)
		# button
		self.add('B8_PB', 'Go', gpio=22)
		# state
		self.isRunning = False
		self.timeToGo = 1   # time to go for the new second
		self.value = 9
		# load the sounds
		self.sounds = [Sound(SoundPathSpeech + str(x) + ".wav") for x in range(10)]


	def onEvent(self, e):
		"""Manage changes for the filght buttons"""
		if self.EM.state == 'CountDown':
			if e is self.Go:
				if self.isRunning:
					# delete the timer (but keep how many seconds are left)
					self.timeToGo = self._timers["CD"]
					del self._timers["CD"]
					# stop the countdown
					self.EM.stopCountDown()
					self.isRunning = False
				else:
					# run the countdown
					self.EM.runCountDown()
					self.isRunning = True
					self.runTimer("CD", self.timeToGo)
					self.timeToGo = 1
			elif e == "CD":
				self.sounds[self.value].play()
				self.value -= 1
				if self.value >= 0:
					self.runTimer("CD", 1)


	def isReadyToStart(self):
		"""Returns True if all the buttons are ready to start"""
		return True



class Flight(Functionality):
	"""manage the flight buttons"""
	def __init__(self, EM):
		"""create the buttons, LED, etc."""
		super(Flight, self).__init__(EM)
		# displays
		self.add('T2_DISP_1', 'altitude', TMindex=6, block=0, size=8)
		# self.add('T2_DISP_2', 'speed', TMindex=1, size=4)
		self.add('T2_DISP_3', 'position', TMindex=5, block=0, size=8)
		# self.add('T2_DISP_1', 'roll', TMindex=2, size=4)
		# self.add('T2_DISP_2', 'yaw', TMindex=3, size=4)
		self.add('T4_DISP_3', 'direction', TMindex=7, block=0, size=4)


		# Panel B2:
		self.add('B2_RGB', 'RGB_autoPilot', pos=6)
		self.add('B2_RGB', 'RGB_takeoff', pos=3)
		self.add('B2_RGB', 'RGB_landing', pos=10)
		self.add('B2_RGB', 'RGB_orbit', pos=7)
		self.add('B2_RGB', 'RGB_overSpeed', pos=4)

		# Panel B4: pilot
		self.add('B4_LED', 'manual', TMindex=4, index=0)
		self.add('B4_POT_0', 'roll', index=0, reverse=True)
		self.add('B4_POT_1', 'yaw', index=1, reverse=True)
		self.add('B4_POT_2', 'speed', index=2)

		# Panel B5: flight mode
		self.add('B5_SW3', 'mode', values=['landing', 'orbit', 'takeoff'], TMindex=4, pins=[2, 3])
		self.add('B5_SW2', 'autoPilot', values=['manual', 'auto'], TMindex=4, pin=4)

		# Panel B8: buttons
		self.add('B8_PB_0', 'rocketEngine', gpio=4)
		self.add('B8_RGB', 'RGB_rocketEngine', pos=13)
		# self.add('P8_PB_1', 'SpaceshipEngine', gpio=18)
		# self.add('P8_PB_2', 'Parachute', gpio=27)
		# self.add('P8_PB_3', 'Brake', gpio=17)
		# self.add('P8_PB_4', 'Unhook', gpio=14)
		# self.add('P8_PB_7', 'LandingGear', gpio=15)

		self.rocketEngineStart = False


	def onEvent(self, e):
		"""Manage changes for the filght buttons"""
		if e is self.autoPilot or e is None:
			self.RGB_autoPilot = GREEN if self.autoPilot else (RED, SLOW)
		if e is self.mode or e is None:
			self.RGB_takeoff = MAGENTA if self.mode == 'takeoff' else BLACK
			self.RGB_landing = CORAL if self.mode == 'landing' else BLACK
			self.RGB_orbit = GREEN if self.mode == 'orbit' else BLACK
		logger.debug("e=%s, state = %s", e, self.EM.state)
		if (e is self.rocketEngine) and (self.EM.state == 'WarmUp'):
			self.RGB_rocketEngine = RED
			self.rocketEngineStart = True
			# TODO: warm up ! (display image/video)


	def isReadyToStart(self):
		"""Returns True if all the buttons are ready to start"""
		return (self.roll.value <= 10) and (self.yaw.value <= 10) and (self.speed.value <= 10)\
		        and (self.mode == 'takeoff') and (self.autoPilot == 'manual')





class AllTheRest(Functionality):
	def __init__(self, EM):  # self.add('T2_DISP_1', 'altitude', TMindex=6, block=0, size=8)
		super(AllTheRest, self).__init__(EM)


		# Panel T9: keyboard
		# TODO:

		# Panel B1: start/mode
		self.add('B1_SW3', 'gameMode', values=['computer', 'spaceship', 'games'], TMindex=4, pins=[0, 1])
		self.add('B1_LED', 'OnOff', TMindex=4, index=1)

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
