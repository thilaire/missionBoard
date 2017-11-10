# coding=utf-8

from rpi_TM1638 import TMBoards
from re import compile

from Element import Element
from LED import LED
from SSD import SSD


# list of required arguments (used to check)
dictOfElements = {'LED': LED, 'SSD': SSD}   # TODO: no need, use subclass !!{ x.__name__:x for x in Element.__subclasses__()}

# simple regex for Pxx_YYY_zzz or Pxx_YYY
regElement = compile("P(\d+)_([A-Z0-9]+)(_([A-Za-z0-9]+))?")


class MissionBoard:
	"""
	Main object (contains interfaces to buttons, displays, callbacks, etc.)
	"""

	def __init__(self, TM_clk, TM_dio, TM_stb):
		# initialize the TMboards
		self._TMB = TMBoards(TM_dio, TM_clk, TM_stb)    # chained TM Boards
		# initialize the TMB for all the elements
		Element.setTMB(self._TMB)

	def runCheck(self):
		"""
		check the system, item per item
		"""
		for e in Element.getAll():
			e.runCheck()


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
		if hasattr(self, name):
			raise ValueError("An element with the same name (%s) already exists", name)
		# get the element Type
		m = regElement.search(keyname)
		if not m:
			raise ValueError("The keyname %s doesn't follow the pattern `Pxx_YYY_zzz` or `Pxx_YYY`", keyname)
		elementType = m.group(2)    # panel, elementType, number = m.group(1,2,4)
		# create the object and add it has an attribute
		# (of the class, we have a singleton here; and it's the way to do with Python)
		setattr(self.__class__, name, dictOfElements[elementType](keyname, name, **args))
