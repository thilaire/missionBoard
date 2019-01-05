# coding=utf-8

"""
Flight Phases
(Init, takeoff, etc.)
"""

from MissionBoard.RGB import BLUE, SLOW
from MissionBoard import State

from Flight import Phase
from Misc import Oxygen, FuelPump

from logging import getLogger
from pygame.mixer import Sound

logger = getLogger()
SoundPath = "../sound/"


# ----- Phase 1 --------
class Phase1(State):
	"""Define the Phase 1"""
	funcNext = [Phase, ]

	def init(self):
		self.EM.Flight_counter = "PHASE 1 "
		Sound(SoundPath + "phase1.wav").play()


	def isOver(self, func):
		"""the phase is over when the switch 'Phase1' is on"""
		logger.warning("P1=%s, P2=%s, P3=%s", self.EM.Phase_phase1.value, self.EM.Phase_phase2.value, self.EM.Phase_phase3.value)
		return self.EM.Phase_phase1 and (not self.EM.Phase_phase2) and (not self.EM.Phase_phase3)


# ----- Fill the tanks --------
class Tanks(State):
	"""Define the 'fill the oxygen/fuel tanks' phase"""
	funcNext = [Oxygen, FuelPump]

	def init(self):
		"""to do when we start the phase"""
		Sound(SoundPath + "phase1engaged.wav").play()
		self.EM.Oxygen.RGB = BLUE, SLOW


	def isOver(self, func):
		"""the phase is over when the tanks are full"""
		logger.debug("Pumps= %d %d %d", self.EM.FuelPump_rocket.value, self.EM.FuelPump_spaceship.value, self.EM.Oxygen_oxygen.value)
		return (self.EM.FuelPump_rocket.value == 10) and (self.EM.FuelPump_spaceship.value == 10) and (self.EM.Oxygen_oxygen.value == 10) and (self.EM.FuelPump_pump == 'off') and (not self.EM.Phase.phase2) and (not self.EM.Phase_phase3)


# ----- Phase 2 --------
class Phase2(State):
	"""Define the Phase 1"""
	funcNext = [Phase, ]

	def init(self):
		self.EM.Flight_counter = "PHASE 2 "
		Sound(SoundPath + "phase2.wav").play()


	def isOver(self, func):
		"""the phase is over when the switch 'Phase2' is on"""
		return self.EM.Phase_phase1 and self.EM.Phase_phase2 and (not self.EM.Phase_phase3)
