# coding=utf-8

from rpi_TM1638 import TMBoards


class MissionBoard:
	"""
	Main object (contains interfaces to buttons, displays, callbacks, etc.)
	"""

	def __init__(self, TM_clk, TM_dio, TM_stb):

		# initialize the TMboards
		self._TMB = TMBoards(TM_dio, TM_clk, TM_stb)


	def run(self):
		"""
		Main loop (manage the different loops
		"""
		#TODO: do nothing for the moment
		pass
