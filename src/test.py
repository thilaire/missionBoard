from rpi_TM1638 import TMBoards
from config import *

class MissionBoard():

	def __init__(self):
		# initialize the TM boards
		self._TMB = TMBoards( TM_DIO, TM_CLK, TM1_STB)


	# the counter
	def setCounter(self,st):
		self._TMB.segments[0] = st

	counter = property(None, setCounter)




