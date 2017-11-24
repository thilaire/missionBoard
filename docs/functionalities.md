# Functionnalities

This is the list of the functionalities I wanted for the *Mission Board*
Once defined, it allows me to know the buttons, switches, displays, ... I need, to decide how to pilot them (see TM1638) and to define the software (its behavior):

- Start:
  - [Start/Mode](#start-power-mode)
- misc functionalities:
  - [Oxygen](#oxygen)
  - [Audio](#audio)
  - [Doors](#doors-decompression-airlock)
  - [Water pump](#water-pump)
  - [Laser](#laser)
- electricity:
  - [Electricity](#electricity)
  - [Lights](#lights)
- levels to display:
  - [Position/Speed](#position-speed)
  - [Countdown, time](#countdown-time)
  - [Fuel](#fuel)
- computer:
  - [Onboard computer](#onboard-computer)
  - [Alarm](#alarm)
- flight
  - [Engine](#engine)
  - [Automatic pilot](#automatic-pilot)
  - [Manual command](#manual-command)
- flight modes:
  - [Landing gear](#landing-gear)
  - [Pilot mode](#pilot-mode)
  - [Take-off mode](#take-off-mode)
  - [Orbit mode](#orbit-mode)
  - [Landing](#landing)



## Start, power, mode
Start the Raspberry Pi
- a switch with a key
- a green led (directly powered by the 5V?)
- rotative switch, with 3 positions : spaceship, game and computer
  - spaceship: main mode to pilot the ship
  - game to run RetroPie
  - computer to switch to the linux desktop (required mouse and keyboard)
+ a plug jack for the power (in the wallet frame)


## Oxygen
This is about the oxygen gas in the spaceship
- a bargraph indicating the level of oxygen
- an "oxygen pump" pushbutton (with led):
  - activate the pump during 10s (sound + blue led during that time + oxygen level rising in the same time)
  - led blue blinking when the pump runs (during 10s), off otherwise
  - led red blinking if the pump is out of order (reparable by activating the backup computer)
- "oxygen" led (display panel)
    - green if the oxygen level is ok
    - orange blinking if the level is low
    - red if we will run out of oxygen

## Audio
Sound through speakers or headphone
- speakers (todo)
- headphone plug (w/o microphone?)
- 3-position switch for the radio-communications:
  - COM1 (recorded sound from real space missions (see [Nasa audio database](https://archive.org/details/nasaaudiocollection) or [Apollo17](http://apollo17.org/))
  - OFF (no radio-communication)
  - COM2 (other sound, to be defined later)
- potentiometer for the volume


## Doors (decompression airlock)
Open the decompression doors (airlock - 2 doors)
- 3-position switch: (1) door #1 open / (2) doors locked / (3) door #2 open
   - the two doors cannot be opened in the same time
   - (2) -> (3): oxygen pump during 5s (level increases), and then the door #2 opens
   - (3) -> (2): door #2 closes, and then oxygen pump for 5s (level decreases)
   - (1) -> (2): door #1 closes
   - (2) -> (1): door #1 opens
- two leds (display panel), one per door:
  - door #1: green when closed, blinking orange during opening/closing, yellow when opened
  - door #2: green when closed, blinking orange during opening/closing, blinking red when opened

Opening/Closing during 5s (leds + sound)
Everything stop + leds in red (+ warning sound?) if we go to fast from (1)<->(2)<->(3), only stop when we go back to position(2)


## Water pump
Run the water pump (toilets)
- 3-position switch: water / off / toilets
- associated sound (flush or water flowing)

## Laser
- a missile switch to arm the laser
- a 2-position switch to choose the laser color (blue/red)
- a push-button with led to fire
  - led goes to blinking red or blue when armed
  - goes to red/blue and makes sound when fired
  - cannot be used anymore in the next two seconds (led goes to orange?)

## Electricity
Manage the production of electricity
- three switches, with led
  - solar panels (on/off), green led
  - batteries (on/off), green verte
  - fuel cell (on/off), green led
- led (display panel) "electricity":
  - green when everything is ok
  - orange when only one element is plugged (on)
  - red if everything is off

If the three switches are off, all the displays turn off, except the "electricy" led in the display panel that goes to red (+ warning sound)
The batteries goes down 5min after takeoff, and fuel cell after 15min ?


## Lights
Turn on/off the lignts in the spaceship
- on/off switch for the cabin lights
- on/off switch for the extern light
- green leds associated (on when the swith is on, except when there is an eletric problem, see [Electricity](#electricity))


## Position, speed
Three groups of four seven-segment displays
- two for the *position* (position and altitude)
- one for the speed
Of course, the position will be non-sense values (my kids are too young to understand, and I do not have enough displays to put the 6-axis position)


## Countdown, time
Height seven-segment displays (two groups of four side-by-side).
Two functions:
- countdown for the takeoff (count down 20s when it starts, with 1/100th of seconds, blink when reach zero if the go-button has not been pressed)
- then display time from takeoff (minuts, seconds, 1/10th seconds - reset when landing)


## Fuel
Manage the fuel
- two bargraphs: fuel in spaceship rocket, fuel in the space rocket (or in rocket #1 and rocket #2)
- 3-position switch: pump fuel spaceship on / pumps off / pump fuel rocket on (only defore takeoff)
- when one of the pump is on, play sound and increase the associated bargraph level. Stop when the fuel tank is full

The fuel of the space rocket decrease quickly after takeoff (1min?). The fuel of the spaceship varies with the power of the rocket (slider in [pilot](#pilot). The bargraphs blink when the fuel is too low





## Onboard computer
Manage the onboard computer and its potential failure
- 2-pos switch: main computer / backup computer
- one led (display panel)
  - green when main computer and everything is ok
  - red when the main computer has failure (+audio message?)
  - orange when switch to backup computer
  - blinking 5s to simulate reboot time when we switch from one to another one


## Alarm
- led (display panel)
  - off when no problem occurs
  - red (maybe blinking) when a problem arises, (with sound?)
The led will turn on when a breakdown is detected (simulated), in addition to the led associated to the problem


## Engines
- led (display panel) for the overspeed (when the speed is too large or >50 during landing)
- push button to turn on the engines of the rocket
- push button to turn on the engines of the spaceship
- inline potentiometer for the engine power
- 2 switchs for the turbo (gas in the nozzles and boost) -> doesn't mean anything, just for fun
  -> change the speed, that's all
- 2 associtaed leds


## Automatic pilot
- switch automatic pilot / manual commands
- led (display pannel) "automatic pilot"
  - green when engaged
  - turn off (or blue) when manual commands
  - goes to orange in case of problem (must be desactivated, or maybe go to backup computer)
- green led "manual commands" activated when manual command
 
The automatic pilot make the counters altitude/position/vitesse vary very slowly (except during take off and landing).
During manual command mode, these counters vary with the corresponding potentiometer (so more quickly)


## manual command
- a joystick (also used for game)
- linar potentiometer (rockets' power)
- two potentiometer: pitch/yaw (roll?)
- green led switch on when manual command (see [Automatic pilot](#automatic-pilot))

-> has influence on the speed/position/altitude in manual command mode (and on the fuel consumption)


## landing gear
- push button with led
  - one push to unfold the landing gear (10s in orange, the time its unfolds + sounds, and then green to indicated the gear is unfolded)
  - one push to fold it (same during 10s, and then led off)

Only usable during the landing mode (otherwise inactive... or maybe start a few seconds alarm + sound + led in blinking red)


## Pilot mode
- rotative 3-position button to choose the mode
  - take-off
  - flight in orbit
  - landing
- 3 leds in the display panel to indicate in which mode we are

Alarm (led+sound) + corresponding led goes to orange (blinking red?) when we switch mode while a sequence is not over (alarm while we did not go back to the right mode)


## Take-off mode
Sequence to follow (to finish the take-off and be able to go to another mode, like flight in orbit):
- engage the rocket button "Phase 1"(ou "start of the take-off sequence")
- put all the levels (fuel and oxygène) to max to go to the next phase
- engage the rocket button "Phase 2") (or "Pre-heat engines")
  - error of the levels are not to their max and "phase 1" button not engaged) -> led + sound
- activate the rocket engine (push button that goes to bleu when pushed)
- close the doors
- turn on the automatic pilot
- engage the button rocket "Phase 3" (or "ready to take-off")
  - error (led+sound) if doors, engine or automatic pilot are not as needed)
- the countdown turns on (starts with 10.000 seconds)
- We need to push the "Go" button when the countdown goes around 0 (+/- 1 secondes, otherwise the "phase 3" must be done again)
- take-off (the engine turns on (associated led blinks/changes its color, altitude increases quickly, rocket fuel deacreases)
- After 30s, we can unhook the spaceship (push-button "unhook spaceship" that blinks when it's readed, goes to red during unhooking (5s) and then turns off)
- we need to turn on the spaceship engines (push button "spaceship engine" that blink when we can do it, and goes to red when the engines are on; the fuel decreases)
- then the sequence is over (led in display label that blinks?), we can go to "orbit mode"


## Orbit mode
It is the "normal" mode
- we can use manual pilot mode, change the power, use the joystick...
-> we cannot switch to takeoff mode anymore


## Landing
Sequence to follow
- turn on the spaceship engine (push button spaceship engine)
- turn on automatic pilot
- unfold the landing gear (push button associated), maybe only when the altitude is "low"
- maintain the pitch/roll around zero (with the potentiometer) Add alarm when the pitch/roll is not correct ?
- decrease the speed when the altitude is <50 (otherwise the led (panel display) "overspeed" turns on in red and the speed display blinks)
- when altitude goes to zero, we need to deploy the parachute (push button with led, led goes to blinking blue when we can deploy it, green when it is deployed)
- brakes (with the push button "brakes")
- then turn off the engines
