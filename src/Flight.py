# coding=utf-8

"""
Flight functionalities
(Phases, )
"""

import logging
from pygame.mixer import Sound
from math import sin, cos

from MissionBoard.RGB import RED, GREEN, SLOW, BLACK, CORAL, MAGENTA, FAST
from MissionBoard import Functionality
from MissionBoard.config import SoundPathSpeech

logger = logging.getLogger("Flight")



def dispFormat(x, l):
	"""format a number with l digits
	used for the 7-segment display"""
	form = "%%%d.%df" % (l, l+1)
	return (form % x)[0:(l+1)]


class Phase(Functionality):
	"""Manage the three rocket buttons for the takeoff phases"""
	def __init__(self, EM):
		"""Create the buttons, LED, etc."""
		super(Phase, self).__init__(EM)
		# elements
		self.phase1 = self.add('B6_SW2_1', 'phase1', TMindex=11, pin=1)
		self.phase2 = self.add('B6_SW2_2', 'phase2', TMindex=11, pin=2)
		self.phase3 = self.add('B6_SW2_3', 'phase3', TMindex=11, pin=3)


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
		self.gas = self.add('T7_SW2_1', 'gas', TMindex=6, pin=7)
		self.LED_gas = self.add('T7_LED_1', 'LED_gas', TMindex=5, index=0)
		self.boost = self.add('T7_SW2_2', 'boost', TMindex=6, pin=6)
		self.LED_boost = self.add('T7_LED_2', 'LED_boost', TMindex=5, index=7)

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
		self.counter = self.add('B3_DISP', 'counter', TMindex=4, block=0, size=8)
		self.RGB_Go = self.add('B8_RGB', 'RGB_Go', pos=21)
		# button
		self.Go = self.add('B8_PB', 'Go', gpio=22)
		# state
		self.isRunning = False
		self.timeToGo = 0.85   # time to go for the new second
		self.value = 15
		# load the sounds
		self.sounds = [Sound(SoundPathSpeech + str(x) + ".wav") for x in range(17)]


	def onEvent(self, e):
		"""Manage changes for the filght buttons"""
		if self.EM.state == 'CountDownState':
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
					self.sounds[self.value].play()
					self.runTimer("CD", self.timeToGo)
					self.isRunning = True
					self.timeToGo = 0.85
					self.EM.runCountDown()
			elif e == "CD":
				self.value -= 1
				if self.value >= 0:
					self.sounds[self.value].play()
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
		self.altitude = self.add('T2_DISP_1', 'altitude', TMindex=6, block=0, size=8)
		# self.speed = self.add('T2_DISP_2', 'speed', TMindex=1, size=4)
		self.positionX = self.add('T2_DISP_3', 'positionX', TMindex=5, block=0, size=4)
		self.positionY = self.add('T2_DISP_3', 'positionY', TMindex=5, block=1, size=4)
		# self.roll = self.add('T2_DISP_1', 'roll', TMindex=2, size=4)
		# self.yaw = self.add('T2_DISP_2', 'yaw', TMindex=3, size=4)
		self.direction = self.add('T4_DISP_3', 'direction', TMindex=7, block=0, size=4)


		# Panel B2:
		self.RGB_autoPilot = self.add('B2_RGB', 'RGB_autoPilot', pos=6)
		self.RGB_takeoff = self.add('B2_RGB', 'RGB_takeoff', pos=3)
		self.RGB_landing = self.add('B2_RGB', 'RGB_landing', pos=10)
		self.RGB_orbit = self.add('B2_RGB', 'RGB_orbit', pos=7)
		self.RGB_overSpeed = self.add('B2_RGB', 'RGB_overSpeed', pos=4)

		# Panel B4: pilot
		self.manual = self.add('B4_LED', 'manual', TMindex=4, index=0)
		self.roll = self.add('B4_POT_0', 'roll', index=0, reverse=True)
		self.yaw = self.add('B4_POT_1', 'yaw', index=1, reverse=True)
		self.speed = self.add('B4_POT_2', 'speed', index=2)

		# Panel B5: flight mode
		self.mode = self.add('B5_SW3', 'mode', values=['landing', 'orbit', 'takeoff'], TMindex=4, pins=[2, 3])
		self.autoPilot = self.add('B5_SW2', 'autoPilot', values=['manual', 'auto'], TMindex=4, pin=4)
		self.flightMode = 'takeoff'

		# Panel B8: buttons
		self.rocketEngine = self.add('B8_PB_0', 'rocketEngine', gpio=4)
		self.RGB_rocketEngine = self.add('B8_RGB', 'RGB_rocketEngine', pos=13)
		# self.SpaceshipEngine = self.add('P8_PB_1', 'SpaceshipEngine', gpio=18)
		# self.Parachute = self.add('P8_PB_2', 'Parachute', gpio=27)
		# self.Brake = self.add('P8_PB_3', 'Brake', gpio=17)
		# self.Unhook = self.add('P8_PB_4', 'Unhook', gpio=14)
		# self.LandingGear = elf.add('P8_PB_7', 'LandingGear', gpio=15)

		self.rocketEngineStart = False


	def onEvent(self, e):
		"""Manage changes for the filght buttons"""
		# init
		if e is None:
			self.RGB_takeoff = MAGENTA if self.mode == 'takeoff' else BLACK
			self.RGB_landing = CORAL if self.mode == 'landing' else BLACK
			self.RGB_orbit = GREEN if self.mode == 'orbit' else BLACK
			self.RGB_autoPilot = GREEN if self.autoPilot else (RED, SLOW)

		# takeoff / landing / orbit button / LEDs
		if e is self.mode:
			if self.mode == self.flightMode:    # go back to normal mode
				self.setFlightModeRGB()
			else:
				# can we change the mode ?
				if (self.mode == 'orbit' and self.okToOrbit()) or (self.mode == 'landing' and self.okToLand()):
					self.flightMode = self.mode.value
				self.setFlightModeRGB()
		# auto pilot
		elif e is self.autoPilot:
			self.RGB_autoPilot = GREEN if self.autoPilot else (RED, SLOW)
		# rocket Engine during Warm up Phase
		elif (e is self.rocketEngine) and (self.EM.state == 'WarmUp'):
			self.RGB_rocketEngine = RED
			self.rocketEngineStart = True
			# TODO: warm up ! (display image/video)
		elif e is self.speed:
			self.EM.FlightLoop.speed = self.speed.value


	def okToOrbit(self):
		"""Returns True if we can go to Orbit mode"""
		return False

	def okToLand(self):
		"""Returns True if we can go to Landing mode"""
		return False

	def setFlightModeRGB(self):
		"""Set the FlightMode LEDs, according to the actual mode and the mode button"""
		logger.debug("%s ? %s", self.flightMode, self.mode)
		if self.flightMode == self.mode:
			self.RGB_takeoff = MAGENTA if self.mode == 'takeoff' else BLACK
			self.RGB_landing = CORAL if self.mode == 'landing' else BLACK
			self.RGB_orbit = GREEN if self.mode == 'orbit' else BLACK
		else:
			self.RGB_takeoff = (RED, FAST) if self.flightMode == 'takeoff' else RED
			self.RGB_landing = (RED, FAST) if self.flightMode == 'landing' else RED
			self.RGB_orbit = (RED, FAST) if self.flightMode == 'orbit' else RED

	def isReadyToStart(self):
		"""Returns True if all the buttons are ready to start"""
		return (self.roll.value <= 10) and (self.yaw.value <= 10) and (self.speed.value <= 10)\
		        and (self.mode == 'takeoff') and (self.autoPilot == 'manual')




