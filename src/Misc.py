# coding=utf-8

"""
Misc functionalities
(Oxygen, Audio, Doors, pumps, Laser)
"""

import logging
from pygame.mixer import Sound
import RPi.GPIO as GPIO

from RGB import RED, YELLOW, GREEN, ORANGE, FAST, SLOW, BLACK, BLUE, RGB, NOBLINK
from ThreadedLoop import ThreadedLoop


logger = logging.getLogger()
SoundPath = "../sound/"


class Laser(ThreadedLoop):
	"""Manage the laser"""

	def __init__(self, EM):
		"""create the buttons, LEDs, etc."""
		super(Laser, self).__init__(EM)
		# buttons
		self.add('B3_SW2_0', 'armed', values=['disarmed', 'armed'], TMindex=7, pin=4)
		self.add('B3_SW2_1', 'color', values=['blue', 'red'], TMindex=4, pin=7)
		self.add('B8_PB_6', 'fire', gpio=2)
		# LED
		self.add('B8_RGB', 'RGB', pos=18, inverted=True)
		# sound
		self.pewpew = [Sound(SoundPath + "laser1.wav"), Sound(SoundPath + "laser2.wav")]
		# intern variables
		self._laserFired = False

	def isReadyToStart(self):
		"""Returns True if all the buttons are ready to start"""
		return self.armed == 'disarmed' and (not self.fire)

	def onEvent(self, e):
		"""Manage event in the switches, timer, etc."""
		if self.EM.electricity > 0:
			if e == 'FIRE':
				self._laserFired = False
			if self.armed == 'armed':
				self.RGB = (RED if self.color == 'red' else BLUE), (NOBLINK if self._laserFired else FAST)
				if e is self.fire and not self._laserFired:
					self._laserFired = True
					self.pewpew[self.color.value].play()
					self.runTimer('FIRE', 5)
			else:
				self.RGB = BLACK
		else:
			self.RGB = BLACK


class Gates(ThreadedLoop):
	"""Manage the gates"""

	def __init__(self, EM):
		"""create the buttons, LEDs, etc."""
		super(Gates, self).__init__(EM)
		self.add('B2_RGB', 'gate1', pos=5, inverted=True)
		self.add('B2_RGB', 'gate2', pos=9)
		self.add('T7_SW3', 'gates', values=['closed', 'gate1', 'gate2'], TMindex=5, pins=[0, 1])

		self.soundOpen = Sound(SoundPath + "../sound/openGate.wav")
		self.soundClose = Sound(SoundPath + "closeGate.wav")
		self.gateMoving = False  # True if a gate is moving
		self.state = 'closed'
		self.error = False

	def isReadyToStart(self):
		"""Returns True if all the buttons are ready to start"""
		return self.gates == 'closed'

	def onEvent(self, e):
		"""Manage changes for the gate switches"""
		logger.debug("BEFORE: %s", self.__dict__)
		if self.EM.electricity > 0:
			# determine the state (moving, error, etc.)
			if (not self.gateMoving) and (not self.error):
				if e == 'gate1':
					self.soundOpen.play()
					self.runTimer("TIMER", 3)
				elif e == 'gate2':
					self.soundOpen.play()
					self.runTimer("TIMER", 3)
				else:
					self.soundClose.play()
					self.runTimer("TIMER", 5)
				self.gateMoving = True
				self.state = e.valueName
			else:
				# still wrong position ?
				self.error = not (self.gates == self.state)
				# still moving ?
				if e == 'TIMER':  # end of the timer
					self.gateMoving = False
			# then update the RGB color
			if self.error:
				self.gate1 = RED, FAST
				self.gate2 = RED, FAST
			else:
				self.gate1 = (YELLOW if self.state == 'gate1' else BLACK, FAST if self.gateMoving else NOBLINK)
				self.gate2 = (YELLOW if self.state == 'gate2' else BLACK, FAST if self.gateMoving else NOBLINK)
		logger.debug("AFTER: %s", self.__dict__)



