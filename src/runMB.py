# coding=utf-8

"""
Describe how the different buttons/displays are connected
Define the different callbacks
"""
from time import sleep
import asyncio

from MissionBoard import MissionBoard
from RGB import RED, YELLOW, GREEN, OLIVE, FAST, SLOW


# create the main object and add the different buttons/displays for each panel
MB = MissionBoard()

# Panel 1: start/mode
#MB.addRotary3(['P1_ROT3', 'gameMode'], TMindex=1, line=2, pins=[2,3])

# Panel 2: displays
MB.add('P2_RGB', ['oxygen', 'electricity', 'takeoff', 'overspeed', 'gate1', 'automaticPilot', 'orbit', '', 'gate2',
	'alarm', 'landing', ''], pos=1)

#MB.add('P3_SSD', 'counter', TMindex=0, block=0)

# Panel 3: laser
#MB.addSwitch2(['P3_SW_0', 'LaserArmed'], TMindex=1, line=1, pin=1)
#MB.addSwitch2(['P3_SW_1', 'LaserColor'], TMindex=1, line=1, pin=2)

# Panel 4: pilot
#MB.add('P4_LED', 'manual', TMindex=0, index=0)
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
#MB.add('P6_PB_UP', 'up', gpio=5)     #TODO: check the gpios!! !!
#MB.add('P6_PB_DOWN', 'down', gpio=6)
#MB.add('P6_PB_LEFT', 'left', gpio=7)
#MB.add('P6_PB_RIGHT', 'right', gpio=12)

# Panel 8: commands
#MB.addPushButton(['P8_PB_0', 'rocketEngine'], IO=12)
#MB.addPushButton(['P8_PB_1', 'spaceshipEngine'], IO=12)
#MB.addPushButton(['P8_PB_2', 'parachute'], IO=12)
#MB.addPushButton(['P8_PB_3', 'brake'], IO=12)
#MB.addPushButton(['P8_PB_4', 'unhook'], IO=12)
#MB.addPushButton(['P8_PB_5', 'oxygenPump'], IO=12)
#MB.addPushButton(['P8_PB_6', 'laser'], IO=12)
#MB.addPushButton(['P8_PB_7', 'landingGear'], IO=12)
#MB.addPushButton(['P8_PB_8', 'go'], IO=12)
MB.add('P8_RGB', ['rocketEngine', 'spaceshipEngine', 'parachute', 'brake', 'unhook', 'oxygenPump', 'laser',
	'landingGear', 'Go'], pos=13)

# Panel 9: audio
#MB.addSwitch3(['P9_SW4'])


# some test to debug
#MB.counter = '0.1.2.3.'
#MB.go = True
#MB.manual = True



# run tests!
#MB.runCheck()
async def test():
	MB.RGB_Go = RED

	await asyncio.sleep(10)

	MB.RGB_gate1 = YELLOW, FAST
	MB.RGB_gate2 = OLIVE, SLOW
	MB.RGB_orbit = GREEN, SLOW, 1


	print('Done')

MB.run(test)