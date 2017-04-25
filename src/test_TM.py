# coding=utf-8

from chainedTM1638 import chainedTM1638, TMBoards
#
from RPi import GPIO

DIO = 19
CLK = 13
STB = 06, 26

TM = TMBoards(DIO, CLK, STB, 0)



TM.leds[0] = True
TM.leds[12] = True

TM.segments[1] = '0'
TM.segments[4] = '9876'
TM.segments[3,1] = '0'

TM.leds = 254
