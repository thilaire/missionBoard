# coding=utf-8


class Element:
	"""
	Main class for all the elements
	each element has a name and a keyname
	the TMB is stored once for every elements
	"""
	_TMB = None  # will be initialized once by MissionBoard class (strange way to do, isn't it?)
	_all = []   # list of all the created elements

	def __init__(self, keyname, name ):
		self._keyname = keyname
		self._name = name
		self._all.append(self)

	@classmethod
	def setTMB(cls, TMB):
		"""Used to set the TMB"""
		cls._TMB = TMB

	def __str__(self):
		return '<%s> (`%s`)' % (self._name, self._keyname)

	@classmethod
	def getAll(cls):
		return cls._all
