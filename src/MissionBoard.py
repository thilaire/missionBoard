# coding=utf-8

"""
Describe how the different buttons/displays are connected
Define the different callbacks
"""
from time import sleep
from aioconsole import ainput
import logging

from EventManager import EventManager
from ElementManager import ElementManager
from RGB import RED, YELLOW, GREEN, ORANGE, FAST, SLOW, BLACK, BLUE, RGB

# logger
logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s - %(name)s : %(levelname)s : %(funcName)s - %(message)s', level=logging.DEBUG)

# some const
NOT_YET_INIT = 1
GROUND = 2
TAKE_OFF = 3
ORBIT = 4
LANDING = 5


class MissionBoard(ElementManager):

	def __init__(self):

		super(MissionBoard, self).__init__()

		# create eventManagers
		laserE = EventManager(self.laser)
		gatesE = EventManager(self.gates)
		lightE = EventManager(self.light)
		turboE = EventManager(self.turbo)
		electricityE = EventManager(self.electricity)
		
		# Panel T2: position
		self.add('T2_DISP_1', 'altitude', TMindex=6, block=0, size=8)
		#self.add('T2_DISP_2', 'speed', TMindex=1, size=4)
		self.add('T2_DISP_3', 'position', TMindex=5, block=0, size=8)
		self._altitude = 0
		self._position = 0
		self._speed = 0

		# Panel T4: attitude
		#self.add('T2_DISP_1', 'roll', TMindex=2, size=4)
		#self.add('T2_DISP_2', 'yaw', TMindex=3, size=4)
		self.add('T4_DISP_3', 'direction', TMindex=7, block=0, size=4)

		# Panel T6: levels
		self.add('T6_LVL_1', 'fuel_rocket', TMindex=7, number=0)
		self.add('T6_LVL_2', 'fuel_spaceship', TMindex=7, number=1)
		self.add('T6_LVL_3', 'oxygen', TMindex=7, number=2)
		self.add('T6_SW3_1', 'water_pump', values=['off','toilets','bathroom'], TMindex=5, pins=[3,2])
		self.add('T6_SW3_2', 'fuel_pump', values=['off','spaceship','rocket'], TMindex=5, pins=[4,5])

		# Panel T7: buttons 1
		self.add('T7_SW2_1', 'turbo_gas', TMindex=6, pin=7, event=turboE)
		self.add('T7_LED_1', 'turbo_gas', TMindex=5, index=0)
		self.add('T7_SW2_2', 'turbo_boost', TMindex=6, pin=6, event=turboE)
		self.add('T7_LED_2', 'turbo_boost', TMindex=5, index=7)
		self.add('T7_SW3', 'gates', values=['closed','gate1','gate2'], TMindex=5, pins=[0,1], event=gatesE)

		# Panel T8: buttons 2
		self.add('T8_SW2_1', 'light_cabin', TMindex=6, pin=5, event=lightE)
		self.add('T8_LED_1', 'light_cabin', TMindex=5, index=2)
		self.add('T8_SW2_2', 'light_outside', TMindex=6, pin=4, event=lightE)
		self.add('T8_LED_2', 'light_outside', TMindex=5, index=3)
		self.add('T8_SW2_3', 'solar', TMindex=6, pin=2, event=electricityE)
		self.add('T8_LED_3', 'solar', TMindex=5, index=4)
		self.add('T8_SW2_4', 'battery', TMindex=6, pin=1, event=electricityE)
		self.add('T8_LED_4', 'battery', TMindex=5, index=5)
		self.add('T8_SW2_5', 'fuel_cell', TMindex=6, pin=0, event=electricityE)
		self.add('T8_LED_5', 'fuel_cell', TMindex=5, index=6)
		self.add('T8_SW2_6', 'computer', values=['backup', 'main'], TMindex=6, pin=3)

		# Panel T9: keyboard
		#TODO:

		# Panel B1: start/mode
		self.add('B1_SW3', 'gameMode', values=['computer', 'spaceship','games'], TMindex=4, pins=[0,1])
		#self.add('B1_LED','OnOff', TMindex=4, index=1)

		# Panel B2: displays
		self.add('B2_RGB', ['oxygen', 'electricity', 'takeoff', 'overspeed', 'gate1', 'automaticPilot', 'orbit', 'x', 'gate2',
			'landing','alarm', 'y'], pos=1, inverted=[5])
		self.add('B3_DISP', 'counter', TMindex=4, block=0, size=8)

		# Panel B3: laser
		self.add('B3_SW2_0', 'laser', values=['disarmed','armed'], TMindex=7, pin=4, event=laserE)
		self.add('B3_SW2_1', 'laserColor', values=['blue','red'], TMindex=4, pin=7, event=laserE)

		# Panel B4: pilot
		self.add('B4_LED', 'manual', TMindex=4, index=0)
		self.add('B4_POT_0', 'roll', index=0)
		self.add('B4_POT_1', 'yaw', index=1)
		self.add('B4_POT_0', 'speed', index=2)

		# Panel B5: flight mode
		self.add('B5_SW3', 'mode', values=['landing','orbit','takeoff'], TMindex=4, pins=[2,3])
		self.add('B5_SW2', 'autoPilot', values=['manual','auto'], TMindex=4, pin=4)

		# Panel B6: lift-off
		self.add('B6_SW2_1', 'phase1', TMindex=7, pin=7)
		self.add('B6_SW2_2', 'phase2', TMindex=7, pin=5)
		self.add('B6_SW2_3', 'phase3', TMindex=7, pin=6)

		# Panel B7: Joystick
		self.add('B7_PB_UP', 'Up', gpio=7)
		self.add('B7_PB_DOWN', 'Down', gpio=5)
		self.add('B7_PB_LEFT', 'Left', gpio=12)
		self.add('B7_PB_RIGHT', 'Right', gpio=6)

		# Panel B8: commands
		self.add('B8_PB_0', 'RocketEngine', gpio=4)
		self.add('B8_PB_1', 'SpaceshipEngine', gpio=18)
		self.add('B8_PB_2', 'Parachute', gpio=27)
		self.add('B8_PB_3', 'Brake', gpio=17)
		self.add('B8_PB_4', 'Unhook', gpio=14)
		self.add('B8_PB_5', 'OxygenPump', gpio=3)
		self.add('B8_PB_6', 'Laser', gpio=2)
		self.add('B8_PB_7', 'LandingGear', gpio=15)
		self.add('B8_PB_8', 'Go', gpio=22)
		self.add('B8_RGB', ['rocketEngine', 'spaceshipEngine', 'parachute', 'brake', 'landingGear',  'laser', 'oxygenPump',
			'unhook', 'Go'], pos=13, inverted=[18,19])

		# Panel B9: audio
		self.add('B9_SW3', 'Com', values=['Off','COM1','COM2'], TMindex=4, pins=[5,6])


		# intern variables

		self._phase = NOT_YET_INIT    # phase (not yet initialized, during takeoff, in orbit, during landing, etc.)
		self._electricity = 5           # amount of available electricity: 0->none, 1->low level, ..., 3 and more -> good

		self._oxygen = 0
		self._fuelRocket = 0
		self._fuelSpaceship = 0


	# altitude
	@property
	def altitude(self):
		"""get the altitude"""
		return self._altitude

	@altitude.setter
	def altitude(self, alt):
		"""set the altitude, and display it"""
		if self._altitude != int(alt):
			self.DISP_altitude = "%8d"%alt
		self._altitude = int(alt)

	# speed
	@property
	def speed(self):
		"""get the speed"""
		return self._speed

	@speed.setter
	def speed(self, sp):
		"""set the speed and display it"""
		if "%06.2d"%self._speed != "%06.2d"%sp:
			self.DISP_speed = "%06.2d"%sp
		self._altitude = sp

	# position
	@property
	def position(self):
		"""get the position"""
		return self._position

	@position.setter
	def position(self, sp):
		"set the position and display it"
		# send the position to the display
		if "%04.4d"%self._position != "%04.4d"%sp:
			self.DISP_position = "%04.4d"%sp
		self._altitude = sp

	
	
	def laser(self, btn):
		"""Manage changes for the laser switches (SW2_laser and SW2_laserColor)"""
		# modify the RGB_laser led according to the status
		if self._electricity>0:
			if self.SW2_laser == 'armed':
				self.RGB_laser = (RED if self.SW2_laserColor == 'red' else BLUE), FAST
			else:
				self.RGB_laser = BLACK
		else:
			self.RGB_laser = BLACK


	def gates(self, btn):
		"""Manage changes for the gate switch"""
		if self._electricity>0:
			if btn == 'gate1':
				MB.RGB_gate1 = YELLOW   # we come from 'closed', so RGB_gate2 is supposed to be BLACK
			elif btn == 'gate2':
				MB.RGB_gate2 = YELLOW   # we come from 'closed', so RGB_gate1 is supposed to be BLACK
			else:
				MB.RGB_gate1 = BLACK
				MB.RGB_gate2 = BLACK


	def turbo(self, btn):
		"""Manage changes for the turbo switches"""
		# adjust the LEDs according to the switches
		if btn is self.SW2_turbo_gas:
			self.LED_turbo_gas = btn.value
		if btn is self.SW2_turbo_boost:
			self.LED_turbo_boost = btn.value


	def light(self, btn):
		"""Manage changes for the light switches"""
		# adjust the LEDs according to the switches
		if btn is self.SW2_light_cabin:
			self.LED_light_cabin = btn.value
		if btn is self.SW2_light_outside:
			self.LED_light_outside = btn.value


	def electricity(self, btn):
		"""Manage changes for the electricity switches"""
		# adjust the LEDs according to the switches
		if btn is self.SW2_solar:
			self.LED_solar = btn.value
		if btn is self.SW2_battery:
			self.LED_battery = btn.value
		if btn is self.SW2_fuel_cell:
			self.LED_fuel_cell = btn.value
		# amount of electricity
		elec = self.SW2_solar.value*1 + self.SW2_battery.value*2 + self.SW2_fuel_cell.value*4    # 1,2 and 4 as weight
		if elec != self._electricity:
			if elec == 0:
				# shutdown!
				logger.debug("shutdown!")
				RGB.turnOff()
				self.DISP_altitude.off()
				self.DISP_position.off()
				self.DISP_counter.off()
				# self.DISP_speed.off()
				# self.DISP_roll.off()
				# self.DISP_yaw.off()
			else:
				# adjust the brightness
				self.DISP_altitude.setBrightness(elec)
				self.DISP_position.setBrightness(elec)
				self.DISP_direction.setBrightness(elec)
				self.DISP_counter.setBrightness(elec)
				# self.DISP_speed.setBrightness(elec)
				# self.DISP_roll.setBrightness(elec)
				# self.DISP_yaw.setBrightness(elec)
			# set the RGB electricity led
			self.RGB_electricity = GREEN if elec>2 else YELLOW if elec==2 else ORANGE if elec==1 else (RED,FAST)
			self._electricity = elec




	async def start(self):
		"""start !"""

		RGB.turnOff()
		self.askATdata()
		self.DISP_counter.clear()

		self.LED_OnOff = True
		self.RGB_Go = RED,FAST
		logger.debug('Start!')
		self.DISP_counter = '01234567'

		while True:
			com = await ainput(">>>")
			try:
				exec(com)
			except Exception as e:
				print(e)





# create the object and start it !
if __name__ == '__main__':
	MB = MissionBoard()
	MB.run( MB.start)