# coding=utf-8

from RPi import GPIO

GPIO.setwarnings(False)       # suppresses warnings on RasPi


# The bits are displayed by mapping bellow
#  -- 0 --
# |       |
# 5       1
#  -- 6 --
# 4       2
# |       |
#  -- 3 --  .7
FONT = {
	' ': 0b00000000,	# (32) <space>
	'!': 0b10000110,	# (33) !
	'"': 0b00100010,	# (34) "
	'(': 0b00110000,	# (40) (
	')': 0b00000110,	# (41) )
	',': 0b00000100,	# (44) ,
	'-': 0b01000000,	# (45) -
	'.': 0b10000000,	# (46) .
	'/': 0b01010010,	# (47) /
	'0': 0b00111111,	# (48) 0
	'1': 0b00000110,	# (49) 1
	'2': 0b01011011,	# (50) 2
	'3': 0b01001111,	# (51) 3
	'4': 0b01100110,	# (52) 4
	'5': 0b01101101,	# (53) 5
	'6': 0b01111101,	# (54) 6
	'7': 0b00100111,	# (55) 7
	'8': 0b01111111,	# (56) 8
	'9': 0b01101111,	# (57) 9
	'=': 0b01001000,	# (61) =
	'?': 0b01010011,	# (63) ?
	'@': 0b01011111,	# (64) @
	'A': 0b01110111,	# (65) A
	'B': 0b01111111,	# (66) B
	'C': 0b00111001,	# (67) C
	'D': 0b00111111,	# (68) D
	'E': 0b01111001,	# (69) E
	'F': 0b01110001,	# (70) F
	'G': 0b00111101,	# (71) G
	'H': 0b01110110,	# (72) H
	'I': 0b00000110,	# (73) I
	'J': 0b00011111,	# (74) J
	'K': 0b01101001,	# (75) K
	'L': 0b00111000,	# (76) L
	'M': 0b00010101,	# (77) M
	'N': 0b00110111,	# (78) N
	'O': 0b00111111,	# (79) O
	'P': 0b01110011,	# (80) P
	'Q': 0b01100111,	# (81) Q
	'R': 0b00110001,	# (82) R
	'S': 0b01101101,	# (83) S
	'T': 0b01111000,	# (84) T
	'U': 0b00111110,	# (85) U
	'V': 0b00101010,	# (86) V
	'W': 0b00011101,	# (87) W
	'X': 0b01110110,	# (88) X
	'Y': 0b01101110,	# (89) Y
	'Z': 0b01011011,	# (90) Z
	'[': 0b00111001,	# (91) [
	']': 0b00001111,	# (93) ]
	'_': 0b00001000,	# (95) _
	'`': 0b00100000,	# (96) `
	'a': 0b01011111,	# (97) a
	'b': 0b01111100,	# (98) b
	'c': 0b01011000,	# (99) c
	'd': 0b01011110,	# (100) d
	'e': 0b01111011,	# (101) e
	'f': 0b00110001,	# (102) f
	'g': 0b01101111,	# (103) g
	'h': 0b01110100,	# (104) h
	'i': 0b00000100,	# (105) i
	'j': 0b00001110,	# (106) j
	'k': 0b01110101,	# (107) k
	'l': 0b00110000,	# (108) l
	'm': 0b01010101,	# (109) m
	'n': 0b01010100,	# (110) n
	'o': 0b01011100,	# (111) o
	'p': 0b01110011,	# (112) p
	'q': 0b01100111,	# (113) q
	'r': 0b01010000,	# (114) r
	's': 0b01101101,	# (115) s
	't': 0b01111000,	# (116) t
	'u': 0b00011100,	# (117) u
	'v': 0b00101010,	# (118) v
	'w': 0b00011101,	# (119) w
	'x': 0b01110110,	# (120) x
	'y': 0b01101110,	# (121) y
	'z': 0b01000111,	# (122) z
	'{': 0b01000110,	# (123) {
	'|': 0b00000110,	# (124) |
	'}': 0b01110000,	# (125) }
	'~': 0b00000001,	# (126) ~
}



READ_MODE = 0x02
WRITE_MODE = 0x00
INCR_ADDR = 0x00
FIXED_ADDR = 0x04


