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
  - [Take-off](#take-off)


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

  
## Start, power, mode
Start the Raspberry Pi
- a switch with a key
- a green led (directly powered by the 5V?)
- rotative switch, with 3 positions : spaceship, game and computer
  - spaceship: main mode to pilot the ship
  - game to run RetroPie
  - computer to switch to the linux desktop (required mouse and keyboard)
+ a plug jack for the power (in the wallet frame)



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


## Lights
Turn on/off the lignts in the spaceship
- on/off switch for the cabin lights
- on/off switch for the extern light
- green leds associated (on when the swith is on, except when there is an eletric problem, see [Electricity](#electricity))


## Water pump
Run the water pump (toilets)
- 3-position switch: water / off / toilets
- associated sound (flush or water flowing)


## Onboard computer
Manage the onboard computer and its potential failure
- 2-pos switch: main computer / backup computer
- one led (display panel)
  - green when main computer and everything is ok
  - red when the main computer has failure (+audio message?)
  - orange when switch to backup computer
  - blinking 5s to simulate reboot time when we switch from one to another one


## Position, speed
Three groups of four seven-segment displays
- two for the *position* (position and altitude)
- one for the speed
Of course, the position will be non-sense values (my kids are too young to understand, and I do not have enough displays to put the 6-axis position)


## Laser
- a missile switch to arm the laser
- a 2-position switch to choose the laser color (blue/red)
- a push-button with led to fire
  - led goes to blinking red or blue when armed
  - goes to red/blue and makes sound when fired
  - cannot be used anymore in the next two seconds (led goes to orange?)

 
## Countdown, time
Height seven-segment displays (two groups of four side-by-side).
Two functions:
- countdown for the takeoff (count down 20s when it starts, with 1/100th of seconds, blink when reach zero if the go-button has not been pressed)
- then display time from takeoff (minuts, seconds, 1/10th seconds - reset when landing)


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


## Fuel
Manage the fuel
- two bargraphs: fuel in spaceship rocket, fuel in the space rocket (or in rocket #1 and rocket #2)
- 3-position switch: pump fuel spaceship on / pumps off / pump fuel rocket on (only defore takeoff)
- when one of the pump is on, play sound and increase the associated bargraph level. Stop when the fuel tank is full

The fuel of the space rocket decrease quickly after takeoff (1min?). The fuel of the spaceship varies with the power of the rocket (slider in [pilot](#pilot). The bargraphs blink when the fuel is too low


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


## Take-off
Séquence à suivre (pour finir le décollage et passer à un autre mode) :
- enclencher le bouton rocket "Phase 1" (ou "début séquence décollage")
- mettre tous les niveaux (carburant et oxygène) à max pour passer à la phase suivante
- enclencher le bouton rocket "Phase 2" (ou "Préchauffage des moteurs")
  - erreur si les niveaux ne sont pas à max et bouton "Phase 1" enclenché
- activer le moteur fusée (bouton poussoir, qui passe en bleu si c'est ok)
- fermeture du sas
- pilote automatique enclenché
- enclencher le bouton rocket "Phase 3" (ou "Paré au décollage")
  - erreur si moteur fusée non activé, sas non fermé, pilote auto non enclenché
- le compte à rebours se déclenche (avec son?)
- il faut appuyer sur le bouton rouge Go!
- décollage en cours (les moteurs s'allument, donc voyant moteur qui clignote/change de couleur, altitude qui augmente, carburant fusée qui diminue)
- au bout de 30s on peut décrocher la fusée (bouton "décrochage fusée" qui clignote qd c'est près, qui passe au rouge qd ça se fait, et puis s'éteind)
- il faut allumer les moteurs de la navette (bouton "moteur navette", qui clignote qd c'est près, passe au vert qd ils s'allument, carburant moteur diminue)
- la séquence est finie (voyant qui clignote ?), on peut passer au mode "orbite"

## Orbit
Mode normal
- on peut passer en pilote manuel, augmenter la puissance, piloter avec le joystick, etc.

## Atterrissage
Séquence à suivre:
- allumage des moteurs navette (bouton moteurs navette)
- pilote automatique
- sortie du train d'atterrissage (bouton train aterrissage)
- maintenir le lacet/roulis autour de zéro (potards) ???? voyant 
- diminuer la vitesse qd altitude <50 (sinon voyant survitesse en rouge + clignotement afficheur vitesse)
- qd altitude arrive à zero, il faut sortir le parachute (bouton parachute, passe en vert quand ouvert)
- freinage (bouton poussoir freinage)
- extinction des moteurs






# I/O (remplis au fur et à mesure des fonctionalités)

#### Bargraphs (max 4, dont 3 panneau haut) :
+ niveau Oxygène
+ niveau carburant fusée
+ niveau carburant navette
  
#### Blocs de 4 afficheurs 7-segment (max 3 panneau haut, 4 bas):
- vitesse
- position
- altitude
+ compte à rebours (x2), panneau bas
- lacet/roulis ???
  
#### Leds :
+ démarrage (directe sur Alim)
+ lumière cabine
+ lumière extérieure
+ panneau solaire (en directe sur switch associé ?)
+ batteries
+ pile à combustible
- pompe carburant fusée
- pompe carburant navette
+ commandes manuelles


#### Switch 2 positions (max 10) :

+ lumière cabine
+ lumière extérieure
+ ordinateur de bord/de secours
+ panneau solaire
+ batteries
+ piles à combustible
+ pilote automatique/commandes manuelles
+ couleur de laser

+ turbo gaz tuyères
+ turbo boost



#### Switch 3 positions (max 10) :
+ sas (porte 1 / sas fermé / porte 2)
+ pompe eau (eau/off/toilettes)
+ pompe carburant (réservoir fusée/off/réservoir navette)
+ audio COM1/Off/COM2

#### Boutons poussoirs (max 10 normaux + 1 gros) :
+ pompe oxygène
+ moteurs fusée
+ décrochage fusée
+ moteurs navette
+ Go! (gros bouton rouge)
+ train d'atterissage
+ ouverture parachute
+ freinage
+ laser
  
#### Voyants lumineux (12 ?) :
+ oxygène  
+ porte 1
+ porte 2
+ électricité
+ pilote automatique
+ alarme/anomalie
+ décollage
+ orbite
+ atterrissage
+ indicateur de survitesse
  
  
#### Potentiomètres (1 en ligne, max 5 rotatif) :
+ son
+ puissance moteurs (en ligne)
+ lacet
+ roulis

#### Clé (1) :
+ démarrage du Rpi

#### Switch rotatif x positions (max 2, x<12): 
+ démarrage (jeux/ordinateur/navette)
- mode de vol (décollage, orbite, attérrissage)

#### Boutons "rocket" (avec LED)
+ phase 1
+ phase 2
+ phase 3

##### Autres :
+ Joystick : commande manuelle
- Hauts-parleurs : son
+ Prises USB :
+ Prises audio Jack 3.5mm : son
- Prise alimentation (sur chassis) : démarrage
+ Raspberry  
  
  
  
  
  
  
  
  
  
# notes diverses  

à mettre à jour

###RPi i/o:
- 6 pour les quatre TM1638 (clk+data, et un Enable par TM)
- 4 pour le joystick
- 6 pour les boutons jeux/commande
- 1 pour le gros bouton
- 2 (ou plus) pour le µC (leds WQ2812b, potentiomètres analogiques)

###RPi USB:
- 1 ou 2 ports libres (souris, clavier, joystick, etc.)
- 1 port touchscreen du LCD
- 1 port carte son ?
- 1 port pour carte USB I/O (Zero delay arcade) ?



####1er TM1638:
2 afficheurs 4x7seg. (1 sur la carte, 1 à côté)
4 switch 3 positions
8 leds (4 switchs 3 pos)
2eme TM1638:
1 afficheur 7seg.
2 bargraph 10seg.
2 boutons jeux/commande
3 switchs 3 pos (sans led?) v  

#### µC
- i2C (2 I/O) + interrupt (1 output) ?
- APA106 (2 outputs)
- potentiometer (3 Analog inputs)
- 9 push buttons + 4-way joystick (3 outputs, 5 inputs)


