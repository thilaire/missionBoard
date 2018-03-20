# coding=utf-8


#TODO: replace with namedTuple ???

class Element:
	"""
	Main class for all the elements
	each element has a name and a keyname
	"""

	_allElements = []   # list of all the created elements
	_MB = None

	def __init__(self, keyname, name, onChange=None):
		self._keyname = keyname
		self._name = name
		self._onChange = onChange
		self._allElements.append(self)


	def __str__(self):
		return '<%s> (`%s`)' % (self._name, self._keyname)

	@classmethod
	def getAll(cls):
		"""Returns the list of all the elements"""
		return cls._allElements

	@classmethod
	def setMB(cls, MB):
		"""Used to set the MissionBoard object"""
		cls._MB = MB