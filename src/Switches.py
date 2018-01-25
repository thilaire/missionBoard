# coding=utf-8

from Element import Element


class Switch(Element):
	"""
	switches (including SW2, SW3 and ROT3)
	"""

	_all = {}     # keep track of the SW object, according to their (TMindex,pin)
	_values = {0: 0, 1: 0, 2: 0}    # keep track of the values

	def __init__(self, keyname, name, TMindex, pins):
		# init super class
		super(Switch, self).__init__(keyname, name)
		# register in the dictionnary of switches
		for pin in pins:
			self._all[(TMindex-4,pin)] = self       # TMindex-4 because TMx7 doesn't count, here
		self._TMindex = TMindex-4

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
		print("onChange <"+str(self)+"> = "+str(self.valueName))


	@classmethod
	def checkChanges(cls, TMindex, value):
		# get the bit that have changed
		diff = value ^ cls._values[TMindex]
		# check for each bit that differ
		for i in range(8):
			if diff&1:
				# get the corresponding switch
				switch = cls._all.get((TMindex,i))
				if switch:
					# and call its onChange method (through Event Queue)
					cls._MB.addEvent(switch)
			diff >>= 1

		cls._values[TMindex] = value

	@property
	def valueName(self):
		return self._valueNames[self.value]


class SW2(Switch):
	"""
	2-position switches
	"""

	def __init__(self, keyname, name, TMindex, pin, values=['off','on'],):
		# init super class
		super(SW2, self).__init__(keyname, name, TMindex, [pin])
		self._pin = pin
		self._valueNames = values

	@property
	def value(self):
		"""Get the value"""
		return bool( (self._values[self._TMindex] >> self._pin) & 1 )

	def __eq__(self, other):
		"""Compare to string in _values"""
		# check if we can compare
		if other not in self._valueNames:
			raise ValueError("The SW2 %s can only be compared to ", str(self), str(self._values))
		# return comparison
		return self._valueNames[(self._values[self._TMindex] >> self._pin) & 1] == other



class SW3(Switch):
	"""
	3-position switches
	"""

	def __init__(self, keyname, name, values, TMindex, pins):
		# init super class
		super(SW3, self).__init__(keyname, name, TMindex, pins)
		self._pins = pins
		self._valueNames = values

	@property
	def value(self):
		"""Get the value"""
		val = self._values[self._TMindex] & (1<<self._pins[0] | 1<<self._pins[1])
		return 0 if val == 0 else (1 if val == 1<<self._pins[0] else 2)


	def __eq__(self, other):
		"""Compare to string in _values"""
		# check if we can compare
		if other not in self._valueNames:
			raise ValueError("The SW3 %s can only be compared to ", str(self), str(self._values))
		# return comparison
		return self._valueNames[self.value] == other