class FuelPump(ThreadedLoop):
	"""Manage the fuel pumps (rocket and spaceship)"""
	def __init__(self, EM):
		"""Create the buttons, LED, etc."""
		super(FuelPump, self).__init__(EM)
		# elements
		self.add('T6_LVL_1', 'rocket', TMindex=7, number=0)
		self.add('T6_LVL_2', 'spaceship', TMindex=7, number=1)
		self.add('T6_SW3_2', 'pump', values=['off', 'spaceship', 'rocket'], TMindex=5, pins=[4, 5])
		# sound
		self.sound = Sound(SoundPath + "fuel.wav")
		# levels
		self.fuel = [0, 0, 0]       # [ x, spaceship fuel, rocket fuel ]
		self.rocket = 0
		self.spaceship = 0

	def isReadyToStart(self):
		"""Returns True if all the buttons are ready to start"""
		return self.pump == 'off'

	def onEvent(self, e):
		"""Manage changes for the pump buttons (water, oxygen and fuel)"""
		# receive timer for the Fuel pump
		if e == 'FUEL PUMP':
			if self.pump.valueName != 'off':
				# increase the corresponding level
				self.fuel[self.pump.value] = min(10, self.fuel[self.pump.value] + 1)
				# adjust the level (LED)
				if self.pump.valueName == 'spaceship':
					self.spaceship = self.fuel[self.pump.value]
				else:
					self.rocket = self.fuel[self.pump.value]
				# and run a timer (in 5s or 10s depending on the level) if the tank is not full
				if self.fuel[self.pump.value] != 10:
					self.runTimer('FUEL PUMP', 5 if self.fuel[self.pump.value] < 8 else 10)
				else:
					# stop the sound
					self.sound.fadeout(1000)

		# the fuel button has been changed
		elif e == self.pump and self.EM.state == 'ground':
			if e.valueName != 'off':
				# play sound in loop (until stop)
				self.sound.play(loops=-1, fade_ms=100)
				# run the timer to increase the level in 5 (or 10) seconds
				self.runTimer('FUEL PUMP', 5 if self.fuel[self.pump.value] < 8 else 10)
			else:
				# stop the sound
				self.sound.fadeout(1000)



class WaterPump(ThreadedLoop):
	"""Manage the water pumps (toilet and bathroom)"""
	def __init__(self, EM):
		"""Create the buttons, LED, etc."""
		super(WaterPump, self).__init__(EM)
		# elements
		self.add('T6_SW3_1', 'pump', values=['off', 'toilets', 'bathroom'], TMindex=5, pins=[3, 2])
		# sounds
		self.toilets = Sound(SoundPath + "toilets.wav")
		self.bathroom = Sound(SoundPath + "bathroom.wav")

	def isReadyToStart(self):
		"""Returns True if all the buttons are ready to start"""
		return self.pump == 'off'

	def onEvent(self, e):
		"""Manage the water button"""
		if e == 'toilets':
			self.toilets.play()
		elif e == 'bathroom':
			self.bathroom.play(loops=-1, fade_ms=100)
		else:
			self.bathroom.fadeout(100)


class Oxygen(ThreadedLoop):
	"""Manage the water pumps (toilet and bathroom)"""

	def __init__(self, EM):
		"""Create the buttons, LED, etc."""
		super(Oxygen, self).__init__(EM)
		# elements
		self.add('B8_RGB', 'RGB_pump', pos=19, inverted=True)
		self.add('B8_PB_5', 'pump', gpio=3, edge=GPIO.BOTH)
		self.add('B2_RGB', 'panel', pos=1)
		self.add('T6_LVL_3', 'oxygen', TMindex=7, number=2)

		# sounds
		self.pumpSound = Sound(SoundPath + "oxygen.wav")
		# levels
		self.level = 0
		self.oxygen = 0

	def isReadyToStart(self):
		"""Returns True if all the buttons are ready to start"""
		return not self.pump

	def onEvent(self, e):
		"""Manage the water button"""
		logger.debug("onEvent Oxygen!!")
		if e is self.pump:
			logger.debug("e.value=%s", e.value)
			if not e.value:
				self.pumpSound.play(loops=-1)
				self.runTimer('DOWN', 1)
		elif e == 'DOWN':
			if not self.pump.value:
				self.level = min(10, self.level + 0.3)
				self.oxygen = int(self.level)
				if self.level==10:
					self.pumpSound.fadeout(1000)  # stop sound
				else:
					self.runTimer('DOWN', 1)
			else:
				self.pumpSound.fadeout(1000)# stop sound
				pass

class AllTheRest(ThreadedLoop):
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
		self.add('B1_LED','OnOff', TMindex=4, index=1)

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

		# Panel B6: lift-off
		self.add('B6_SW2_1', 'phase1', TMindex=7, pin=7)
		self.add('B6_SW2_2', 'phase2', TMindex=7, pin=5)
		self.add('B6_SW2_3', 'phase3', TMindex=7, pin=6)

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