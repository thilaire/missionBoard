# coding=utf-8

from Element import Element


class LED(Element):
	"""
	class for a LED
	Store its information (TMindex and index) and its state
	"""

	def __init__(self, keyname, name, TMindex, index):
		super(LED, self).__init__(keyname, name)
		self._TMindex = TMindex & 3
		self._index = index


	def __set__(self, obj, value):
		"""Set the led (value is evaluated as a boolean)"""
		self.sendSPI([0b01000000 | self._TMindex | self._index << 2 | (1 << 5 if value else 0)])
