from rpi_TM1638 import TMBoards

class MissionBoard():

	def __init__(self):

		self._TMB = TMBoards(21,20,19)

	def setCounter(self,st):
		self._TMB.segments[0] = st

	counter = property(None, setCounter)