class chainedTM1638(object):
	"""chainedTM1638 class"""

	def __init__(self, dio, clk, stb, brightness=1):
		"""
		Initialize the chainedTM1638 
		GPIO numbers refer to "Broadcom SOC Channel", so CLK=11 means CLK is GPIO11 (so pin 23)
		:param dio: Data I/O GPIO
		:param clk: clock GPIO
		:param stb: Chip Select GPIO    -> a tuple if several chainedTM1638 boards are chained
		:param brightness: brightness of the display (between 0 and 7)
		"""

		# store the GPIOs
		self.dio = dio
		self.clk = clk
		self.stb = tuple(stb)

		# configure the GPIO
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.dio, GPIO.OUT)
		GPIO.setup(self.clk, GPIO.OUT)
		for stb in self.stb:
			GPIO.setup(stb, GPIO.OUT)

		# Clk and Stb <- High for every TM
		self._setStb(True, None)
		GPIO.output(self.clk, True)

		# init the displays
		self.turnOn(brightness)
		self.clearDisplay()



	def clearDisplay(self, TMindex=None):
		"""Turn off every led
		if TMindex is given, every TM of TMindex is cleared
		otherwise, they are all cleared
		"""
		self._setDataMode(WRITE_MODE, INCR_ADDR, TMindex)   # set data read mode (automatic address increased)
		self._setStb(False, TMindex)
		self._sendByte(0xC0)   # address command set to the 1st address
		for i in range(16):
			self._sendByte(0x00)   # set to zero all the addresses
		self._setStb(True, TMindex)


	def turnOff(self, TMindex=None):
		"""Turn off (physically) the leds"""
		self.sendCommand(0x80, TMindex)

	def turnOn(self, brightness, TMindex=None):
		"""
		Turn on the display and set the brightness
		The pulse width used is set to:
		0 => 1/16       4 => 11/16
		1 => 2/16       5 => 12/16
		2 => 4/16       6 => 13/16
		3 => 10/16      7 => 14/16
		:param brightness: between 0 and 7
		:param TMindex: number of the TM to turn on (None if it's for all the TM)
		"""
		self.sendCommand(0x88 | (brightness & 7), TMindex)


	# ==================
	# Internal commands
	# ==================
	def _setStb(self, value, TMindex):
		"""
		Set all the Stb pinouts (if TMindex is True)
		or only one Stb (given by TMindex) to Value
		:param value: value given to the Stb(s)
		:param TMindex: None if all the chainedTM1638 are impacted, or the index of that TM if it concerns only one
		"""
		if TMindex is None:
			for stb in self.stb:
				GPIO.output(stb, value)
		else:
			GPIO.output(self.stb[TMindex], value)


	def _setDataMode(self, wr_mode, addr_mode, TMindex):
		"""
		Set the data modes
		:param wr_mode: READ_MODE (read the key scan) or WRITE_MODE (write data)
		:param addr_mode: INCR_ADDR (automatic address increased) or FIXED_ADDR
		:param TMindex: number of the TM to turn on (None if it's for all the TM)
		"""
		self.sendCommand(0x40 | wr_mode | addr_mode, TMindex)

	def _sendByte(self, data):
		"""
		Send a byte (Stb must be Low)
		:param data: a byte to send 
		"""
		for i in range(8):
			GPIO.output(self.clk, False)
			GPIO.output(self.dio, (data & 1) == 1)
			data >>= 1
			GPIO.output(self.clk, True)


	def sendCommand(self, cmd, TMindex):
		"""
		Send a command
		:param cmd: cmd to send
		:param TMindex: number of the TM to turn on (None if it's for all the TM)
		"""
		self._setStb(False, TMindex)
		self._sendByte(cmd)
		self._setStb(True, TMindex)


	def sendData(self, addr, data, TMindex):
		"""
		Send a data at address addr
		:param addr: adress of the data
		:param data: value of the data
		:param TMindex: number of the TM to turn on (None if it's for all the TM)
		"""
		self._setDataMode(WRITE_MODE, FIXED_ADDR, TMindex)
		self._setStb(False, TMindex)
		self._sendByte(0xC0 | addr)
		self._sendByte(data)
		self._setStb(True, TMindex)






