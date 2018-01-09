# coding=utf-8

from Element import Element
from time import sleep
from Font import FONT

class DISP(Element):
	"""
	Seven-Segment display
	"""
	def __init__(self, keyname, name, TMindex, block, size):
		super(DISP, self).__init__(keyname, name)
		self._TMindex = TMindex&7
		self._block = block     # 0 or 1
		self._size = size       # 4 or 8
		self._value = ''        # TODO: useful ?

	def runCheck ( self ):
		"""
		prints '0.0.0.0' to '9.9.9.9' to test the SSD
		"""
		input('Checking SSD %s'%str(self))
		for i in range(10):
			print('.',end='')
			self.set((str(i)+'.')*4)
			sleep(1)
		self.set('')
		print('Done')

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
			raise ValueError("Cannot assign the Display %s, the value should be %d characters",(str(self), self._size))
		# send the command and the list of values
		command = 0b11000000 + (1<<4 if self._size==8 else 0) + (self._block<<3) + self._TMindex
		self._MB.sendSPI( [command,] + lv)


	def setBrightness(self, brightness):
		"""Set the brightness"""
		self._MB.sendSPI( [0b10000000 | self._TMindex | (brightness&7)<<3])

	def off(self):
		"""Turns off the display"""
		self._MB.sendSPI([0b11100000 | self._TMindex])

	def clear( self ):
		"""Clear the display"""
		self._MB.sendSPI([0b11101000 | self._TMindex])