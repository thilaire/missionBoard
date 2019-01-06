# coding=utf-8

"""
Flight Phases
(Init, takeoff, etc.)
"""

from MissionBoard.RGB import BLUE, SLOW, BLACK, BLINK, RED
from MissionBoard import State

from Flight import Phase, Flight
from Misc import Oxygen, FuelPump
from .config import SoundPathSpeech

from logging import getLogger
from pygame.mixer import Sound

logger = getLogger()



# ----- Phase 1 --------
class Phase1(State):
	"""Define the Phase 1"""
	funcNext = [Phase, ]

	def init(self):
		self.EM.CountDown_counter = "PHASE 1 "
		Sound(SoundPathSpeech + "phase1.wav").play()


	def isOver(self, func):
		"""the phase is over when the switch 'Phase1' is on"""
		return self.EM.Phase_phase1 and (not self.EM.Phase_phase2) and (not self.EM.Phase_phase3)


# ----- Fill the tanks --------
class Tanks(State):
	"""Define the 'fill the oxygen/fuel tanks' phase"""
	funcNext = [Oxygen, FuelPump]

	def init(self):
		"""to do when we start the phase"""
		Sound(SoundPathSpeech + "phase1engaged.wav").play()
		self.EM.Oxygen.RGB_pump = BLUE, SLOW


	def isOver(self, func):
		"""the phase is over when the tanks are full"""
		return (self.EM.FuelPump_rocket.value == 10) and (self.EM.FuelPump_spaceship.value == 10) and (self.EM.Oxygen_oxygen.value == 10) and (self.EM.FuelPump_pump == 'off') and (not self.EM.Phase.phase2) and (not self.EM.Phase_phase3)


# ----- Phase 2 --------
class Phase2(State):
	"""Define the Phase 2"""
	funcNext = [Phase, ]

	def init(self):
		self.EM.Oxygen.RGB_pump = BLACK
		self.EM.CountDown_counter = "PHASE 2 "
		Sound(SoundPathSpeech + "phase2.wav").play()


	def isOver(self, func):
		"""the phase is over when the switch 'Phase2' is on"""
		return self.EM.Phase_phase1 and self.EM.Phase_phase2 and (not self.EM.Phase_phase3)


# --------- Warm Up ----------
class WarmUp(State):
	"""Warm up Phase"""

	funcNext = [Flight, ]

	def init(self):
		Sound(SoundPathSpeech + "phase2engaged.wav").play()
		self.EM.Flight_RGB_rocketEngine = BLUE, BLINK

	def isOver(self, func):
		return (self.EM.Flight_autoPilot == 'auto') and (self.EM.Flight.rocketEngineStart == True)


# ----- Phase 3 --------
class Phase3(State):
	"""Define the Phase 3"""
	funcNext = [Phase, ]

	def init(self):
		self.EM.CountDown_counter = "PHASE 3 "
		Sound(SoundPathSpeech + "phase3.wav").play()


	def isOver(self, func):
		"""the phase is over when the switch 'Phase3' is on"""
		return self.EM.Phase_phase1 and self.EM.Phase_phase2 and self.EM.Phase_phase3



# --------- Countdown ----------
class CountDown(State):
	"""Countdown Phase"""

	funcNext = [Flight, ]

	def init(self):
		Sound(SoundPathSpeech + "phase3engaged.wav").play()
		self.EM.Flight_RGB_Go = RED, BLINK


	def isOver(self, func):
		return False