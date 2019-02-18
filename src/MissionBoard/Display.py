# coding=utf-8

from MissionBoard.Element import Element
from MissionBoard.Font import FONT


class DISP(Element):
	"""
	Seven-Segment display
	"""
	def __init__(self, keyname, name, TMindex, block, size):
		super(DISP, self).__init__(keyname, name)
		self._TMindex = TMindex & 7
		self._block = block     # 0 or 1
		self._size = size       # 4 or 8
		self._value = ''        # TODO: useful ?

	def __set__(self, instance, value):
		self._value = value
		# parse the value to transform it in list of bytes int to send
		# -> allows to parse the '.' characters
		lv = []
		for c in value:
			if c not in FONT:
				raise ValueError("Cannot display the character '%s'", c)
			elif c == '.' and lv:  # c is a point and the previous char doesn't a point
				lv.append(lv.pop() | 128)  # add 128 to the previous char (ie add the point)
			else:
				lv.append(FONT[c])
		# check if the size of the list
		if len(lv) != self._size:
			raise ValueError("Cannot assign the Display %s, the value should be %d characters", (str(self), self._size))
		# send the command and the list of values
		command = 0b11000000 + (1 << 4 if self._size == 8 else 0) + (self._block << 3) + self._TMindex
		self.sendSPI([command, ] + lv)


	def setBrightness(self, brightness):
		"""Set the brightness"""
		self.sendSPI([0b10000000 | self._TMindex | (brightness & 7) << 3])

	def off(self):
		"""Turns off the display"""
		self.sendSPI([0b11100000 | self._TMindex])

	def clear(self):
		"""Clear the display"""
		self.sendSPI([0b11101000 | self._TMindex])


class LVL(Element):
	"""
	Levels (on 7-segment display)
	"""

	_values = [0, 0, 0, 0]    # keep track of the values sent to the TMx8

	def __init__(self, keyname, name, TMindex, number):
		super(LVL, self).__init__(keyname, name)
		self._TMindex = TMindex & 7
		self._number = number & 3
		self._value = 0


	def __set__(self, instance, value):
		# bound the value
		if value > 10:
			value = 10
		if value < 0:
			value = 0
		# send commands if the value has changed
		if value != self._value:
			self._value = value
			# build the bytes to send
			byte = (1 << value) - 1
			self._values[self._number] = byte >> 2  # all the bytes up to
			self._values[3] = ((byte & 3) << (2*(2-self._number))) | (self._values[3] & (~(3 << (2*(2-self._number)))))
			# send the command and the list of values
			command = 0b11001000 | self._TMindex
			self.sendSPI([command, ] + self._values)

	@property
	def value(self):
		return self._value

