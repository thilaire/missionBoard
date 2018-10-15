# coding=utf-8

"""
Electricity functionalities
"""

import logging

from MissionBoard.RGB import RED, YELLOW, GREEN, ORANGE, FAST, RGB
from MissionBoard import Functionality

logger = logging.getLogger("Elec")
SoundPath = "../sound/"


class Electricity(Functionality):
	"""Manage the electricity (buttons and displays)"""
	def __init__(self, EM):
		"""create the buttons, LED, etc."""
		super(Electricity, self).__init__(EM)
		self.add('T8_SW2_3', 'solar', TMindex=6, pin=2)
		self.add('T8_LED_3', 'LED_solar', TMindex=5, index=4)
		self.add('T8_SW2_4', 'battery', TMindex=6, pin=1)
		self.add('T8_LED_4', 'LED_battery', TMindex=5, index=5)
		self.add('T8_SW2_5', 'fuel', TMindex=6, pin=0)
		self.add('T8_LED_5', 'LED_fuel', TMindex=5, index=6)
		self.add('B2_RGB', 'RGB', pos=2)

	def onEvent(self, e):
		"""Manage changes for the electricity switches"""
		logger.debug("enter `electricity` function")
		# adjust the LEDs according to the switches
		if e is self.solar:
			self.LED_solar = e.value
		if e is self.battery:
			self.LED_battery = e.value
		if e is self.fuel:
			self.LED_fuel = e.value
		# amount of electricity
		elec = self.solar.value * 1 + self.battery.value * 2 + self.fuel.value * 4  # 1,2 and 4 as weight
		if elec != self.EM.electricity:
			if elec == 0:
				# shutdown!
				logger.debug("shutdown electricity!")
				RGB.turnOff()
				# self.EM.DISP_altitude.off()
				# self.EM.DISP_position.off()
				# self.EM.DISP_counter.off()
				# self.EM.DISP_speed.off()
				# self.EM.DISP_roll.off()
				# self.EM.DISP_yaw.off()
			else:
				# adjust the brightness
				# self.EM.DISP_altitude.setBrightness(elec)
				# self.EM.DISP_position.setBrightness(elec)
				# self.EM.DISP_direction.setBrightness(elec)
				# self.EM.DISP_counter.setBrightness(elec)
				# self.EM.DISP_speed.setBrightness(elec)
				# self.EM.DISP_roll.setBrightness(elec)
				# self.EM.DISP_yaw.setBrightness(elec)
				# set the RGB electricity led
				pass
			self.RGB = GREEN if elec > 2 else YELLOW if elec == 2 else ORANGE if elec == 1 else (RED, FAST)
			self.EM.electricity = elec

	def isReadyToStart(self):
		"""Returns True if all the buttons are ready to start"""
		return (not self.solar) and (not self.battery) and (not self.fuel)


class Light(Functionality):
	"""Manage the lights inside/outside the spaceship"""
	def __init__(self, EM):
		"""create the buttons, LEDs, etc."""
		super(Light, self).__init__(EM)
		self.add('T8_SW2_1', 'cabin', TMindex=6, pin=5)
		self.add('T8_LED_1', 'LED_cabin', TMindex=5, index=2)
		self.add('T8_SW2_2', 'outside', TMindex=6, pin=4)
		self.add('T8_LED_2', 'LED_outside', TMindex=5, index=3)

	def onEvent(self, e):
		"""Manage changes for the light switches"""
		if self.EM.state != 'Init':
			# adjust the LEDs according to the switches
			if e is self.cabin:
				self.LED_cabin = e.value
			if e is self.outside:
				self.LED_outside = e.value

	def isReadyToStart(self):
		"""Returns True if all the buttons are ready to start"""
		return (not self.cabin) and (not self.outside)
