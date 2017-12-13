# coding=utf-8


class Element:
	"""
	Main class for all the elements
	each element has a name and a keyname
	"""
	_all = []   # list of all the created elements

	def __init__(self, keyname, name ):
		self._keyname = keyname
		self._name = name
		self._all.append(self)

	def __str__(self):
		return '<%s> (`%s`)' % (self._name, self._keyname)

	@classmethod
	def getAll(cls):
		return cls._all
