# coding=utf-8

from rpi_TM1638 import TMBoards


# fake enum (enum only exists in Python 3.x)
LED, RGB, SSD, BAR, ROT, POT, SW3, SW2, PB = range(9)
# list of required arguments (used to check)
argsElement = {LED: ('TMindex', 'index'), SSD: ('TMindex','block')}


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
		pass


	def run(self):
		"""
		Main loop (manage the different loops
		"""
		#TODO: do nothing for the moment
		pass



	def add(self, elementType, keyname, name, **args):
		"""
		Declares a new element
		Parameters:
			- elementType: should be in (LED, RGB, SSD, BAR, ROT, POT, SW3, SW2, PB)
			- keyname: name following the IO convention (ie 'Px_yyy_zzz')
			- name: name of the element
			- elementClass: class of the element to be created
			- args: other arguments used to store the element
		"""
		# check the name
		if name in self._elements:
			raise ValueError("An element with the same name (%s) already exists", name)
		# TODO: use the keyname ??
		# check for the arguments
		if set(args.keys()) != set(argsElement[elementType]):
			raise ValueError("The arguments given for the element %s are not correct (receive %s but requires %s)",elementType, args.keys(), argsElement[elementType])
		# store it
		self._elements[name] = (elementType, args)



	def __set__(self, instance, value):
		# check if element exists
		if instance not in self._elements:
			raise ValueError("The element %s does not exist", instance)
		# chek if it can be modified
		e, args = self._elements[instance][0], self._elements[instance][1:] # there is no extended unpack in python 2.x
		if e not in (LED, SSD, BAR, RGB):
			raise ValueError("The element %s is not a display, so it cannot be modified", instance)
		if e == SSD:
			TMindex, block = args['TMindex'], args['block']
			# TODO: check the size of the value (4 chars + eventually 4 points)
			self._TMB.Segments[TMindex*8+block] = value
		elif e == LED:
			TMindex, index = args['TMindex'], args['index']
			self._TMB.leds[TMindex*8+index] = value
		elif e == BAR:
			raise NotImplementedError()
		elif e == RGB:
			raise NotImplementedError()