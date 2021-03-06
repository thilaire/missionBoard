# coding=utf-8

"""
Misc functionalities
(Oxygen, Audio, Doors, pumps, Laser)
"""

import logging
from pygame.mixer import Sound
import RPi.GPIO as GPIO

from MissionBoard.RGB import RED, YELLOW, FAST, BLACK, BLUE, NOBLINK
from MissionBoard import Functionality
from MissionBoard.config import SoundPath

logger = logging.getLogger("Misc")


class Laser(Functionality):
	"""Manage the laser"""

	def __init__(self, EM):
		"""create the buttons, LEDs, etc."""
		super(Laser, self).__init__(EM)
		# buttons
		self.armed = self.add('B3_SW2_0', 'armed', values=['disarmed', 'armed'], TMindex=7, pin=4)
		self.color = self.add('B3_SW2_1', 'color', values=['blue', 'red'], TMindex=4, pin=7)
		self.fire = self.add('B8_PB_6', 'fire', gpio=2)
		# LED
		self.RGB = self.add('B8_RGB', 'RGB', pos=18, inverted=True)
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


class Gates(Functionality):
	"""Manage the gates"""

	def __init__(self, EM):
		"""create the buttons, LEDs, etc."""
		super(Gates, self).__init__(EM)
		self.gate1 = self.add('B2_RGB', 'gate1', pos=5, inverted=True)
		self.gate2 = self.add('B2_RGB', 'gate2', pos=9)
		self.gates = self.add('T7_SW3', 'gates', values=['closed', 'gate1', 'gate2'], TMindex=5, pins=[0, 1])

		self.soundOpen = Sound(SoundPath + "openGate.wav")
		self.soundClose = Sound(SoundPath + "closeGate.wav")
		self.gateMoving = False  # True if a gate is moving
		self.state = 'closed'
		self.error = False

	def isReadyToStart(self):
		"""Returns True if all the buttons are ready to start"""
		return self.gates == 'closed'

	def onEvent(self, e):
		"""Manage changes for the gate switches"""
		if e is None:
			# initialization
			self.gate1 = (YELLOW if self.state == 'gate1' else BLACK, FAST if self.gateMoving else NOBLINK)
			self.gate2 = (YELLOW if self.state == 'gate2' else BLACK, FAST if self.gateMoving else NOBLINK)
		elif self.EM.electricity > 0:
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




class FuelPump(Functionality):
	"""Manage the fuel pumps (rocket and spaceship)"""
	def __init__(self, EM):
		"""Create the buttons, LED, etc."""
		super(FuelPump, self).__init__(EM)
		# elements
		self.rocket = self.add('T6_LVL_1', 'rocket', TMindex=7, number=0)
		self.spaceship = self.add('T6_LVL_2', 'spaceship', TMindex=7, number=1)
		self.pump = self.add('T6_SW3_2', 'pump', values=['off', 'spaceship', 'rocket'], TMindex=5, pins=[4, 5])
		# sound
		self.sound = Sound(SoundPath + "fuel.wav")
		# levels
		self.fuel = [0, 0, 0]       # [ x, spaceship fuel, rocket fuel ]
		self.rocket = 0     # init level for LVL rocket
		self.spaceship = 0  # init level for LVL spaceship

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
				# and run a timer (in 1s or 3s depending on the level) if the tank is not full
				if self.fuel[self.pump.value] != 10:
					self.runTimer('FUEL PUMP', 1 if self.fuel[self.pump.value] < 8 else 3)
				else:
					# stop the sound
					self.sound.fadeout(1000)

		# the fuel button has been changed
		elif e == self.pump and self.EM.state == 'Tanks':
			if e.valueName != 'off':
				# play sound in loop (until stop)
				self.sound.play(loops=-1, fade_ms=100)
				# run the timer to increase the level in 1 (or 3) seconds
				self.runTimer('FUEL PUMP', 1 if self.fuel[self.pump.value] < 8 else 3)
			else:
				# stop the sound
				self.sound.fadeout(1000)
		# initialization
		elif e is None:
			pass




class WaterPump(Functionality):
	"""Manage the water pumps (toilet and bathroom)"""
	def __init__(self, EM):
		"""Create the buttons, LED, etc."""
		super(WaterPump, self).__init__(EM)
		# elements
		self.pump = self.add('T6_SW3_1', 'pump', values=['off', 'toilets', 'bathroom'], TMindex=5, pins=[3, 2])
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
		elif e == 'off':
			self.bathroom.fadeout(100)


class Oxygen(Functionality):
	"""Manage the water pumps (toilet and bathroom)"""

	def __init__(self, EM):
		"""Create the buttons, LED, etc."""
		super(Oxygen, self).__init__(EM)
		# elements
		self.RGB_pump = self.add('B8_RGB', 'RGB_pump', pos=19, inverted=True)
		self.pump = self.add('B8_PB_5', 'pump', gpio=3, edge=GPIO.BOTH)
		self.panel = self.add('B2_RGB', 'panel', pos=1)
		self.oxygen = self.add('T6_LVL_3', 'oxygen', TMindex=7, number=2)

		# sounds
		self.pumpSound = Sound(SoundPath + "oxygen.wav")
		# levels
		self.level = 0
		self.oxygen = 0     # init level for LVL oxygen

	def isReadyToStart(self):
		"""Returns True if all the buttons are ready to start"""
		return not self.pump

	def onEvent(self, e):
		"""Manage the water button"""
		if self.EM.state == 'Tanks':    # only for `Tanks` state
			if e is self.pump:
				if e.value:
					self.pumpSound.play(loops=-1)
					self.runTimer('DOWN', 1)
			elif e == 'DOWN':
				if self.pump.value:
					self.level = min(10, self.level + 0.8)  # 0.3
					self.oxygen = int(self.level)
					if self.level == 10:
						self.pumpSound.fadeout(1000)  # stop sound
						self.RGB_pump = BLACK
					else:
						self.runTimer('DOWN', 1)
				else:
					self.pumpSound.fadeout(1000)    # stop sound
					pass