class TMBoards(chainedTM1638):
	"""
	Consider all the chained TM1638 boards (8 leds, 8 7-segment displays and 8 switchs) in one object
	"""

	def __init__(self, dio, clk, stb, brightness=1):
		# initialize chainedTM
		super(TMBoards, self).__init__(dio, clk, stb, brightness)

		# nb of boards
		self._nbBoards = len(stb)

		# add leds, 7-segments
		self._leds = Leds(self)
		self._segments = Segments(self)


	@property
	def nbBoards(self):
		"""Returns the number of TM1638 boards chained"""
		return self._nbBoards

	@property
	def leds(self):
		"""setter for the leds"""
		return self._leds

	@leds.setter
	def leds(self, values):
		"""setter TM.leds = value 
		where value is a list/tuple of booleans
		Performs TM.leds[i] = value[i] for all i"""
		for i, v in enumerate(values):
			self._leds[i] = v

	@property
	def segments(self):
		"""setter for the leds"""
		return self._segments

	@segments.setter
	def segments(self, values):
		"""setter TM.segments = value 
		where value is a list/tuple of booleans
		Performs TM.segments[i] = value[i] for all i"""
		for i, v in enumerate(values):
			self._segments[i] = v


class Leds(object):
	"""Class to manipulate the leds mounted on the chained TM Boards"""
	def __init__(self, TM):
		"""Initialize the Led object
		"""
		self._TM = TM

	def __setitem__(self, index, value ):
		"""
		called by TM.Leds[i] = value
		:param index: index of the led or tuple of indexes
		:param value: (boolean) value to give for this led (it could be a int, evaluated as boolean)
		"""
		# the leds are on the bit 0 of the odd addresses (led[0] on address 1, led[1] on address 3)
		# leds from 8 to 15 are on chained TM #2, etc.
		self._TM.sendData((index % 8) * 2 + 1, 1 if value else 0, index // 8)


class Segments(object):
	"""Class to manipulate the 7-segment displays on the chained TM Boards"""
	def __init__(self, TM):
		"""Initialize the Segment object"""
		self._TM = TM
		self._intern = [0,]*(8*self._TM.nbBoards)     # 8 7-segments per board


	def __setitem__(self, index, value):
		"""
		called by 
			TM.segments[i] = string
				-> set the i-th 7-segment display (and all the following, according to the length of value1)
				all the 7-segment displays after the #i are filled by the characters in value1
				this could be one-character string (so 7-segment #i is set to that character)
				or a longer string, and the following 7-segment displays are modified accordingly
				Example:
				TM.segments[0] = '8'    -> the display #0 is set to '8'
				or 
				TM.segments[0] = '456'  -> the display #0 is set to '4', the display #1 to '5' and #2 to '6'
			
			or
			 	
			TM.segments[i,j] = boolean
				-> set the j-th segment of the i-th 7-segment
				Example:
				TM.segments[2,3] = True -> set the 3rd segment of the 2nd 7-segment display
				
		i: index of the 7-segment display (0 for the 1st 7-segments (left of the 1st TM Board), 8 for the 1st of the 2nd board, etc.)
		j: number of the segment (between 0 and 8)
		

		:param index: index of the 7-segment, or tuple (i,j) 
		:param value: string (or one-character string) when index is a int, otherwise a boolean
		"""
		if isinstance(index, int):
			# TM.segments[i] = '0123'
			for i, c in enumerate(value):
				# get the value to display
				if c not in FONT:
					raise ValueError("Cannot display the character '%s'",c)
				val = FONT[c]
				# check if something change (otherwise do not send data, it's useless)
				if self._intern[index+i] != val:
					# store the new intern value
					self._intern[index+i] = val
					# send the data to the TM
					self._TM.sendData(((index+i) % 8) * 2, val, (index+i) // 8)
		elif isinstance(index, (list,tuple)):
				# get the 7-segment display index and the led index
				i, j = index
				# determine the new intern value
				if value:
					self._intern[i] |= 1 << j
				else:
					self._intern[i] &= ~(1 << j)
				# send the data to the TM
				self._TM.sendData((i % 8) * 2, self._intern[i], i // 8)



