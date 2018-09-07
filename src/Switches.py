# coding=utf-8

from Element import Element

import logging
logger = logging.getLogger()

class Switch(Element):
	"""
	switches (including SW2, SW3 and ROT3)
	"""

	_all = {}     # keep track of the SW object, according to their (TMindex,pin)
	_values = {0: 0, 1: 0, 2: 0, 3: 0}    # keep track of the values

	def __init__(self, keyname, name, TMindex, pins, event=None):
		# init super class
		super(Switch, self).__init__(keyname, name, event)
		# register in the dictionnary of switches
		for pin in pins:
			self._all[(TMindex-4,pin)] = self       # TMindex-4 because TMx7 doesn't count, here
		self._TMindex = TMindex-4


	@classmethod
	def checkChanges(cls, TMindex, value):
		# get the bit that have changed
		diff = value ^ cls._values[TMindex]
		# check for each bit that differ
		lswitch = []    # list of switches that have changed
		for i in range(8):
			if diff & 1:
				# get the corresponding switch
				switch = cls._all.get((TMindex, i))
				if switch:
					# add it the list of switches that have changed (if it is not yet in)
					if switch not in lswitch:
						lswitch.append(switch)
			diff >>= 1
		# notify each switch (it uses the queue of the eventManager associated)
		for sw in lswitch:
			sw.notify()

		cls._values[TMindex] = value

	@property
	def valueName(self):
		return self._valueNames[self.value]


class SW2(Switch):
	"""
	2-position switches
	"""

	def __init__(self, keyname, name, TMindex, pin, values=['off','on'], event=None):
		# init super class
		super(SW2, self).__init__(keyname, name, TMindex, [pin], event)
		self._pin = pin
		self._valueNames = list(values)

	@property
	def value(self):
		"""Get the value"""
		return bool( (self._values[self._TMindex] >> self._pin) & 1 )

	def __eq__(self, other):
		"""Compare to string in _values"""
		# check if we can compare
		if isinstance(other, str):
			if other not in self._valueNames:
				return False
				#raise ValueError("The SW2 %s can only be compared to %s", str(self), str(self._valueNames))
			# return comparison
			return self._valueNames[(self._values[self._TMindex] >> self._pin) & 1] == other
		else:
			return self is other


class SW3(Switch):
	"""
	3-position switches
	"""

	def __init__(self, keyname, name, values, TMindex, pins, event=None):
		# init super class
		super(SW3, self).__init__(keyname, name, TMindex, pins, event)
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
		if isinstance(other, str):
			if other not in self._valueNames:
				raise ValueError("The SW3 %s can only be compared to ", str(self), str(self._values))
			# return comparison
			return self._valueNames[self.value] == other
		else:
			return self is other