# coding=utf-8

"""
Describe how the different buttons/displays are connected
Define the different callbacks
"""
from time import sleep
import asyncio
from aioconsole import ainput

from MissionBoard import MissionBoard, onChange
from RGB import RED, YELLOW, GREEN, OLIVE, FAST, SLOW, BLACK


# create the main object and add the different buttons/displays for each panel
MB = MissionBoard()

# Panel 1: start/mode
#MB.addRotary3(['P1_ROT3', 'gameMode'], TMindex=1, line=2, pins=[2,3])

# Panel 2: displays
MB.add('P2_RGB', ['oxygen', 'electricity', 'takeoff', 'overspeed', 'gate1', 'automaticPilot', 'orbit', '', 'gate2',
	'alarm', 'landing', ''], pos=1)

MB.add('P3_DISP', 'counter', TMindex=4, block=0, size=8)

# Panel 3: laser
#MB.add(['P3_SW2_0', 'LaserArmed'], TMindex=1, line=3, pin=7)
#MB.add(['P3_SW2_1', 'LaserColor'], TMindex=1, line=3, pin=8)

# Panel 4: pilot
MB.add('P4_LED', 'manual', TMindex=4, index=0)
#MB.addPotentiometer(['P4_POT_0', 'roll'], AN=1)
#MB.addPotentiometer(['P4_POT_1', 'yaw'], AN=2)
#MB.addPotentiometer(['P4_POT_0', 'speed'], AN=0)

# Panel 5: flight mode
#MB.addRotary3(['P5_SW_3POS', 'mode'], TMindex=1, line=1, pins=[4,5])
#MB.addSwitch2(['P5_SW2', 'automaticPilot'], TMindex=1, line=1, pin=12)

# Panel 6: lift-off
#MB.addSwitch2(['P6_SW2_1', 'phase1'], TMindex=1, line=1, pin=12)
#MB.addSwitch2(['P6_SW2_2', 'phase2'], TMindex=1, line=1, pin=13)
#MB.addSwitch2(['P6_SW2_3', 'phase3'], TMindex=1, line=1, pin=14)

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
MB.add('P8_RGB', ['rocketEngine', 'spaceshipEngine', 'parachute', 'brake', 'unhook', 'oxygenPump', 'laser',
	'landingGear', 'Go'], pos=13)

# Panel 9: audio
#MB.addSwitch3(['P9_SW4'])




MB.PB_Go.state=0
@onChange(MB.PB_Go)
async def GoChange(self):
	print("GoChange !!")
	if MB.PB_Go.state==1:
		MB.RGB_Go = RED, FAST
		MB.PB_Go.state = 0
	else:
		MB.RGB_Go = BLACK
		MB.PB_Go.state = 1



# run tests!
#MB.runCheck()
async def debug():


	while True:
		com = await ainput(">>>")
		try:
			exec(com)
		except Exception as e:
			print(e)


MB.run(debug)