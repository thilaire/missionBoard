# coding=utf-8

from MissionBoard.Element import Element

RED = 0xFF0000
GREEN = 0x00FF00
YELLOW = 0xFFFF00
BLUE = 0x0000FF
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
BLINK = 0xF0F0
NOBLINK = 0xFFFF


def bitRotation(b, shift):
	"""#right and left bit rotation (16-bit numbers)"""
	if shift > 0:
		return ((b >> shift) | (b << (16-shift))) & 0xFFFF
	else:
		return ((b << shift) | (b >> (16-shift))) & 0xFFFF


class RGB(Element):
	"""class for the RGB leds"""
	def __init__(self, keyname, name, pos, inverted=False):
		# inverted contain a list of pos, for RGB led those Red and Green are inverted (sometimes happen for my WS2812 clones)
		super(RGB, self).__init__(keyname, name)
		self._pos = pos
		self._inverted = inverted


	def __set__(self, instance, value):
		"""Set a value
		The value should be:
			- a color (a 3-byte number)
			- a color and a blink scheme (2-byte number)
			- a color, a blink scheme and offset (1-byte value)"""

		# define color and blink according to the value (could be a color, a color+blink scheme, or a color+scheme+offset
		if isinstance(value, int):
			color = value
			blink = 0xFFFF  # no blink
		elif len(value) == 2:
			color, blink = value
		elif len(value) == 3:
			color, blink, offset = value
			if offset is True:
				blink = ~blink
			elif isinstance(offset, int):
				blink = bitRotation(blink, offset)
		else:
			raise ValueError("Value is not a int nor a length of size 2 or 3")

		# convert it to list of bytes, and send it
		if self._inverted:
			color = (color & 0x0000FF) | ((color & 0x00ff00) << 8) | ((color & 0xFF0000) >> 8)
		data = [self._pos, ] + list(blink.to_bytes(2, byteorder='big')) + list(color.to_bytes(3, byteorder='big'))
		self.sendSPI(data)

	@classmethod
	def turnOff(cls):
		"""Turn off all the RGB leds"""
		cls._EM.sendSPI([0b00011111])
