# coding=utf-8

"""
Describe how the different buttons/displays are connected
Define the different callbacks
"""
from time import sleep
import asyncio
from aioconsole import ainput
import logging

from MissionBoard import MissionBoard, onChange
from RGB import RED, YELLOW, GREEN, OLIVE, FAST, SLOW, BLACK, BLUE, RGB


# create the main object and add the different buttons/displays for each panel
MB = MissionBoard()

logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s - %(name)s : %(levelname)s : %(funcName)s - %(message)s', level=logging.DEBUG)


# Panel 1: start/mode
MB.add('P1_SW3', 'gameMode', values=['computer', 'spaceship','games'], TMindex=4, pins=[0,1])
MB.add('P1_LED','OnOff', TMindex=4, index=1)

# Panel 2: displays
MB.add('P2_RGB', ['oxygen', 'electricity', 'takeoff', 'overspeed', 'gate1', 'automaticPilot', 'orbit', '', 'gate2',
	'landing','alarm', ''], pos=1, inverted=[5])
MB.add('P3_DISP', 'counter', TMindex=4, block=0, size=8)

# Panel 3: laser
MB.add('P3_SW2_0', 'Laser', values=['disarmed','armed'], TMindex=7, pin=0)
MB.add('P3_SW2_1', 'LaserColor', values=['blue','red'], TMindex=4, pin=7)

# Panel 4: pilot
MB.add('P4_LED', 'manual', TMindex=4, index=0)
MB.add('P4_POT_0', 'roll', index=0)
MB.add('P4_POT_1', 'yaw', index=1)
MB.add('P4_POT_0', 'speed', index=2)

# Panel 5: flight mode
MB.add('P5_SW3', 'mode', values=['landing','orbit','takeoff'], TMindex=4, pins=[2,3])
MB.add('P5_SW2', 'autoPilot', values=['manual','auto'], TMindex=4, pin=4)

# Panel 6: lift-off
MB.add('P6_SW2_1', 'phase1', TMindex=7, pin=3)
MB.add('P6_SW2_2', 'phase2', TMindex=7, pin=1)
MB.add('P6_SW2_3', 'phase3', TMindex=7, pin=2)

# Panel 7: Joystick
MB.add('P7_PB_UP', 'Up', gpio=7)
MB.add('P7_PB_DOWN', 'Down', gpio=5)
MB.add('P7_PB_LEFT', 'Left', gpio=12)
MB.add('P7_PB_RIGHT', 'Right', gpio=6)

# Panel 8: commands
MB.add('P8_PB_0', 'RocketEngine', gpio=4)
MB.add('P8_PB_1', 'SpaceshipEngine', gpio=18)
MB.add('P8_PB_2', 'Parachute', gpio=27)
MB.add('P8_PB_3', 'Brake', gpio=17)
MB.add('P8_PB_4', 'Unhook', gpio=14)
MB.add('P8_PB_5', 'OxygenPump', gpio=3)
MB.add('P8_PB_6', 'Laser', gpio=2)
MB.add('P8_PB_7', 'LandingGear', gpio=15)
MB.add('P8_PB_8', 'Go', gpio=22)
MB.add('P8_RGB', ['rocketEngine', 'spaceshipEngine', 'parachute', 'brake', 'landingGear',  'laser', 'oxygenPump',
	'unhook', 'Go'], pos=13, inverted=[18,19])

# Panel 9: audio
MB.add('P9_SW3', 'Com', values=['Off','COM1','COM2'], TMindex=4, pins=[5,6])


@onChange(MB.SW2_LaserColor)
async def lc(self):
	logger.debug('%s = %s',str(self),self.valueName)
	if MB.SW2_Laser == 'armed':
		MB.RGB_laser = (RED if self == 'red' else BLUE), FAST


@onChange(MB.SW2_Laser)
async def lcc(self):
	logger.debug('%s = %s',str(self),self.valueName)
	if self == 'armed':
		MB.RGB_laser = (RED if MB.SW2_LaserColor == 'red' else BLUE), FAST
	else:
		MB.RGB_laser = BLACK



MB.PB_Go.state=0
@onChange(MB.PB_Go)
async def GoChange(self):
	logger.debug('%s state=%d',str(self),self.state)
	if self.state==1:
		MB.RGB_Go = RED, FAST
		self.state = 0
	else:
		MB.RGB_Go = BLACK
		self.state = 1


@onChange(MB.SW3_mode)
async def changeMode(self):
	logger.debug('%s = %s',str(self),self.valueName)
	MB.RGB_landing = BLACK
	MB.RGB_takeoff = BLACK
	MB.RGB_orbit = BLACK
	if self == 'orbit':
		MB.RGB_orbit = GREEN
	elif self == 'takeoff':
		MB.RGB_takeoff = GREEN
	else:
		MB.RGB_landing = GREEN


# run tests!
#MB.runCheck()
async def debug():

	RGB.turnOff()
	MB.askATdata()
	MB.DISP_counter.clear()

	#MB.LED_OnOff = True
	#MB.RGB_Go = RED,FAST

	while True:
		com = await ainput(">>>")
		try:
			exec(com)
		except Exception as e:
			print(e)


MB.run(debug)