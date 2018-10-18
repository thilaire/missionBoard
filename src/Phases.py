# coding=utf-8

"""
Flight Phases
(Init, takeoff, etc.)
"""

from MissionBoard.RGB import BLUE, SLOW
from MissionBoard import State

from Flight import Phase
from Misc import Oxygen, WaterPump

from logging import getLogger
logger = getLogger()


# ----- Phase 1 --------
class Phase1(State):
	"""Define the Phase 1"""
	funcNext = [Phase, ]

	def init(self):
		self.EM.Flight_counter = "PHASE 1 "

	def isOver(self, func):
		"""the phase is over when the switch 'Phase1' is on"""
		logger.warning("P1=%s, P2=%s, P3=%s", self.EM.Phase_phase1.value, self.EM.Phase_phase2.value, self.EM.Phase_phase3.value)
		return self.EM.Phase_phase1 and (not self.EM.Phase_phase2) and (not self.EM.Phase_phase3)


# ----- Fill the tanks --------
class Tanks(State):
	"""Define the 'fill the oxygen/fuel tanks' phase"""
	funcNext = [Oxygen, WaterPump]

	def init(self):
		"""to do when we start the phase"""
		self.EM.Oxygen.RGB = BLUE, SLOW


	def isOver(self, func):
		"""the phase is over when the tanks are full"""
		return (self.EM.WaterPump_level == 10) and (self.EM.Oxygen.fuel[1] == 10) and (self.EM.Oxygen.fuel[2] == 10) \
		        and (not self.EM.Phase.phase2) and (not self.EM.Phase_phase3)


