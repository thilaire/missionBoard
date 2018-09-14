# coding=utf-8


class Element:
	"""
	Main class for all the elements
	each element has a name and a keyname
	"""

	_allElements = []   # list of all the created elements
	_EM = None          # ATBridge

	def __init__(self, keyname, name, event=None):
		self._keyname = keyname
		self._name = name
		self._eventM = event
		self._allElements.append(self)


	def __str__(self):
		return '<%s> (`%s`)' % (self._name, self._keyname)

	@classmethod
	def getAll(cls):
		"""Returns the list of all the elements"""
		return cls._allElements

	@classmethod
	def setEM(cls, EM):
		"""Used to set the MissionBoard object"""
		cls._EM = EM

	def sendSPI(self, data):
		"""Simply call the sendSPI of the ATBridge"""
		self._EM.sendSPI(data)

	def notify(self):
		"""notify the eventmanager that something changes for this object"""
		if self._eventM:
			self._eventM.notify(self)
