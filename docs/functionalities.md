# Functionnalities

This is the list of the functionalities I wanted for the *Mission Board*
Once defined, it allows me to know the buttons, switches, displays, ... I need, to decide how to pilot them (see TM1638) and to define the software (its behavior):

- [Oxygen](#oxygen)
- [Start/Mode](#start-power-mode)
- [Audio](#audio)
- [Doors](#doors-decompression-airlock)
- [Lights](#lights)
- [Water pump](#water-pump)
- [Onboard computer](#onboard-computer)


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


## Altitude and speed
Trois groupes d'afficheur 7-seg
- deux afficheurs pour la position (position/altitude) (on est bien d'accord que ça n'a pas de sens)
- un pour la vitesse

## Laser
- missile swith pour armer le laser
- switch 2 positions pour la couleur du laser (bleu/rouge)
- un bouton lumineux pour tirer
  - passe au rouge ou bleu qd armé
  - fait du son qd on tire

 
## Compte à rebours - durée mission
Huit afficheurs 7-segments (2 groupes de 4 collés).
Deux fonctions
- compte à rebours (décompte 20s qd il est déclenché, avec les centièmes de sec; clignote qd on arrive à zéro si on n'a pas lancé)
- puis compte la durée de la mission (ne peut être remis à zéro qu'à l'atterrissage)

## Electricity
Gestion de l'électricité produite
- Séries de switchs, avec sa led 
  - panneaux solaires (on/off), led verte en direct
  - batteries (on/off), led verte
  - piles à combustible (on/off), led verte
- voyant lumineux "électricité" -> vert qd tout est ok, orange si un seul élément de branché, rouge si tout est à off

Si tout est à off, le panneau s'éteind, saut le voyant lumineux "électricité" qui passe au rouge (+ son alerte). On perd la batterie au bout de 5min, et la piles à combustible au bout de 15min ?


## Carburant
Gestion du carburant
- deux bargraph : moteurs fusée, moteurs navette/vaisseau (ou bien moteur 1 et moteur 2)
- switch 3 pos. pompe fusée / off / pompe vaisseau (ne sert qu'avant le décollage)
- deux leds (vertes) allumée qd le remplissage s'effectue (1 led en face de "pompe fusée", l'autre pour "pompe vaisseau"), puis s'éteind qd le remplissage est fini (10s ?)

Le carburant fusée se vide rapidement après décollage (1min?), le carburant navette se vide en fct de la puissance moteurs
Les bargraph carburant moteurs clignotent en rouge qd plus de carburant

## Pilote automatique
- switch pilote automatique / commandes manuelles
- voyant lumineux "pilote automatique"
  - en vert quand enclenché
  - éteind qd mis sur off (ou en bleu)
  - passe en orange en cas de problème (doit être désactivé, ou bien on passe sur l'ordinateur de secours)
- active la LED "commandes manuelles" qd on n'est pas en pilote automatique
 
Le pilote automatique fait bouger doucement les compteurs d'altitude/position et vitesse en mode "stationnaire" (ou bcp en mode "décollage"/"atterissage").
Les commandes manuelles font bouger les compteurs altitude/position/vitesse plus vite

## Commande manuelles
- joystick
- potentiomètre linéaire : puissance moteurs
- 2 potentiomètres : lacet/roulis
- LED verte allumée qd mode "commande manuelle"

-> influent sur les compteurs vitesse/position/altitude en mode "commandes manuelles" (et sur la vitesse de consommation carburant ?)

# Alarme
- voyant lumineux alarme
  - éteint lorsqu'un aucun problème
  - rouge (clignotant ou non) lorsque problème, avec signal sonore
le voyant s'allumera lorsque qu'une panne sera détectée (simulée), en complément d'un autre voyant indiquant le pb


## Moteurs
- voyant lumineux de survitesse (qd vitesse trop grande ou >50 en fin d'atterrissage)
- bouton moteurs fusée
- bouton moteurs navette
- potentiomètre en ligne pour régler la puissance des moteurs
- 2 switchs pour le turbo (gaz tuyères et boost)
  -> change la vitesse, c'est tout
- 2 leds associées
Lien avec le carburant


## train d'atterrissage
- bouton poussoir train
  - un appui pour le sortir (10s en oragne le temps qu'il sorte + son, et ensuite en vert pour dire qu'il est sorti)
  - un appui pour le rentrer (idem, voyant éteind qd il est rentré)

Utilisable uniquement pendant le mode d'atterissage (sinon inactif, ou bien provoque une alarme de quelques secondes: voyant alarme + voyant du bouton en rouge clignotant 5s)


## Pilotage
- un bouton rotatif 3 pos. permet de choisir le mode
  - décollage
  - orbite
  - atterrissage
- 3 voyants lumieux (décollage/orbit/atterrissage) pour indiquer dans quel état on est

l'alarme retentit (+son?) et le voyant correspondant passe en orange (rouge?) si on change de mode alors qu'une séquence n'est pas terminée (tant qu'on n'est pas revenu dans le bon mode) 

### Décollage
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

### Orbite 
Mode normal
- on peut passer en pilote manuel, augmenter la puissance, piloter avec le joystick, etc.

### Atterrissage
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


