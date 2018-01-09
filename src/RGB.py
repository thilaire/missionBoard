# coding=utf-8

from Element import Element

RED = 0xFF0000
GREEN = 0x0000FF
YELLOW = 0xFFFF00
BLUE  = 0x00FF00
ORANGE = 0xF58231
PURPLE = 0x911EB4
CYAN = 0x46F0F0
MAGENTA = 0xF032E6
LIME = 0xD2F53C
PINK = 0xFABEBE
TEAL = 0x008080
LAVENDER = 0xE6BEFF
BROWN = 0xAA6E28
BEIGE = 0xFFFAC8
MAROON = 0x800000
MINT = 0xAAFFC3
OLIVE = 0x808000
CORAL = 0xFFD8B1
NAVY = 0x000080
GREY = 0x808080
WHITE = 0xFFFFFF
BLACK = 0x000000
OFF = 0x000000

FAST = 0x5555
SLOW = 0xFF00


def bitRotation(b, shift):
	"""#right and left bit rotation (16-bit numbers)"""
	if shift > 0:
		return ((b >> shift) | (b << (16-shift))) & 0xFFFF
	else:
		return ((b << shift) | (b >> (16-shift))) & 0xFFFF


class RGB(Element):

	def __init__(self, keyname, name, pos):
		super(RGB, self).__init__(keyname, name)
		self._pos = pos


	def runCheck(self):
		pass

	def __set__(self, instance, value):
		# value should be a color (a 3-byte number) and a blink scheme (2-byte number)

		# define color and blink according to the value (could be a color, a color+blink scheme, or a color+scheme+offset
		if isinstance(value, int):
			color = value
			blink = 0xFFFF  # no blink
		elif len(value)==2:
			color,blink = value
		elif len(value)==3:
			color, blink, offset = value
			if offset is True:
				blink = ~blink
			elif isinstance(offset, int):
				blink = bitRotation(blink, offset)

		# convert it to list of bytes, and send it
		data = [self._pos,] + list(blink.to_bytes(2, byteorder='big')) + list(color.to_bytes(3, byteorder='big'))
		self._MB.sendSPI(data)