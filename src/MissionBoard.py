# coding=utf-8

from rpi_TM1638 import TMBoards
from re import compile

# list of required arguments (used to check)
argsElement = {'LED': ('TMindex', 'index'), 'SSD': ('TMindex','block')}

# simple regex for Pxx_YYY_zzz or Pxx_YYY
regElement = compile("P(\d+)_([A-Z0-9]+)(_([A-Za-z0-9]+))?")

class MissionBoard:
	"""
	Main object (contains interfaces to buttons, displays, callbacks, etc.)
	"""

	def __init__(self, TM_clk, TM_dio, TM_stb):

		# initialize the TMboards
		self._TMB = TMBoards(TM_dio, TM_clk, TM_stb)    # chained TM Boards
		self._elements = {}     # dictionary of elements (displays, buttons, etc.)


	def runCheck(self):
		"""
		check the system, item per item
		"""
		# sort the elements


	def run(self):
		"""
		Main loop (manage the different loops
		"""
		#TODO: do nothing for the moment
		pass



	def add(self, keyname, name, **args):
		"""
		Declares a new element
		Parameters:
			- keyname: name following the IO convention (ie 'Px_yyy_zzz')
				-> the element type (LED, PB, etc.) is determined from the keyname
			- name: name of the element
			- args: arguments used to determine the elements (TMindex, etc.)
		"""
		# check the name
		if name in self._elements:
			raise ValueError("An element with the same name (%s) already exists", name)
		if keyname in self._elements:
			raise ValueError("An element with the same name (%s) already exists", keyname)
		# get the element Type
		m = regElement.search(keyname)
		if not m:
			raise ValueError("The keyname %s doesn't follow the pattern `Pxx_YYY_zzz` or `Pxx_YYY`", keyname)
		elementType = m.group(2)    # panel, elementType, number = m.group(1,2,4)
		# check for the arguments
		if set(args.keys()) != set(argsElement[elementType]):
			raise ValueError("The arguments given for the element %s are not correct (receive %s but requires %s)", elementType, args.keys(), argsElement[elementType])
		# store it
		self._elements[name] = (elementType, args)
		self._elements[keyname] = (elementType, args)



	def __set__(self, instance, value):
		# check if element exists
		if instance not in self._elements:
			raise ValueError("The element %s does not exist", instance)
		# chek if it can be modified
		elementType, args = self._elements[instance]
		if elementType not in ('LED', 'SSD', 'BAR', 'RGB'):
			raise ValueError("The element %s is not a display, so it cannot be modified", instance)
		if elementType == 'SSD':
			TMindex, block = args['TMindex'], args['block']
			# TODO: check the size of the value (4 chars + eventually 4 points)
			self._TMB.segments[TMindex*8+block] = value
		elif elementType == 'LED':
			TMindex, index = args['TMindex'], args['index']
			self._TMB.leds[TMindex*8+index] = value
		elif elementType == 'BAR':
			raise NotImplementedError()
		elif elementType == 'RGB':
			raise NotImplementedError()

