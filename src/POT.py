# coding=utf-8

from Element import Element


class POT(Element):
	"""
	Potentiometers
	"""

	_all = {}   # list of potentiometers

	def __init__(self, keyname, name, index):
		# init super class
		super(POT, self).__init__(keyname, name)
		# register in the dictionnary of switches
		self._all[index] = self
		self._index = index
		self._value = 0

	def runCheck(self):
		"""
		check the push button
		"""
		# input('Checking PushButton %s' % str(self.name))
		#
		# print('%s is %s' % 'on' if self else 'off')     # WORK ????
		# v = self._value
		# while (v != self._value):
		# 	sleep(5e-2)
		#
		# # PB is now low/high
		# print('%s is %s' % 'on' if self else 'off')  # WORK ????
		# print('Done')
		pass


	async def onChange(self):
		"""onChange method
		to be filled for each switch"""
		print("onChange <"+str(self)+"> = "+str(self.value))


	@classmethod
	def checkChanges(cls, index, value):
		# get the concerned potentiometer
		try:
			Pot = cls._all[index]
		except:
			print("INDEX="+str(index))
		# assign its new value
		Pot._value = value
		# call onChange method (through Event Queue) for each switch
		cls._MB.addEvent(Pot)


	@property
	def value(self):
		return self._value