class FlightLoop(Functionality):
	def __init__(self, EM):
		super(FlightLoop, self).__init__(EM)

		self.altitude = 0
		self.speed = 0
		self.positionX = 0
		self.positionY = 0
		self.roll = 0
		self.pitch = 90
		self.direction = 0

		self.deltaT = 1e-3      # Constant !!

	def isReadyToStart(self):
		return True

	def onEvent(self, e):
		# event e can only be timer
		logger.debug("Flight Loop !! %s", e)
		# update the position
		self.positionX += self.deltaT * self.speed * cos(self.pitch) * cos(self.direction)
		self.positionY += self.deltaT * self.speed * cos(self.pitch) * sin(self.direction)
		self.EM.Flight.positionX = dispFormat(self.positionX, 4)
		self.EM.Flight.positionY = dispFormat(self.positionY, 4)
		# update the altitude
		self.altitude += self.deltaT*self.speed * sin(self.pitch)
		self.EM.Flight.altitude = dispFormat(self.altitude, 8)

		if e:
			self.runTimer("Loop", 1)




class AllTheRest(Functionality):
	def __init__(self, EM):  # self.add('T2_DISP_1', 'altitude', TMindex=6, block=0, size=8)
		super(AllTheRest, self).__init__(EM)


		# Panel T9: keyboard
		# TODO:

		# Panel B1: start/mode
		self.gameMode = self.add('B1_SW3', 'gameMode', values=['computer', 'spaceship', 'games'], TMindex=4, pins=[0, 1])
		self.OnOff = self.add('B1_LED', 'OnOff', TMindex=4, index=1)

		# Panel B7: Joystick
		self.Up = self.add('B7_PB_UP', 'Up', gpio=7)
		self.Down = self.add('B7_PB_DOWN', 'Down', gpio=5)
		self.Left = self.add('B7_PB_LEFT', 'Left', gpio=12)
		self.Right = self.add('B7_PB_RIGHT', 'Right', gpio=6)

		# Panel B8: commands


		# Panel B9: audio
		self.Com = self.add('B9_SW3', 'Com', values=['Off', 'COM1', 'COM2'], TMindex=4, pins=[5, 6])

	def isReadyToStart(self):
		"""Returns True if all the buttons are ready to start"""
		return True
